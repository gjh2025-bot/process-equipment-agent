![domain:chemical-engineering](https://img.shields.io/badge/domain-chemical%20engineering-blue)
![tech:uagents](https://img.shields.io/badge/tech-uAgents-orange)
![protocol:chat](https://img.shields.io/badge/protocol-chat-green)
![status:mvp](https://img.shields.io/badge/status-MVP-lightgrey)

# Process Equipment Selection Assistant

A conversational manager agent that turns a **lab-scale chemical synthesis
brief** into a **preliminary pilot-scale equipment recommendation** — complete
with screening reasoning, mock suppliers, a rough CAPEX range, and an
RFQ-style supplier inquiry draft.

It is an early-stage **decision-support** tool, not a certified process design
tool. All equipment and supplier data is mock data for demonstration.

---

## What it does

Acting as a coordinator ("manager"), the agent runs a deterministic workflow
over your process brief:

1. **Recognize** the process — product, reaction route, and key cautions.
2. **Scale up** by simple ratio (lab volume → target pilot volume).
3. **Decompose** into unit operations (mixing, reaction, separation, washing,
   drying, collection).
4. **Select & screen** candidate equipment on temperature, pressure, volume,
   and contamination control — with transparent accept/reject reasoning.
5. **Match suppliers** and estimate a rough, deduplicated CAPEX range.
6. **Draft an RFQ** that states your operating point and what the equipment
   must be rated to cover.

The equipment, suppliers, and prices always come from the deterministic
workflow — the language model only helps explain the results conversationally,
never inventing data.

---

## How to talk to it

Just chat naturally. Useful prompts:

- `hi` — short intro and options
- `analyze` — run the built-in **MnO₂ hydrothermal** demo case
- `what equipment do you recommend for my MnO₂ process?`
- `why the Teflon-lined autoclave?`
- `rfq` — get the supplier inquiry draft for the latest analysis
- Paste your own process brief as **JSON** to analyze a different case

---

## Example interaction

**You:** what equipment do you recommend for my MnO₂ process?

**Agent:** For the 2 L bench-pilot batch (scaled 50× from a 40 mL lab recipe),
the recommended equipment includes a **Teflon-lined stainless steel batch
autoclave** for the 180 °C hydrothermal reaction, a **vacuum filtration setup**
for separating the fine MnO₂ particles, and a **vacuum oven** for drying — all
chosen for high contamination control. Rough mock CAPEX: **$11,550 – $278,000**.
This is preliminary, mock-data decision support — please have a qualified
process engineer review it. Reply `rfq` for the supplier inquiry draft.

---

## Demo case

Scale-up of a lab-scale **hydrothermal synthesis of MnO₂ nanoparticle powder**
for aqueous zinc-ion battery cathodes (40 mL lab batch → 2 L bench-pilot).

## Limitations

- Preliminary and illustrative only — **requires review by a qualified process
  engineer before any procurement**.
- No process simulation, heat/mass balance, or pressure-vessel design.
- Prices, lead times, and suppliers are mock placeholders, not quotes.

## Source

Built on a local-first, standard-library Python workflow wrapped as a uAgent
using the chat protocol. Repository:
`https://github.com/gjh2025-bot/process-equipment-agent`
