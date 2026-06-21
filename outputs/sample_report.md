# Preliminary Equipment Selection Report

**Project:** Pilot-scale MnO2 nanoparticle production for battery cathode components

**Goal:** Scale up a lab-scale hydrothermal synthesis of MnO2 nanostructures into a small pilot-scale batch process and recommend preliminary equipment.

> Preliminary decision-support output generated with mock data. Not a certified engineering design. Requires review by a qualified process engineer before any procurement.

## 1. Process Summary

- **Target product:** MnO2 nanoparticle powder
- **Intended application:** aqueous zinc-ion battery cathode component
- **Scale-up factor:** 50
- **Target batch volume:** 2 L

**Critical quality attributes:**

- controlled nanoscale particle size or grain size
- consistent MnO2 phase and crystallinity
- low residual soluble ionic contamination
- low unwanted metallic contamination from equipment
- reproducible batch quality

## 2. Key Assumptions and Missing Data

- Hydrothermal operating pressure is autogenous and given as a condition, not a confirmed numeric value. Design pressure at the hold temperature must be verified.
- Particle size, yield, and morphology after scale-up are not predicted by this tool and require experimental confirmation.

## 3. Major Unit Operations

| ID | Unit Operation | Type | Temp (C) | Pressure (bar) | Volume (L) |
| --- | --- | --- | --- | --- | --- |
| U-01 | Precursor solution preparation | precursor_mixing | 25 | 1 | 2 |
| U-02 | Heated mixing | precursor_mixing | 60 | 1 | 2 |
| U-03 | Hydrothermal batch reaction | hydrothermal_reactor | 180 | 10 | 2 |
| U-04 | Controlled cooling and safe depressurization | hydrothermal_reactor | 180 | 10 | 2 |
| U-05 | Solid-liquid separation | solid_liquid_separation | 25 | 1 | 2 |
| U-06 | Washing to neutral pH | washing | 25 | 1 | 2 |
| U-07 | Vacuum drying | drying | 80 | 0.1 | 2 |
| U-08 | Powder collection | powder_collection | 25 | 1 | 2 |

## 4. Recommended Equipment

| Unit | Recommended Equipment | Type | Contamination Control |
| --- | --- | --- | --- |
| Precursor solution preparation | Jacketed glass mixing vessel | precursor_mixing | high |
| Heated mixing | Jacketed glass mixing vessel | precursor_mixing | high |
| Hydrothermal batch reaction | Teflon-lined stainless steel batch autoclave | hydrothermal_reactor | high |
| Controlled cooling and safe depressurization | Teflon-lined stainless steel batch autoclave | hydrothermal_reactor | high |
| Solid-liquid separation | Lab or pilot vacuum filtration setup | solid_liquid_separation | high |
| Washing to neutral pH | Repeated DI water reslurry washing vessel | washing | high |
| Vacuum drying | Vacuum oven | drying | high |
| Powder collection | Clean powder collection container | powder_collection | high |

## 5. Screening Reasoning

### Precursor solution preparation (U-01)

**Accepted candidates:**

- **Jacketed glass mixing vessel** (MIX-001)
  - [OK] Temperature 25 C (equipment range 20-90 C).
  - [OK] Pressure 1 bar (equipment range 1-1 bar).
  - [OK] Required volume 2 L (equipment range 0.5-5 L).
- **316L stainless steel jacketed stirred tank** (MIX-002)
  - [OK] Temperature 25 C (equipment range 20-120 C).
  - [OK] Pressure 1 bar (equipment range 1-2 bar).
  - [OK] Required volume 2 L (equipment range 2-50 L).

**Rejected candidates:**

- None

**Unresolved risks:**

- Do not use for sealed hydrothermal operation.
- Only suitable before the pressure-rated reaction step.

### Heated mixing (U-02)

**Accepted candidates:**

- **Jacketed glass mixing vessel** (MIX-001)
  - [OK] Temperature 60 C (equipment range 20-90 C).
  - [OK] Pressure 1 bar (equipment range 1-1 bar).
  - [OK] Required volume 2 L (equipment range 0.5-5 L).
- **316L stainless steel jacketed stirred tank** (MIX-002)
  - [OK] Temperature 60 C (equipment range 20-120 C).
  - [OK] Pressure 1 bar (equipment range 1-2 bar).
  - [OK] Required volume 2 L (equipment range 2-50 L).
