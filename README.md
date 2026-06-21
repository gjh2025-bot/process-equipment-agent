# Process Equipment Selection Assistant

A local-first engineering prototype that turns a lab-scale process brief into a
**preliminary equipment recommendation report**. The demo case is the scale-up
of a lab-scale hydrothermal synthesis of **MnO₂ nanoparticle powder** for
aqueous zinc-ion battery cathodes.

It is an early-stage **decision-support** tool, not a certified process design
tool. All equipment and supplier data is mock data for demonstration.

## What it does

Given a structured process brief, it runs a simple, deterministic workflow:

```
data/sample_input.json
  -> process_basis        (product, scale, scale-up factor, missing data)
  -> unit_decomposer      (break process into unit operations)
  -> equipment_selector   (find candidate equipment from a mock database)
  -> engineering_reviewer (screen on temperature / pressure / volume, recommend)
  -> supplier_matcher     (match mock suppliers, rough CAPEX range)
  -> rfq_generator        (draft an RFQ-style supplier inquiry)
  -> outputs/sample_output.json   (structured result)
  -> outputs/sample_report.md     (human-readable report)
```

Every step is rule-based and transparent: the report shows **why** each
equipment candidate was accepted or rejected.

## Requirements

- Python 3.9+ (developed on 3.11). **No third-party packages** — standard
  library only, so `requirements.txt` is intentionally empty.

## How to run

From the project root:

```bash
python main.py --input data/sample_input.json
```

On Windows, if `python` is not found (the Microsoft Store stub), use the
Python launcher instead:

```powershell
py main.py --input data/sample_input.json
```

This writes two files into `outputs/`:

- `outputs/sample_output.json` — full structured result
- `outputs/sample_report.md` — readable report for demo

## Project structure

```
hackathon-project/
  main.py                     # workflow entry point / orchestration
  requirements.txt            # empty (standard library only)
  data/
    sample_input.json         # the demo process brief
    equipment_database.json   # mock equipment knowledge base
    supplier_database.json    # mock supplier + CAPEX data
  src/
    process_basis.py
    unit_decomposer.py
    equipment_selector.py
    engineering_reviewer.py
    supplier_matcher.py
    rfq_generator.py
  outputs/
    sample_output.json        # generated
    sample_report.md          # generated
  docs/
    project_guide.md
    architecture.md
```

## Example result (MnO₂ demo)

For the 2 L bench-pilot batch, the workflow recommends, for example:

| Unit operation              | Recommended equipment                         |
| --------------------------- | --------------------------------------------- |
| Hydrothermal batch reaction | Teflon-lined stainless steel batch autoclave  |
| Solid-liquid separation     | Lab or pilot vacuum filtration setup          |
| Vacuum drying               | Vacuum oven                                    |

- Rough total CAPEX (mock, deduplicated): **$11,550 – $278,000 USD**
- Equipment shared across steps (e.g. the reactor used for both reaction and
  cooling) is counted once in the CAPEX total.

## Scope and limitations

- Preliminary and illustrative only — **requires review by a qualified process
  engineer before any procurement**.
- No process simulation, heat/mass balance, or pressure-vessel design.
- No real web search, supplier APIs, ASPEN integration, or external LLM calls.
- Prices, lead times, and suppliers are mock placeholders.

## Possible future work

The modular design is intended to later wrap into a Fetch.ai / uAgents system
(coordinator agent + equipment specialist agents, ASI:One chat interface).
This comes only after the local workflow is stable. See `docs/architecture.md`.
