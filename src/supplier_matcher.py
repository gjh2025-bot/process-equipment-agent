"""
supplier_matcher.py

Match each recommended piece of equipment to mock suppliers and build a rough
CAPEX estimate.

Matching is by equipment_type: a supplier is a match if the recommended
equipment's type is listed in the supplier's "equipment_types_supported".
All prices and lead times are illustrative mock data from
data/supplier_database.json and must not be used for real procurement.
"""


def match_suppliers(reviews, supplier_database):
    """Match recommended equipment to suppliers and total a rough CAPEX range.

    Args:
        reviews: output of engineering_reviewer.review_candidates.
        supplier_database: parsed data/supplier_database.json.

    Returns:
        dict with per-unit supplier matches and an overall CAPEX summary.
    """
    all_suppliers = supplier_database.get("suppliers", [])

    matches = []
    capex_low_total = 0
    capex_high_total = 0
    have_any_price = False
    # Track equipment already counted, so one physical unit shared by several
    # process steps (e.g. the reactor used for both reaction and cooling) is
    # not double-counted in the total CAPEX.
    counted_equipment_ids = set()

    for review in reviews:
        recommended = review["recommended_equipment"]

        if not recommended:
            matches.append(
                {
                    "unit_id": review["unit_id"],
                    "unit_name": review["unit_name"],
                    "recommended_equipment": None,
                    "suppliers": [],
                    "unit_capex_range_usd": None,
                }
            )
            continue

        equipment_type = recommended["equipment_type"]
        suppliers = _find_suppliers(equipment_type, all_suppliers)

        # Use the lowest min price and highest max price across the matched
        # suppliers as this unit's rough CAPEX range.
        unit_range = _unit_capex_range(suppliers)
        # Only add to the total the first time we see a given equipment id, so
        # equipment shared across steps is counted once.
        if unit_range and recommended["equipment_id"] not in counted_equipment_ids:
            counted_equipment_ids.add(recommended["equipment_id"])
            capex_low_total += unit_range[0]
            capex_high_total += unit_range[1]
            have_any_price = True

        matches.append(
            {
                "unit_id": review["unit_id"],
                "unit_name": review["unit_name"],
                "recommended_equipment": {
                    "equipment_id": recommended["equipment_id"],
                    "equipment_name": recommended["equipment_name"],
                    "equipment_type": equipment_type,
                },
                "suppliers": suppliers,
                "unit_capex_range_usd": unit_range,
            }
        )

    capex_summary = {
        "rough_total_capex_usd": [capex_low_total, capex_high_total]
        if have_any_price
        else None,
        "note": (
            "Illustrative mock CAPEX only. Each distinct recommended equipment "
            "item is counted once (equipment shared across steps is not "
            "double-counted). Totals use the lowest and highest mock supplier "
            "prices. Not a quote."
        ),
    }

    return {"unit_supplier_matches": matches, "capex_summary": capex_summary}


def _find_suppliers(equipment_type, all_suppliers):
    """Return supplier records that support the given equipment type."""
    found = []
    for supplier in all_suppliers:
        if equipment_type in supplier.get("equipment_types_supported", []):
            found.append(
                {
                    "supplier_id": supplier["supplier_id"],
                    "supplier_name": supplier["supplier_name"],
                    "example_equipment": supplier.get("example_equipment"),
                    "location": supplier.get("location"),
                    "estimated_price_range_usd": supplier.get(
                        "estimated_price_range_usd"
                    ),
                    "typical_lead_time_weeks": supplier.get(
                        "typical_lead_time_weeks"
                    ),
                    "strengths": supplier.get("strengths", []),
                    "limitations": supplier.get("limitations", []),
                    "rfq_notes": supplier.get("rfq_notes", []),
                }
            )
    return found


def _unit_capex_range(suppliers):
    """Combine matched supplier prices into one [low, high] range for a unit."""
    lows = []
    highs = []
    for supplier in suppliers:
        price = supplier.get("estimated_price_range_usd")
        if price and len(price) == 2:
            lows.append(price[0])
            highs.append(price[1])
    if not lows:
        return None
    return [min(lows), max(highs)]