- **Open atmospheric stirred tank reactor** (RXN-003)
  - [OK] Temperature 60 C (equipment range 20-100 C).
  - [OK] Pressure 1 bar (equipment range 1-1 bar).
  - [OK] Required volume 2 L (equipment range 1-100 L).

**Rejected candidates:**

- None

**Unresolved risks:**

- Do not use for sealed hydrothermal operation.
- Only suitable before the pressure-rated reaction step.

### Hydrothermal batch reaction (U-03)

**Accepted candidates:**

- **Teflon-lined stainless steel batch autoclave** (RXN-001)
  - [OK] Temperature 180 C (equipment range 80-220 C).
  - [OK] Pressure 10 bar (equipment range 1-30 bar).
  - [OK] Required volume 2 L (equipment range 0.1-5 L).
- **Stirred pressure reactor with PTFE-lined wetted parts** (RXN-002)
  - [OK] Temperature 180 C (equipment range 80-250 C).
  - [OK] Pressure 10 bar (equipment range 1-50 bar).
  - [OK] Required volume 2 L (equipment range 1-20 L).

**Rejected candidates:**

- None

**Unresolved risks:**

- Pressure rating must be verified at 180 C with autogenous pressure.
- Do not overfill vessel.
- Thermal ramp and cooling profile may affect MnO2 morphology.

### Controlled cooling and safe depressurization (U-04)

**Accepted candidates:**

- **Teflon-lined stainless steel batch autoclave** (RXN-001)
  - [OK] Temperature 180 C (equipment range 80-220 C).
  - [OK] Pressure 10 bar (equipment range 1-30 bar).
  - [OK] Required volume 2 L (equipment range 0.1-5 L).
- **Stirred pressure reactor with PTFE-lined wetted parts** (RXN-002)
  - [OK] Temperature 180 C (equipment range 80-250 C).
  - [OK] Pressure 10 bar (equipment range 1-50 bar).
  - [OK] Required volume 2 L (equipment range 1-20 L).

**Rejected candidates:**

- None

**Unresolved risks:**

- Pressure rating must be verified at 180 C with autogenous pressure.
- Do not overfill vessel.
- Thermal ramp and cooling profile may affect MnO2 morphology.

### Solid-liquid separation (U-05)

**Accepted candidates:**

- **Pilot basket centrifuge** (SEP-002)
  - [OK] Temperature 25 C (equipment range 5-60 C).
  - [OK] Pressure 1 bar (equipment range 1-1 bar).
  - [OK] Required volume 2 L (equipment range 1-20 L).
- **Lab or pilot vacuum filtration setup** (SEP-003)
  - [OK] Temperature 25 C (equipment range 5-60 C).
  - [OK] Pressure 1 bar (equipment range 0.2-1 bar).
  - [OK] Required volume 2 L (equipment range 0.1-5 L).

**Rejected candidates:**

- **Bench-top centrifuge** (SEP-001)
  - [OK] Temperature 25 C (equipment range 5-40 C).
  - [OK] Pressure 1 bar (equipment range 1-1 bar).
  - [FAIL] Required volume 2 L (equipment range 0.01-1 L).
- **Agitated nutsche filter dryer** (SEP-004)
  - [OK] Temperature 25 C (equipment range 20-120 C).
  - [OK] Pressure 1 bar (equipment range 0.1-6 bar).
  - [FAIL] Required volume 2 L (equipment range 5-100 L).

**Unresolved risks:**

- Filter media pore size and cake permeability must be tested.
- May need pre-wetting or staged filtration.

### Washing to neutral pH (U-06)

**Accepted candidates:**

- **Repeated DI water reslurry washing vessel** (WASH-001)
  - [OK] Temperature 25 C (equipment range 20-60 C).
  - [OK] Pressure 1 bar (equipment range 1-1 bar).
  - [OK] Required volume 2 L (equipment range 0.5-10 L).

**Rejected candidates:**

- None

**Unresolved risks:**

- Conductivity and pH should be monitored to confirm washing completeness.
- Avoid product loss during repeated washing.

### Vacuum drying (U-07)

**Accepted candidates:**

- **Vacuum oven** (DRY-001)
  - [OK] Temperature 80 C (equipment range 30-120 C).
  - [OK] Pressure 0.1 bar (equipment range 0.001-1 bar).
  - [OK] Required volume 2 L (equipment range 0.1-10 L).

**Rejected candidates:**

- None

**Unresolved risks:**

- Drying temperature and time should be validated against MnO2 phase and hydration requirements.
- Avoid cross-contamination from previous powders.

