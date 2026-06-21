"""
engineering_reviewer.py

Screen the candidate equipment from equipment_selector against engineering
constraints, then pick a recommended option for each unit operation.

This module favours transparent, rule-based reasoning over clever scoring.
For every candidate it records exactly which checks passed and which failed,
so a reader can audit each accept / reject decision.

Checks applied per candidate:
  - temperature: the unit's temperature must fall in the equipment range
  - pressure:    the unit's pressure must fall in the equipment range
  - volume:      the unit's required volume must fall in the equipment's
                 working volume range

A candidate is ACCEPTED only if all three checks pass. Among accepted
candidates, the recommendation is the one with the best contamination control
(contamination matters a lot for battery-grade MnO2), breaking ties by the
order they appear in the database.
"""


# Rank used to prefer cleaner equipment when several candidates are accepted.
_CONTAMINATION_RANK = {"high": 3, "medium": 2, "low": 1}


def review_candidates(selection_results, process_basis):
    """Review every unit's candidates and choose a recommendation.

    Args:
        selection_results: output of equipment_selector.select_equipment.
            Each unit_result carries the unit's operating requirements
            (temperature_c, pressure_bar, required_volume_l).
        process_basis: output of process_basis.build_process_basis (reserved
            for shared risk / missing-data context).

    Returns:
        list of dicts, one per unit, with accepted/rejected candidates, the
        recommended equipment, and any unresolved risks.
    """
    reviews = []
    for unit_result in selection_results:
        accepted = []
        rejected = []

        for candidate in unit_result["candidates"]:
            verdict = _evaluate_candidate(unit_result, candidate)
            if verdict["accepted"]:
                accepted.append(verdict)
            else:
                rejected.append(verdict)

        recommended = _choose_recommendation(accepted)

        reviews.append(
            {
                "unit_id": unit_result["unit_id"],
                "unit_name": unit_result["unit_name"],
                "unit_type": unit_result["unit_type"],
                # Carry the unit's actual operating point forward so the RFQ
                # can state "we operate at X, so the equipment must cover X".
                "operating_temperature_c": unit_result.get("temperature_c"),
                "operating_pressure_bar": unit_result.get("pressure_bar"),
                "required_volume_l": unit_result.get("required_volume_l"),
                "accepted_candidates": accepted,
                "rejected_candidates": rejected,
                "recommended_equipment": recommended,
                "unresolved_risks": _unresolved_risks(recommended),
            }
        )
    return reviews


def _evaluate_candidate(unit_result, candidate):
    """Apply the temperature / pressure / volume checks to one candidate."""
    equipment = candidate["equipment_record"]

    # The unit's operating requirements live directly on unit_result.
    unit_temp = unit_result.get("temperature_c")
    unit_pressure = unit_result.get("pressure_bar")
    unit_volume = unit_result.get("required_volume_l")

    checks = []
    reasons = []

    temp_ok = _in_range(unit_temp, equipment.get("temperature_c_range"))
    checks.append(("temperature", temp_ok))
    reasons.append(
        _check_sentence(
            "Temperature", unit_temp, "C", equipment.get("temperature_c_range"), temp_ok
        )
    )

    pressure_ok = _in_range(unit_pressure, equipment.get("pressure_bar_range"))
    checks.append(("pressure", pressure_ok))
    reasons.append(
        _check_sentence(
            "Pressure", unit_pressure, "bar", equipment.get("pressure_bar_range"),
            pressure_ok,
        )
    )

    volume_ok = _in_range(unit_volume, equipment.get("working_volume_l_range"))
    checks.append(("volume", volume_ok))
    reasons.append(
        _check_sentence(
            "Required volume", unit_volume, "L",
            equipment.get("working_volume_l_range"), volume_ok,
        )
    )

    accepted = all(passed for _, passed in checks)

    return {
        "equipment_id": candidate["equipment_id"],
        "equipment_name": candidate["equipment_name"],
        "equipment_type": candidate["equipment_type"],
        "contamination_control_level": equipment.get(
            "contamination_control_level", "unknown"
        ),
        "accepted": accepted,
        "checks": {name: passed for name, passed in checks},
        "reasons": reasons,
        "equipment_record": equipment,
    }


def _choose_recommendation(accepted):
    """Pick the best accepted candidate, preferring cleaner equipment."""
    if not accepted:
        return None

    def sort_key(item):
        rank = _CONTAMINATION_RANK.get(item["contamination_control_level"], 0)
        # Higher contamination rank first; stable sort keeps database order.
        return -rank

    return sorted(accepted, key=sort_key)[0]


def _unresolved_risks(recommended):
    """Surface the recommended equipment's risk notes (if any)."""
    if not recommended:
        return ["No suitable equipment was accepted for this unit operation."]
    return recommended["equipment_record"].get("risk_notes", [])


def _in_range(value, range_pair):
    """Return True if value is inside [low, high]. Missing data -> False."""
    if value is None or not range_pair or len(range_pair) != 2:
        return False
    low, high = range_pair
    return low <= value <= high


def _check_sentence(label, value, unit, range_pair, passed):
    """Build a readable pass/fail sentence for one check."""
    status = "OK" if passed else "FAIL"
    if range_pair and len(range_pair) == 2:
        range_text = "{}-{} {}".format(range_pair[0], range_pair[1], unit)
    else:
        range_text = "unknown range"
    return "[{}] {} {} {} (equipment range {}).".format(
        status, label, value, unit, range_text
    )
