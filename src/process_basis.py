"""
process_basis.py

Build a preliminary "process basis" from the lab-scale process brief.

This module does NOT simulate anything. It only reads the structured input
JSON and pulls out / lightly infers the engineering basics that the rest of
the workflow needs (product, scale, operating conditions, priorities, and
the data we are missing).
"""


def build_process_basis(process_input):
    """Return a structured process basis dictionary.

    Args:
        process_input: the parsed contents of data/sample_input.json

    Returns:
        dict describing the preliminary process basis.
    """
    lab = process_input.get("lab_scale_process", {})
    target = process_input.get("target_scale", {})
    product = process_input.get("target_product", {})

    # --- Lab-scale basis -------------------------------------------------
    lab_volume_ml = lab.get("batch_liquid_volume_ml")
    hydrothermal = lab.get("hydrothermal_step", {})
    pre_step = lab.get("pre_hydrothermal_step", {})

    lab_basis = {
        "batch_liquid_volume_ml": lab_volume_ml,
        "synthesis_route": lab.get("synthesis_route"),
        "pre_reaction_temperature_c_range": pre_step.get("temperature_c_range"),
        "hydrothermal_temperature_c": hydrothermal.get("temperature_c"),
        "hydrothermal_duration_hr": hydrothermal.get("duration_hr"),
        "hydrothermal_pressure_condition": hydrothermal.get("pressure_condition"),
    }

    # --- Target-scale basis ---------------------------------------------
    target_volume_l = target.get("target_batch_liquid_volume_l")
    target_basis = {
        "mode": target.get("mode"),
        "target_batch_liquid_volume_l": target_volume_l,
        "batches_per_day": target.get("batches_per_day"),
        "operation_mode": target.get("operation_mode"),
    }

    # --- Scale-up factor -------------------------------------------------
    # Prefer the value given in the input. If absent, compute it from volumes.
    scale_up_factor = target.get("scale_up_factor_from_lab_volume")
    if scale_up_factor is None and lab_volume_ml and target_volume_l:
        scale_up_factor = round((target_volume_l * 1000.0) / lab_volume_ml, 1)

    # --- Operating condition summary ------------------------------------
    operating_conditions = {
        "pre_reaction_temperature_c_range": pre_step.get("temperature_c_range"),
        "reaction_temperature_c": hydrothermal.get("temperature_c"),
        "reaction_pressure": hydrothermal.get("pressure_condition"),
        "drying_temperature_c": _find_drying_temperature(lab),
    }

    # --- Missing / uncertain data ---------------------------------------
    # These are simple, transparent checks so a reader can see WHY each item
    # is flagged. This is intentionally rule-based, not "smart".
    missing_data = _find_missing_data(process_input, scale_up_factor)

    return {
        "product_summary": {
            "name": product.get("name"),
            "intended_application": product.get("intended_application"),
            "critical_quality_attributes": product.get(
                "critical_quality_attributes", []
            ),
        },
        "lab_scale_basis": lab_basis,
        "target_scale_basis": target_basis,
        "scale_up_factor": scale_up_factor,
        "operating_condition_summary": operating_conditions,
        "quality_and_contamination_priorities": process_input.get(
            "equipment_selection_priorities", []
        ),
        "preferred_materials": process_input.get("preferred_materials", []),
        "avoid_materials": process_input.get("avoid_materials", []),
        "known_risks": process_input.get("known_process_concerns", []),
        "missing_or_uncertain_data": missing_data,
    }


def _find_drying_temperature(lab):
    """Look through post-reaction steps for a drying temperature."""
    for step in lab.get("post_reaction_steps", []):
        if step.get("operation") == "drying":
            return step.get("temperature_c")
    return None


def _find_missing_data(process_input, scale_up_factor):
    """Return a list of plain-language notes about gaps in the input."""
    notes = []

    target = process_input.get("target_scale", {})
    if target.get("target_batch_liquid_volume_l") is None:
        notes.append("Target batch volume is not specified.")

    if scale_up_factor is None:
        notes.append("Scale-up factor could not be determined.")

    hydrothermal = process_input.get("lab_scale_process", {}).get(
        "hydrothermal_step", {}
    )
    # Autogenous pressure is given as a condition, not a number, so the real
    # design pressure still needs to be confirmed.
    if not isinstance(hydrothermal.get("pressure_bar"), (int, float)):
        notes.append(
            "Hydrothermal operating pressure is autogenous and given as a "
            "condition, not a confirmed numeric value. Design pressure at "
            "the hold temperature must be verified."
        )

    notes.append(
        "Particle size, yield, and morphology after scale-up are not predicted "
        "by this tool and require experimental confirmation."
    )

    return notes