### Powder collection (U-08)

**Accepted candidates:**

- **Clean powder collection container** (COL-001)
  - [OK] Temperature 25 C (equipment range 20-60 C).
  - [OK] Pressure 1 bar (equipment range 1-1 bar).
  - [OK] Required volume 2 L (equipment range 0.1-20 L).

**Rejected candidates:**

- None

**Unresolved risks:**

- Use clean, dedicated containers to avoid cross-contamination.
- Consider powder handling PPE and dust control.

## 6. Mock Supplier Matches

### Precursor solution preparation -> Jacketed glass mixing vessel

| Supplier | Example Equipment | Price (USD) | Lead Time (weeks) |
| --- | --- | --- | --- |
| BenchScale Process Glassware Co. | Jacketed glass mixing vessel, 1-5 L | 1500 - 8000 | 2 - 6 |
| PilotMix Systems | 316L stainless steel jacketed stirred tank, 5-50 L | 8000 - 35000 | 6 - 14 |

### Heated mixing -> Jacketed glass mixing vessel

| Supplier | Example Equipment | Price (USD) | Lead Time (weeks) |
| --- | --- | --- | --- |
| BenchScale Process Glassware Co. | Jacketed glass mixing vessel, 1-5 L | 1500 - 8000 | 2 - 6 |
| PilotMix Systems | 316L stainless steel jacketed stirred tank, 5-50 L | 8000 - 35000 | 6 - 14 |

### Hydrothermal batch reaction -> Teflon-lined stainless steel batch autoclave

| Supplier | Example Equipment | Price (USD) | Lead Time (weeks) |
| --- | --- | --- | --- |
| HydroTherm Lab Reactors | Teflon-lined stainless steel batch autoclave, 0.5-5 L | 5000 - 25000 | 4 - 10 |
| Pilot Pressure Reactor Solutions | Stirred pressure reactor with PTFE-lined wetted parts, 2-20 L | 30000 - 120000 | 10 - 24 |

### Controlled cooling and safe depressurization -> Teflon-lined stainless steel batch autoclave

| Supplier | Example Equipment | Price (USD) | Lead Time (weeks) |
| --- | --- | --- | --- |
| HydroTherm Lab Reactors | Teflon-lined stainless steel batch autoclave, 0.5-5 L | 5000 - 25000 | 4 - 10 |
| Pilot Pressure Reactor Solutions | Stirred pressure reactor with PTFE-lined wetted parts, 2-20 L | 30000 - 120000 | 10 - 24 |

### Solid-liquid separation -> Lab or pilot vacuum filtration setup

| Supplier | Example Equipment | Price (USD) | Lead Time (weeks) |
| --- | --- | --- | --- |
| CleanSolid Separation Tools | Lab or pilot vacuum filtration setup with ceramic or PTFE-compatible media | 1000 - 12000 | 2 - 8 |
| PilotCentrifuge Equipment Group | Pilot basket centrifuge for fine slurry separation, 1-20 L | 15000 - 80000 | 8 - 20 |

### Washing to neutral pH -> Repeated DI water reslurry washing vessel

| Supplier | Example Equipment | Price (USD) | Lead Time (weeks) |
| --- | --- | --- | --- |
| CleanSolid Separation Tools | Lab or pilot vacuum filtration setup with ceramic or PTFE-compatible media | 1000 - 12000 | 2 - 8 |

### Vacuum drying -> Vacuum oven

| Supplier | Example Equipment | Price (USD) | Lead Time (weeks) |
| --- | --- | --- | --- |
| VacuumDry Bench Systems | Vacuum oven for battery material powder drying, 30-120 C | 3000 - 20000 | 2 - 8 |
| PilotSolids Drying Systems | Small tray dryer or convection oven for pilot powder drying | 5000 - 30000 | 4 - 12 |

### Powder collection -> Clean powder collection container

| Supplier | Example Equipment | Price (USD) | Lead Time (weeks) |
| --- | --- | --- | --- |
| CleanPowder Handling Supplies | Clean HDPE, polypropylene, or glass powder collection containers | 50 - 1000 | 1 - 4 |

## 7. Rough CAPEX Summary

**Rough total CAPEX range:** $11,550 - $278,000 USD

> Illustrative mock CAPEX only. Each distinct recommended equipment item is counted once (equipment shared across steps is not double-counted). Totals use the lowest and highest mock supplier prices. Not a quote.

## 8. RFQ-Style Supplier Inquiry Draft

