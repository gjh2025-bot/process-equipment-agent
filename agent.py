"""
agent.py

ASI:One-compatible manager uAgent for the Process Equipment Selection
Assistant.

This agent wraps the existing local workflow (see main.py / src/) and exposes
it over the uAgents chat protocol, so it can be reached from ASI:One.

Design for the hackathon MVP:
  - The agent's "brain" is the deterministic local workflow (mock data only).
  - On any chat message it acts as a coordinator ("manager"): it recognizes the
    process, runs the unit decomposition + equipment screening + supplier
    matching (the "specialist" steps), and replies with a readable summary.
  - If the user sends a JSON process brief, it is used as the input. Otherwise
    the bundled MnO2 sample is used, so a judge can just say "hi" and get a
    full demo.
  - Reply "rfq" to get the RFQ-style supplier inquiry draft (human-in-the-loop).

Run locally:  python agent.py
"""

import json
import os
import sys
from datetime import datetime
from uuid import uuid4

# Make src/ importable and reuse the existing workflow.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from main import run_workflow_from_dict, load_json, EQUIPMENT_DB_PATH  # noqa: E402

from uagents import Agent, Context, Protocol  # noqa: E402
from uagents_core.contrib.protocols.chat import (  # noqa: E402
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SAMPLE_INPUT_PATH = os.path.join(PROJECT_ROOT, "data", "sample_input.json")

# Optional ASI:One LLM layer. If an API key is set, the agent uses the LLM to
# converse naturally on top of the deterministic analysis. If not, it falls
# back to the rule-based replies, so the demo never breaks.
ASI_ONE_API_KEY = os.environ.get("ASI_ONE_API_KEY", "").strip()
_llm_client = None
if ASI_ONE_API_KEY:
    from openai import OpenAI

    _llm_client = OpenAI(base_url="https://api.asi1.ai/v1", api_key=ASI_ONE_API_KEY)


def llm_reply(grounding, user_text):
    """Ask the ASI:One LLM to answer naturally, grounded in the analysis.

    Returns None on any failure so the caller can fall back to a fixed reply.
    """
    if not _llm_client:
        return None
    system_prompt = (
        "You are a process equipment selection assistant for early-stage "
        "chemical process scale-up. A deterministic tool has ALREADY produced "
        "the analysis below. Answer the user using ONLY this analysis - never "
        "invent equipment, prices, suppliers, or numbers. Be concise, friendly, "
        "and conversational. For a greeting, give a one or two sentence intro "
        "and offer to analyze or show the demo - do NOT dump the whole report. "
        "When giving recommendations, remind the user this is preliminary, "
        "mock-data decision support.\n\n"
        "=== ANALYSIS (ground truth) ===\n{}".format(grounding)
    )
    try:
        response = _llm_client.chat.completions.create(
            model="asi1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text or "hello"},
            ],
            max_tokens=1024,
        )
        return str(response.choices[0].message.content)
    except Exception:
        return None


agent = Agent(
    name="equipment-selection-manager",
    seed="process-equipment-selection-assistant-seed-v1",
    port=8001,
    mailbox=True,
    publish_agent_details=True,
)

protocol = Protocol(spec=chat_protocol_spec)


# ----------------------------------------------------------------------------
# Turning a workflow result into a short, chat-friendly report.
# ----------------------------------------------------------------------------
def recognize_process(process_input):
    """Surface what the manager 'recognized' about the process brief."""
    lab = process_input.get("lab_scale_process", {})
    product = process_input.get("target_product", {})
    lines = []
    if product.get("name"):
        lines.append("- Target product: {}".format(product["name"]))
    if lab.get("synthesis_route"):
        lines.append("- Reaction / route: {}".format(lab["synthesis_route"]))
    concerns = process_input.get("known_process_concerns", [])
    if concerns:
        lines.append("- Key cautions:")
        for concern in concerns[:3]:
            lines.append("    - {}".format(concern))
    return "\n".join(lines)


