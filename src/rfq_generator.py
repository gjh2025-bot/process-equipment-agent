"""
rfq_generator.py

Generate an RFQ-style (Request For Quote) draft for the recommended equipment.

This module only builds text. It never sends emails or contacts suppliers.
The draft is meant to be pasted into the final report so a human can review
and send it themselves.
"""


def generate_rfq(reviews, supplier_result, process_basis):
    """Build an RFQ draft covering every recommended equipment item.

    Args:
        reviews: output of engineering_reviewer.review_candidates.
        supplier_result: output of supplier_matcher.match_suppliers.
        process_basis: output of process_basis.build_process_basis.

    Returns:
        dict with a short intro, one RFQ item per recommended equipment, and a
        closing note.
    """
    product = process_basis["product_summary"]
    target = process_basis["target_scale_basis"]
    preferred_materials = process_basis.get("preferred_materials", [])
    avoid_materials = process_basis.get("avoid_materials", [])

    # Index supplier matches by unit id so we can attach supplier names.
    suppliers_by_unit = {
        m["unit_id"]: m for m in supplier_result["unit_supplier_matches"]
    }

    intro = (
        "Request for preliminary quotation for pilot-scale equipment supporting "
        "the production of {product} for {application}. Target batch size is "
        "{volume} L in {mode} batch operation. This is an early-stage inquiry "
        "for budgetary purposes only.".format(
            product=product.get("name", "the target product"),
            application=product.get("intended_application", "the intended application"),
            volume=target.get("target_batch_liquid_volume_l", "TBD"),
            mode=target.get("mode", "pilot"),
        )
    )

    # Build one RFQ item per distinct recommended equipment item, so a shared
    # unit is not requested twice.
    items = []
    seen_equipment_ids = set()
    for review in reviews:
        recommended = review["recommended_equipment"]
        if not recommended:
            continue
        equipment_id = recommended["equipment_id"]
        if equipment_id in seen_equipment_ids:
            continue
        seen_equipment_ids.add(equipment_id)

        items.append(
            _build_item(
                review,
                recommended,
                suppliers_by_unit.get(review["unit_id"], {}),
                preferred_materials,
                avoid_materials,
            )
        )

    closing = (
        "Please provide budgetary pricing, lead time, product-contact material "
        "options, and relevant certifications. All values will be treated as "
        "preliminary and subject to engineering review."
    )

    return {"intro": intro, "items": items, "closing": closing}


def _build_item(review, recommended, supplier_match, preferred_materials, avoid_materials):
    """Build a single RFQ item for one recommended equipment piece."""
    equipment = recommended["equipment_record"]

    # State the ACTUAL operating point first, then explain that the equipment's
    # rated range must cover that point (with margin). This reads the way an
    # engineer would actually write an RFQ.
    operating_conditions = [
        "Operating temperature is {} C, so the equipment must be rated to "
        "cover this point with margin (recommended example is rated "
        "{} C).".format(
            review.get("operating_temperature_c", "TBD"),
            _range_text(equipment.get("temperature_c_range")),
        ),
        "Operating pressure is about {} bar, so the equipment must be rated "
        "to cover this with adequate relief (recommended example is rated "
        "{} bar).".format(
            review.get("operating_pressure_bar", "TBD"),
            _range_text(equipment.get("pressure_bar_range")),
        ),
        "Batch volume is {} L, so the working volume must accommodate this "
        "(recommended example handles {} L).".format(
            review.get("required_volume_l", "TBD"),
            _range_text(equipment.get("working_volume_l_range")),
        ),
    ]

    # Standard questions every supplier should answer, plus any RFQ notes the
    # mock supplier database already provided.
    questions = [
        "What product-contact materials are available, and can they avoid: "
        + ", ".join(avoid_materials)
        + "?",
        "Can the equipment meet the operating conditions listed above with an "
        "adequate safety margin?",
        "What contamination control, cleaning, and validation options are "
        "supported?",
        "What is the budgetary price and typical lead time?",
    ]
    for supplier in supplier_match.get("suppliers", []):
        for note in supplier.get("rfq_notes", []):
            questions.append("({}) {}".format(supplier["supplier_name"], note))

    supplier_names = [
        s["supplier_name"] for s in supplier_match.get("suppliers", [])
    ]

    return {
        "for_unit": review["unit_name"],
        "equipment_type": recommended["equipment_type"],
        "equipment_example": recommended["equipment_name"],
        "operating_conditions": operating_conditions,
        "preferred_contact_materials": preferred_materials,
        "materials_to_avoid": avoid_materials,
        "questions_for_supplier": questions,
        "candidate_suppliers": supplier_names,
    }


def _range_text(range_pair):
    """Format a [low, high] pair, or note that it is unspecified."""
    if range_pair and len(range_pair) == 2:
        return "{} to {}".format(range_pair[0], range_pair[1])
    return "to be specified"