Request for preliminary quotation for pilot-scale equipment supporting the production of MnO2 nanoparticle powder for aqueous zinc-ion battery cathode component. Target batch size is 2 L in bench-pilot batch operation. This is an early-stage inquiry for budgetary purposes only.

### RFQ Item 1: precursor_mixing

- **For unit:** Precursor solution preparation
- **Example equipment:** Jacketed glass mixing vessel
- **Operating conditions:**
  - Operating temperature is 25 C, so the equipment must be rated to cover this point with margin (recommended example is rated 20 to 90 C).
  - Operating pressure is about 1 bar, so the equipment must be rated to cover this with adequate relief (recommended example is rated 1 to 1 bar).
  - Batch volume is 2 L, so the working volume must accommodate this (recommended example handles 0.5 to 5 L).
- **Preferred contact materials:** PTFE-lined contact surfaces, 316L stainless steel external pressure-rated body, glass-lined steel if compatible, ceramic or polymeric filter media with low contamination risk
- **Materials to avoid:** unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces
- **Questions for supplier:**
  - What product-contact materials are available, and can they avoid: unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces?
  - Can the equipment meet the operating conditions listed above with an adequate safety margin?
  - What contamination control, cleaning, and validation options are supported?
  - What is the budgetary price and typical lead time?
  - (BenchScale Process Glassware Co.) Ask for working volume, jacket temperature range, stirrer material, and product-contact material certification.
  - (PilotMix Systems) Ask about surface finish, passivation, cleanability, and compatibility with acidic manganese-containing aqueous slurry.
- **Candidate suppliers:** BenchScale Process Glassware Co., PilotMix Systems

### RFQ Item 2: hydrothermal_reactor

- **For unit:** Hydrothermal batch reaction
- **Example equipment:** Teflon-lined stainless steel batch autoclave
- **Operating conditions:**
  - Operating temperature is 180 C, so the equipment must be rated to cover this point with margin (recommended example is rated 80 to 220 C).
  - Operating pressure is about 10 bar, so the equipment must be rated to cover this with adequate relief (recommended example is rated 1 to 30 bar).
  - Batch volume is 2 L, so the working volume must accommodate this (recommended example handles 0.1 to 5 L).
- **Preferred contact materials:** PTFE-lined contact surfaces, 316L stainless steel external pressure-rated body, glass-lined steel if compatible, ceramic or polymeric filter media with low contamination risk
- **Materials to avoid:** unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces
- **Questions for supplier:**
  - What product-contact materials are available, and can they avoid: unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces?
  - Can the equipment meet the operating conditions listed above with an adequate safety margin?
  - What contamination control, cleaning, and validation options are supported?
  - What is the budgetary price and typical lead time?
  - (HydroTherm Lab Reactors) Ask for certified pressure rating at 180 C, maximum fill fraction, liner material, pressure relief options, and temperature control method.
  - (Pilot Pressure Reactor Solutions) Ask for wetted material options, seal design, agitation range, pressure relief system, data logging, and batch reproducibility features.
- **Candidate suppliers:** HydroTherm Lab Reactors, Pilot Pressure Reactor Solutions

### RFQ Item 3: solid_liquid_separation

- **For unit:** Solid-liquid separation
- **Example equipment:** Lab or pilot vacuum filtration setup
- **Operating conditions:**
  - Operating temperature is 25 C, so the equipment must be rated to cover this point with margin (recommended example is rated 5 to 60 C).
  - Operating pressure is about 1 bar, so the equipment must be rated to cover this with adequate relief (recommended example is rated 0.2 to 1 bar).
  - Batch volume is 2 L, so the working volume must accommodate this (recommended example handles 0.1 to 5 L).
- **Preferred contact materials:** PTFE-lined contact surfaces, 316L stainless steel external pressure-rated body, glass-lined steel if compatible, ceramic or polymeric filter media with low contamination risk
- **Materials to avoid:** unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces
- **Questions for supplier:**
  - What product-contact materials are available, and can they avoid: unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces?
  - Can the equipment meet the operating conditions listed above with an adequate safety margin?
  - What contamination control, cleaning, and validation options are supported?
  - What is the budgetary price and typical lead time?
  - (CleanSolid Separation Tools) Ask for filter media pore size, chemical compatibility, hold-up volume, cake washing options, and expected filtration area.
  - (PilotCentrifuge Equipment Group) Ask for bowl material, liner options, minimum particle retention, cleaning procedure, and compatibility with MnO2 nanoparticle slurry.
