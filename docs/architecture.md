# Architecture: Process Equipment Selection Assistant

## 1. System Purpose

This project is a local-first engineering workflow prototype for preliminary process equipment selection.

The demo case is the scale-up of a lab-scale hydrothermal synthesis process for MnO2 nanoparticle powder used as a battery cathode component.

The system takes structured lab-scale process information and mock engineering databases as input, then produces a preliminary equipment recommendation report.

The MVP is not a certified process design tool. It is a decision-support prototype that demonstrates how a process engineering workflow can be broken into modular reasoning steps.

## 2. MVP Scope

The first version is a local Python workflow.

It should run end-to-end from a sample JSON input file to output files without requiring real web search, real supplier APIs, ASPEN integration, Agentverse deployment, or external LLM calls.

The MVP focuses on:

- understanding the process brief
- generating a preliminary process basis
- decomposing the process into unit operations
- selecting equipment candidates from a mock database
- screening candidates using process constraints
- matching selected equipment to mock suppliers
- producing a readable report and RFQ-style draft

## 3. Input Files

The MVP uses three main data files.

### `data/sample_input.json`

This is the user-provided process brief for the demo case.

It contains:

- project goal
- target product
- lab-scale recipe
- hydrothermal reaction conditions
- post-reaction separation, washing, and drying steps
- target scale
- known process concerns
- equipment selection priorities
- preferred and avoided materials
- expected unit operations
- MVP constraints

This file should represent what a user might know at the beginning of an early process design task.

### `data/equipment_database.json`

This is a mock equipment knowledge base.

It contains candidate equipment options such as:

- precursor mixing vessels
- hydrothermal reactors
- solid-liquid separation equipment
- washing equipment
- drying equipment
- powder collection containers

Each equipment entry includes basic screening fields such as:

- equipment type
- suitable process steps
- phase suitability
- working volume range
- temperature range
- pressure range
- product-contact materials
- contamination control level
- cleanability
- pros, cons, and risk notes

### `data/supplier_database.json`

This is a mock supplier and CAPEX database.

It contains placeholder suppliers for the equipment categories in the demo.

Each supplier entry includes:

- supported equipment types
- example equipment
- estimated price range
- lead time
- strengths
- limitations
- RFQ notes

This data is for demonstration only and should not be used for real procurement.

## 4. Output Files

The MVP should produce two main output files.

### `outputs/sample_output.json`

A structured machine-readable output containing:

- process basis
- identified unit operations
- equipment candidates
- screening results
- final recommended equipment
- matched mock suppliers
- rough CAPEX range
- RFQ draft content

### `outputs/sample_report.md`

A human-readable report suitable for demo.

It should include:

- process summary
- key assumptions
- major unit operations
- recommended equipment table
- accepted and rejected equipment reasoning
- engineering concerns
- mock supplier matches
- rough CAPEX summary
- RFQ-style supplier inquiry draft
- limitations and next steps

## 5. Workflow Overview

The MVP follows this workflow:

```text
data/sample_input.json
  -> process_basis.py
  -> unit_decomposer.py
  -> equipment_selector.py
  -> engineering_reviewer.py
  -> supplier_matcher.py
  -> rfq_generator.py
  -> outputs/sample_output.json
  -> outputs/sample_report.md
```

## 6. Module Responsibilities

### `main.py`

The workflow entry point.

Responsibilities:

1. Load input data.
2. Load equipment and supplier databases.
3. Call each module in order.
4. Store intermediate results in a structured dictionary.
5. Save final JSON output.
6. Save final Markdown report.

`main.py` should stay simple. It should orchestrate the workflow, not contain all engineering logic.

### `src/process_basis.py`

Generates a preliminary process basis from the user-provided process brief.

Responsibilities:

- identify target product and application
- extract lab-scale reaction conditions
- extract target scale
- estimate simple scale-up factor
- summarize key operating conditions
- summarize process priorities
- identify missing or uncertain data

This module should not pretend to perform full process simulation.

### `src/unit_decomposer.py`

Breaks the process into major unit operations.

For the MnO2 hydrothermal demo, expected unit operations include:

- precursor solution preparation
- heated mixing
- hydrothermal batch reaction
- controlled cooling and safe depressurization
- solid-liquid separation
- washing to neutral pH
- vacuum drying
- powder collection

Responsibilities:

- create structured unit operation objects
- assign each unit a unit type
- assign each unit relevant operating constraints
- connect each unit to process concerns

### `src/equipment_selector.py`

Selects candidate equipment from the mock equipment database.

Responsibilities:

- match unit operations to equipment categories
- filter candidates by process step
- check rough working volume range
- check temperature range
- check pressure range
- check phase suitability
- return candidate equipment lists for each unit operation

