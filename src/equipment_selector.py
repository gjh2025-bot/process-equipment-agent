"""
equipment_selector.py

Find candidate equipment for each unit operation from the mock equipment
database.

This step is intentionally a LOOSE, first-pass search. It only checks the two
fields that decide whether a piece of equipment is even the right kind of tool
for the job:

  1. process step  -- the unit's process_step must be listed in the
                      equipment's "suitable_process_steps"
  2. phase         -- the unit's phase must overlap the equipment's
                      "suitable_phase"

The stricter engineering checks (temperature, pressure, volume, contamination,
materials) are done later in engineering_reviewer.py, so that the "candidate
search" and the "accept / reject decision" stay clearly separated.
"""


def select_equipment(units, equipment_database):
    """Return candidate equipment for every unit operation.

    Args:
        units: list of unit-operation dicts from unit_decomposer.
        equipment_database: parsed data/equipment_database.json.

    Returns:
        list of dicts, one per unit, each containing the unit id/name and a
        list of candidate equipment entries.
    """
    all_equipment = equipment_database.get("equipment", [])

    results = []
    for unit in units:
        candidates = []
        for equipment in all_equipment:
            if _is_candidate(unit, equipment):
                candidates.append(_describe_candidate(unit, equipment))

        results.append(
            {
                "unit_id": unit["unit_id"],
                "unit_name": unit["unit_name"],
                "unit_type": unit["unit_type"],
                # Carry the unit's operating requirements forward so the
                # engineering reviewer can apply its strict checks without
                # re-reading the unit list.
                "process_step": unit["process_step"],
                "phase": unit["phase"],
                "temperature_c": unit["temperature_c"],
                "pressure_bar": unit["pressure_bar"],
                "required_volume_l": unit["required_volume_l"],
                "candidates": candidates,
            }
        )
    return results


def _is_candidate(unit, equipment):
    """Return True if the equipment is the right kind of tool for the unit."""
    step_matches = unit["process_step"] in equipment.get(
        "suitable_process_steps", []
    )
    phase_matches = unit["phase"] in equipment.get("suitable_phase", [])
    return step_matches and phase_matches


def _describe_candidate(unit, equipment):
    """Build a candidate record that records WHY it was matched.

    The matched_fields / initial_fit_notes make the first-pass selection
    transparent and easy to read in the final report.
    """
    return {
        "equipment_id": equipment["equipment_id"],
        "equipment_name": equipment["name"],
        "equipment_type": equipment["equipment_type"],
        "matched_fields": {
            "process_step": unit["process_step"],
            "phase": unit["phase"],
        },
        "initial_fit_notes": [
            "Process step '{}' is listed in this equipment's suitable steps.".format(
                unit["process_step"]
            ),
            "Phase '{}' is supported by this equipment.".format(unit["phase"]),
        ],
        # Carry the full equipment record forward so the engineering reviewer
        # can apply the strict temperature / pressure / volume / material
        # checks without re-reading the database.
        "equipment_record": equipment,
    }
