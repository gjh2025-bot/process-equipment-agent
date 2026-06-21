"""
main.py

Entry point for the Process Equipment Selection Assistant local MVP.
"""

import argparse
import json
import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from process_basis import build_process_basis
from unit_decomposer import decompose_process
from equipment_selector import select_equipment
from engineering_reviewer import review_candidates
from supplier_matcher import match_suppliers
from rfq_generator import generate_rfq


EQUIPMENT_DB_PATH = os.path.join("data", "equipment_database.json")
SUPPLIER_DB_PATH = os.path.join("data", "supplier_database.json")
OUTPUT_DIR = "outputs"
OUTPUT_JSON_PATH = os.path.join(OUTPUT_DIR, "sample_output.json")
OUTPUT_REPORT_PATH = os.path.join(OUTPUT_DIR, "sample_report.md")


def load_json(path):
    """Load JSON from a UTF-8 file."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def run_workflow(input_path):
    """Run the full local MVP workflow."""
    process_input = load_json(input_path)
    equipment_database = load_json(EQUIPMENT_DB_PATH)
    supplier_database = load_json(SUPPLIER_DB_PATH)

    process_basis = build_process_basis(process_input)
    units = decompose_process(process_input, process_basis)
    selection_results = select_equipment(units, equipment_database)
    reviews = review_candidates(selection_results, process_basis)
    supplier_result = match_suppliers(reviews, supplier_database)
    rfq = generate_rfq(reviews, supplier_result, process_basis)

    return {
        "project_name": process_input.get("project_name"),
        "process_goal": process_input.get("process_goal"),
        "process_basis": process_basis,
        "unit_operations": units,
        "equipment_review": reviews,
        "supplier_matching": supplier_result,
        "rfq_draft": rfq,
        "disclaimer": (
            "Preliminary decision-support output generated with mock data. "
            "Not a certified engineering design. Requires review by a "
            "qualified process engineer before any procurement."
        ),
    }


def save_json_output(result, path):
    """Write the structured result to a readable JSON file."""
    cleaned = _strip_equipment_records(result)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(cleaned, handle, indent=2, ensure_ascii=False)


def _strip_equipment_records(result):
    """Remove bulky carried equipment records from the saved JSON output."""
    copied = json.loads(json.dumps(result, ensure_ascii=False))

    for review in copied.get("equipment_review", []):
        for key in ("accepted_candidates", "rejected_candidates"):
            for candidate in review.get(key, []):
                candidate.pop("equipment_record", None)
        recommended = review.get("recommended_equipment")
        if recommended:
            recommended.pop("equipment_record", None)

    return copied


def save_markdown_report(result, path):
    """Write a human-readable Markdown report."""
    lines = []
    add = lines.append

    basis = result["process_basis"]
    product = basis["product_summary"]

    add("# Preliminary Equipment Selection Report")
    add("")
    add("**Project:** {}".format(result.get("project_name", "N/A")))
    add("")
    add("**Goal:** {}".format(result.get("process_goal", "N/A")))
    add("")
    add("> {}".format(result["disclaimer"]))
    add("")

    add("## 1. Process Summary")
    add("")
    add("- **Target product:** {}".format(product.get("name")))
    add("- **Intended application:** {}".format(product.get("intended_application")))
    add("- **Scale-up factor:** {}".format(basis.get("scale_up_factor")))
    add(
        "- **Target batch volume:** {} L".format(
            basis["target_scale_basis"].get("target_batch_liquid_volume_l")
        )
    )
    add("")
    add("**Critical quality attributes:**")
    add("")
    for attribute in product.get("critical_quality_attributes", []):
        add("- {}".format(attribute))
    add("")

    add("## 2. Key Assumptions and Missing Data")
    add("")
    for note in basis.get("missing_or_uncertain_data", []):
        add("- {}".format(note))
    add("")

    add("## 3. Major Unit Operations")
    add("")
    add("| ID | Unit Operation | Type | Temp (C) | Pressure (bar) | Volume (L) |")
    add("| --- | --- | --- | --- | --- | --- |")
    for unit in result["unit_operations"]:
        add(
            "| {} | {} | {} | {} | {} | {} |".format(
                unit["unit_id"],
                unit["unit_name"],
                unit["unit_type"],
                unit["temperature_c"],
                unit["pressure_bar"],
                unit["required_volume_l"],
            )
        )
    add("")

    add("## 4. Recommended Equipment")
    add("")
    add("| Unit | Recommended Equipment | Type | Contamination Control |")
    add("| --- | --- | --- | --- |")
    for review in result["equipment_review"]:
        rec = review["recommended_equipment"]
        if rec:
            add(
                "| {} | {} | {} | {} |".format(
                    review["unit_name"],
                    rec["equipment_name"],
                    rec["equipment_type"],
                    rec.get("contamination_control_level", "n/a"),
                )
            )
        else:
            add("| {} | _No suitable equipment accepted_ | - | - |".format(review["unit_name"]))
    add("")

    add("## 5. Screening Reasoning")
    add("")
    for review in result["equipment_review"]:
        add("### {} ({})".format(review["unit_name"], review["unit_id"]))
        add("")
        add("**Accepted candidates:**")
        add("")
        if review["accepted_candidates"]:
            for candidate in review["accepted_candidates"]:
                add("- **{}** ({})".format(candidate["equipment_name"], candidate["equipment_id"]))
                for reason in candidate["reasons"]:
                    add("  - {}".format(reason))
        else:
            add("- None")
        add("")
        add("**Rejected candidates:**")
        add("")
        if review["rejected_candidates"]:
            for candidate in review["rejected_candidates"]:
                add("- **{}** ({})".format(candidate["equipment_name"], candidate["equipment_id"]))
                for reason in candidate["reasons"]:
                    add("  - {}".format(reason))
        else:
            add("- None")
        add("")
        add("**Unresolved risks:**")
        add("")
        for risk in review["unresolved_risks"]:
            add("- {}".format(risk))
        add("")

    add("## 6. Mock Supplier Matches")
    add("")
    for match in result["supplier_matching"]["unit_supplier_matches"]:
        rec = match["recommended_equipment"]
        if not rec:
            continue
        add("### {} -> {}".format(match["unit_name"], rec["equipment_name"]))
        add("")
        if match["suppliers"]:
            add("| Supplier | Example Equipment | Price (USD) | Lead Time (weeks) |")
            add("| --- | --- | --- | --- |")
            for supplier in match["suppliers"]:
                add(
                    "| {} | {} | {} | {} |".format(
                        supplier["supplier_name"],
                        supplier.get("example_equipment", "n/a"),
                        _range_text(supplier.get("estimated_price_range_usd")),
                        _range_text(supplier.get("typical_lead_time_weeks")),
                    )
                )
        else:
            add("_No matching mock suppliers found._")
        add("")

    capex = result["supplier_matching"]["capex_summary"]
    add("## 7. Rough CAPEX Summary")
    add("")
    total = capex.get("rough_total_capex_usd")
    if total:
        add("**Rough total CAPEX range:** ${:,} - ${:,} USD".format(total[0], total[1]))
    else:
        add("**Rough total CAPEX range:** not available")
    add("")
    add("> {}".format(capex.get("note", "")))
    add("")

    rfq = result["rfq_draft"]
    add("## 8. RFQ-Style Supplier Inquiry Draft")
    add("")
    add(rfq["intro"])
    add("")
    for index, item in enumerate(rfq["items"], start=1):
        add("### RFQ Item {}: {}".format(index, item["equipment_type"]))
        add("")
        add("- **For unit:** {}".format(item["for_unit"]))
        add("- **Example equipment:** {}".format(item["equipment_example"]))
        add("- **Operating conditions:**")
        for condition in item["operating_conditions"]:
            add("  - {}".format(condition))
        add(
            "- **Preferred contact materials:** {}".format(
                ", ".join(item["preferred_contact_materials"]) or "n/a"
            )
        )
        add(
            "- **Materials to avoid:** {}".format(
                ", ".join(item["materials_to_avoid"]) or "n/a"
            )
        )
        add("- **Questions for supplier:**")
        for question in item["questions_for_supplier"]:
            add("  - {}".format(question))
        add("- **Candidate suppliers:** {}".format(", ".join(item["candidate_suppliers"]) or "n/a"))
        add("")
    add(rfq["closing"])
    add("")

    add("## 9. Limitations and Next Steps")
    add("")
    add("- This report is preliminary and uses mock equipment and supplier data.")
    add("- No process simulation, heat/mass balance, or vessel design was performed.")
    add("- Pressure, temperature, and material compatibility must be confirmed with suppliers.")
    add("- A qualified process engineer must review all selections before procurement.")
    add("")

    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def _range_text(range_pair):
    """Format a [low, high] pair for the report."""
    if range_pair and len(range_pair) == 2:
        return "{} - {}".format(range_pair[0], range_pair[1])
    return "n/a"


def main():
    parser = argparse.ArgumentParser(
        description="Process Equipment Selection Assistant local MVP."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the process input JSON, e.g. data/sample_input.json.",
    )
    args = parser.parse_args()

    result = run_workflow(args.input)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_json_output(result, OUTPUT_JSON_PATH)
    save_markdown_report(result, OUTPUT_REPORT_PATH)

    print("Workflow complete.")
    print("  - {}".format(OUTPUT_JSON_PATH))
    print("  - {}".format(OUTPUT_REPORT_PATH))


if __name__ == "__main__":
    main()