- **Candidate suppliers:** CleanSolid Separation Tools, PilotCentrifuge Equipment Group

### RFQ Item 4: washing

- **For unit:** Washing to neutral pH
- **Example equipment:** Repeated DI water reslurry washing vessel
- **Operating conditions:**
  - Operating temperature is 25 C, so the equipment must be rated to cover this point with margin (recommended example is rated 20 to 60 C).
  - Operating pressure is about 1 bar, so the equipment must be rated to cover this with adequate relief (recommended example is rated 1 to 1 bar).
  - Batch volume is 2 L, so the working volume must accommodate this (recommended example handles 0.5 to 10 L).
- **Preferred contact materials:** PTFE-lined contact surfaces, 316L stainless steel external pressure-rated body, glass-lined steel if compatible, ceramic or polymeric filter media with low contamination risk
- **Materials to avoid:** unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces
- **Questions for supplier:**
  - What product-contact materials are available, and can they avoid: unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces?
  - Can the equipment meet the operating conditions listed above with an adequate safety margin?
  - What contamination control, cleaning, and validation options are supported?
  - What is the budgetary price and typical lead time?
  - (CleanSolid Separation Tools) Ask for filter media pore size, chemical compatibility, hold-up volume, cake washing options, and expected filtration area.
- **Candidate suppliers:** CleanSolid Separation Tools

### RFQ Item 5: drying

- **For unit:** Vacuum drying
- **Example equipment:** Vacuum oven
- **Operating conditions:**
  - Operating temperature is 80 C, so the equipment must be rated to cover this point with margin (recommended example is rated 30 to 120 C).
  - Operating pressure is about 0.1 bar, so the equipment must be rated to cover this with adequate relief (recommended example is rated 0.001 to 1 bar).
  - Batch volume is 2 L, so the working volume must accommodate this (recommended example handles 0.1 to 10 L).
- **Preferred contact materials:** PTFE-lined contact surfaces, 316L stainless steel external pressure-rated body, glass-lined steel if compatible, ceramic or polymeric filter media with low contamination risk
- **Materials to avoid:** unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces
- **Questions for supplier:**
  - What product-contact materials are available, and can they avoid: unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces?
  - Can the equipment meet the operating conditions listed above with an adequate safety margin?
  - What contamination control, cleaning, and validation options are supported?
  - What is the budgetary price and typical lead time?
  - (VacuumDry Bench Systems) Ask for chamber material, shelf temperature uniformity, vacuum range, tray material, and contamination control features.
  - (PilotSolids Drying Systems) Ask for temperature uniformity, HEPA filtration options, tray material, and cleaning protocol.
- **Candidate suppliers:** VacuumDry Bench Systems, PilotSolids Drying Systems

### RFQ Item 6: powder_collection

- **For unit:** Powder collection
- **Example equipment:** Clean powder collection container
- **Operating conditions:**
  - Operating temperature is 25 C, so the equipment must be rated to cover this point with margin (recommended example is rated 20 to 60 C).
  - Operating pressure is about 1 bar, so the equipment must be rated to cover this with adequate relief (recommended example is rated 1 to 1 bar).
  - Batch volume is 2 L, so the working volume must accommodate this (recommended example handles 0.1 to 20 L).
- **Preferred contact materials:** PTFE-lined contact surfaces, 316L stainless steel external pressure-rated body, glass-lined steel if compatible, ceramic or polymeric filter media with low contamination risk
- **Materials to avoid:** unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces
- **Questions for supplier:**
  - What product-contact materials are available, and can they avoid: unlined carbon steel in product-contact areas, materials that may leach unwanted transition metals, porous or difficult-to-clean product-contact surfaces?
  - Can the equipment meet the operating conditions listed above with an adequate safety margin?
  - What contamination control, cleaning, and validation options are supported?
  - What is the budgetary price and typical lead time?
  - (CleanPowder Handling Supplies) Ask for cleanroom packaging, material certification, container volume, and antistatic options.
- **Candidate suppliers:** CleanPowder Handling Supplies

Please provide budgetary pricing, lead time, product-contact material options, and relevant certifications. All values will be treated as preliminary and subject to engineering review.

## 9. Limitations and Next Steps

- This report is preliminary and uses mock equipment and supplier data.
- No process simulation, heat/mass balance, or vessel design was performed.
- Pressure, temperature, and material compatibility must be confirmed with suppliers.
- A qualified process engineer must review all selections before procurement.