def format_chat_report(process_input, result):
    """Build a concise markdown summary suitable for a chat reply."""
    basis = result["process_basis"]
    lines = []

    lines.append("**Process Equipment Selection - Preliminary Recommendation**")
    lines.append("")
    lines.append("_What I recognized:_")
    lines.append(recognize_process(process_input))
    lines.append("")
    lines.append(
        "_Scale-up:_ lab {} mL -> target {} L (factor {}).".format(
            basis["lab_scale_basis"].get("batch_liquid_volume_ml"),
            basis["target_scale_basis"].get("target_batch_liquid_volume_l"),
            basis.get("scale_up_factor"),
        )
    )
    lines.append("")
    lines.append("**Recommended equipment per unit:**")
    for review in result["equipment_review"]:
        rec = review["recommended_equipment"]
        if rec:
            lines.append(
                "- {}: {} ({}, contamination control: {})".format(
                    review["unit_name"],
                    rec["equipment_name"],
                    rec["equipment_id"],
                    rec.get("contamination_control_level", "n/a"),
                )
            )
        else:
            lines.append(
                "- {}: no suitable equipment accepted".format(review["unit_name"])
            )
    lines.append("")

    capex = result["supplier_matching"]["capex_summary"].get("rough_total_capex_usd")
    if capex:
        lines.append(
            "**Rough total CAPEX (mock, deduplicated):** ${:,} - ${:,} USD".format(
                capex[0], capex[1]
            )
        )
    lines.append("")
    lines.append(
        "Reply **rfq** for the RFQ-style supplier inquiry draft, or send your own "
        "process brief as JSON to analyze a different case."
    )
    lines.append("")
    lines.append(
        "_Preliminary, mock-data decision support. Requires review by a "
        "qualified process engineer._"
    )
    return "\n".join(lines)


def format_rfq_reply(result):
    """Build a chat reply containing the RFQ draft."""
    rfq = result["rfq_draft"]
    lines = ["**RFQ-Style Supplier Inquiry Draft**", "", rfq["intro"], ""]
    for index, item in enumerate(rfq["items"], start=1):
        lines.append("**Item {}: {}** ({})".format(
            index, item["equipment_type"], item["equipment_example"]))
        for condition in item["operating_conditions"]:
            lines.append("- {}".format(condition))
        if item["candidate_suppliers"]:
            lines.append("- Candidate suppliers: {}".format(
                ", ".join(item["candidate_suppliers"])))
        lines.append("")
    lines.append(rfq["closing"])
    return "\n".join(lines)


def parse_input_or_default(text):
    """Use the user's JSON brief if provided, else the bundled sample."""
    text = (text or "").strip()
    if text.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    return load_json(SAMPLE_INPUT_PATH)


GREETINGS = {
    "hi", "hello", "hey", "help", "start", "menu", "yo", "sup",
    "hola", "你好", "?", "hi!", "hello!",
}


def welcome_message():
    """Short, friendly intro shown for greetings (instead of a wall of text)."""
    return (
        "Hi! I'm the **Process Equipment Selection Assistant**. I take a "
        "lab-scale chemical synthesis brief and recommend pilot-scale "
        "equipment, mock suppliers, and an RFQ draft (preliminary, mock-data "
        "decision support).\n\n"
        "Try one of these:\n"
        "- **analyze** - run the built-in MnO2 hydrothermal demo case\n"
        "- paste your own process brief as **JSON** to analyze a different case\n"
        "- **rfq** - get the supplier inquiry draft for the last analysis\n\n"
        "What would you like to do?"
    )


# ----------------------------------------------------------------------------
# Chat protocol handlers.
# ----------------------------------------------------------------------------
@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # Acknowledge every incoming message, as the chat protocol expects.
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    text = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            text += item.text

    stripped = text.strip()
    lowered = stripped.lower()
    store_key = "last_input:{}".format(sender)

    try:
        if lowered == "rfq":
            # Keep RFQ deterministic so the exact inquiry wording is preserved.
            last = ctx.storage.get(store_key)
            process_input = json.loads(last) if last else load_json(SAMPLE_INPUT_PATH)
            result = run_workflow_from_dict(process_input)
            reply = format_rfq_reply(result)
        else:
            # Run the deterministic analysis (JSON brief if provided, else the
            # built-in MnO2 demo case) and use it as ground truth.
            process_input = parse_input_or_default(text)
            ctx.storage.set(store_key, json.dumps(process_input))
            result = run_workflow_from_dict(process_input)
            report = format_chat_report(process_input, result)

            # If an LLM is configured, let it answer naturally grounded on the
            # report. Otherwise fall back to fixed, rule-based replies.
            reply = llm_reply(report, stripped)
            if reply is None:
                if not stripped or lowered in GREETINGS:
                    reply = welcome_message()
                else:
                    reply = report
    except Exception:
        ctx.logger.exception("Error running workflow")
        reply = "Sorry, I could not process that request."

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=reply),
                EndSessionContent(type="end-session"),
            ],
        ),
    )


@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass


agent.include(protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