This module performs preliminary candidate search, not final recommendation.

### `src/engineering_reviewer.py`

Screens and ranks equipment candidates using engineering constraints.

Responsibilities:

- evaluate pressure suitability
- evaluate temperature suitability
- evaluate contamination control
- evaluate material compatibility
- evaluate suitability for fine MnO2 particle handling
- explain accepted candidates
- explain rejected candidates
- flag unresolved risks and missing data

This module should prioritize transparent reasoning over complex scoring.

### `src/supplier_matcher.py`

Matches recommended equipment to mock suppliers.

Responsibilities:

- find suppliers that support the recommended equipment types
- attach mock price ranges
- attach mock lead times
- summarize supplier strengths and limitations
- calculate a rough total CAPEX range from selected supplier options

This module should use only `data/supplier_database.json` in the MVP.

### `src/rfq_generator.py`

Generates an RFQ-style draft for supplier communication.

Responsibilities:

- summarize requested equipment
- include key operating conditions
- include product-contact material requirements
- ask for pressure and temperature ratings
- ask for contamination control information
- ask for cleaning, validation, and lead time details
- produce text that can be placed in the final report

The RFQ should not actually send emails or contact suppliers.

## 7. Data Flow

The system should pass structured dictionaries between modules.

Recommended intermediate objects:

### Process Basis

Contains:

- product summary
- lab-scale basis
- target-scale basis
- scale-up factor
- operating condition summary
- quality and contamination priorities
- known risks
- missing data

### Unit Operation List

Contains one object per unit operation:

- unit id
- unit name
- unit type
- process step
- phase
- volume or capacity requirement
- temperature requirement
- pressure requirement
- material concerns
- contamination concerns

### Equipment Candidate List

Contains candidate equipment for each unit operation:

- unit id
- equipment id
- equipment name
- equipment type
- matched fields
- initial fit notes

### Engineering Review Result

Contains:

- accepted candidates
- rejected candidates
- rejection reasons
- recommendation rationale
- unresolved risks

### Supplier Match Result

Contains:

- selected equipment
- supplier options
- mock price range
- mock lead time
- RFQ notes

## 8. Design Principles

The MVP should be:

- local-first
- deterministic
- modular
- readable
- beginner-friendly
- easy to debug
- easy to later wrap into an agent

Avoid:

- hidden external API dependencies
- real procurement behavior
- overcomplicated agent orchestration too early
- unsupported engineering claims
- scope expansion beyond the MnO2 demo case

## 9. Engineering Assumptions

The MVP assumes:

- the input is already structured as JSON
- equipment matching is rule-based and database-driven
- supplier matching uses mock data
- CAPEX ranges are illustrative only
- the output is preliminary and requires professional review

Important limitations:

- no ASPEN simulation
- no rigorous heat and mass balance
- no pressure vessel design calculation
- no particle size prediction
- no battery performance prediction
- no real supplier validation

## 10. Future Agent Architecture

After the local MVP works, the workflow can be wrapped into Fetch.ai/uAgents.

Possible future architecture:

### Coordinator Agent

Receives the user request through ASI:One or another chat interface.

Responsibilities:

- parse the user request
- call the local workflow
- return the report
- ask follow-up questions if required data is missing

### Equipment Specialist Agents

Possible specialist agents:

- Hydrothermal Reactor Specialist
- Solid-Liquid Separation Specialist
- Drying Equipment Specialist
- Supplier Matching Specialist

These agents can be added later if the local MVP is stable.

### Agentverse / ASI:One Integration

Later work may include:

- registering the coordinator agent on Agentverse
- making it ASI:One compatible
- adding an Agentverse profile
- creating an ASI:One shared chat demo
- optionally splitting equipment selection into multiple specialist agents

This should come after the local MVP works.

## 11. Build Order

Recommended development order:

1. Confirm data files exist.
2. Implement `main.py` with placeholder workflow.
3. Implement `process_basis.py`.
4. Implement `unit_decomposer.py`.
5. Implement `equipment_selector.py`.
6. Implement `engineering_reviewer.py`.
7. Implement `supplier_matcher.py`.
8. Implement `rfq_generator.py`.
9. Generate `outputs/sample_output.json`.
10. Generate `outputs/sample_report.md`.
11. Improve README.
12. Commit to Git.
13. Later wrap into uAgents if time allows.

## 12. Definition of Done for Local MVP

The local MVP is done when this command works:

```bash
python main.py --input data/sample_input.json
```

And produces:

```text
outputs/sample_output.json
outputs/sample_report.md
```

The report should clearly explain:

- what the process is
- what units are required
- what equipment is recommended
- why the equipment is recommended
- what risks remain
- what mock suppliers could be contacted
- what the RFQ draft would ask for
