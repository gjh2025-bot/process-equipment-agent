# Demo Script (~90 seconds)

A tight script for presenting the Process Equipment Selection Assistant on
ASI:One. English lines are ready to speak; _italics_ are stage directions.

---

## 1. The pitch (~15s)

> "When a chemist has a process that works at lab scale, the first engineering
> question is: **what equipment do I need to scale it up, and roughly what will
> it cost?** Today that takes an engineer hours of manual screening. Our agent
> does a **preliminary pass in seconds** — and you just talk to it on ASI:One."

## 2. Live demo (~50s)

_Open your agent in ASI:One. Type:_

**`analyze`**

> "I gave it a real case — scaling a lab-scale **hydrothermal synthesis of
> MnO₂** for battery cathodes from 40 mL up to a 2-liter pilot batch. It
> recognized the reaction, scaled it 50×, broke it into unit operations, and
> recommended equipment for each — a **pressure-rated Teflon-lined autoclave**
> for the 180 °C reaction, vacuum filtration for the fine particles, a vacuum
> oven for drying — with a rough CAPEX range."

_Then ask a follow-up to show it reasons, not just dumps:_

**`why the Teflon-lined autoclave?`**

> "Notice it explains the *why* — pressure rating, contamination control for
> battery-grade purity. And this is the key part: **the equipment, prices, and
> suppliers all come from a deterministic engineering workflow** — the language
> model only phrases it conversationally, it never makes up data."

_Then:_

**`rfq`**

> "And it drafts a ready-to-send supplier inquiry, stating our operating point
> and what the equipment must be rated to cover."

## 3. The close (~20s)

> "Under the hood it's a **Fetch.ai uAgent** on Agentverse, ASI:One-compatible
> via the chat protocol, wrapping a transparent rule-based workflow. It's
> positioned honestly as **preliminary decision-support** — not a certified
> design — so an engineer reviews the output before procurement. Next steps are
> splitting it into specialist sub-agents and adding human-in-the-loop selection."

---

## Backup / Q&A one-liners

- **"Is it making the numbers up?"** — No. A deterministic Python workflow
  selects equipment and computes CAPEX from a database; the LLM only explains.
- **"What if the LLM is down?"** — It falls back to clean rule-based replies, so
  the demo never breaks.
- **"How is it scoped?"** — Mock data, preliminary only, requires engineer
  review. No process simulation or vessel design.
- **"Why Fetch.ai?"** — Modular agent design; the manager can later coordinate
  specialist sub-agents, all discoverable and chat-accessible via ASI:One.
