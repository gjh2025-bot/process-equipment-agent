"""
unit_decomposer.py

Break the process into major unit operations.

This is a deterministic, rule-based decomposition for the MnO2 hydrothermal
demo case. Each unit operation is turned into a structured object that carries
the operating requirements (phase, temperature, pressure, volume) that the
equipment selector and engineering reviewer will screen against.

The `process_step` field on each unit is the key used later to match against
the equipment database's "suitable_process_steps".
"""


# Approximate autogenous pressure of water near 180 C is roughly 10 bar.
# This is an illustrative design point, NOT a certified value.
HYDROTHERMAL_DESIGN_PRESSURE_BAR = 10


def decompose_process(process_input, process_basis):
    """Return a list of structured unit-operation dictionaries.

    Args:
        process_input: parsed data/sample_input.json
        process_basis: output of process_basis.build_process_basis

    Returns:
        list of unit-operation dicts in process order.
    """
    target_volume_l = process_basis["target_scale_basis"].get(
        "target_batch_liquid_volume_l"
    )
    conditions = process_basis["operating_condition_summary"]

    pre_temp_range = conditions.get("pre_reaction_temperature_c_range") or [50, 60]
    reaction_temp = conditions.get("reaction_temperature_c") or 180
    drying_temp = conditions.get("drying_temperature_c") or 80

    # Each entry is defined explicitly so the workflow is easy to read and
    # easy to explain during a demo. The order follows the physical process.
    units = [
        {
            "unit_name": "Precursor solution preparation",
            "unit_type": "precursor_mixing",
            "process_step": "precursor solution preparation",
            "phase": "liquid",
            "temperature_c": 25,
            "pressure_bar": 1,
        },
        {
            "unit_name": "Heated mixing",
            "unit_type": "precursor_mixing",
            "process_step": "heated mixing",
            "phase": "liquid",
            "temperature_c": pre_temp_range[1],
            "pressure_bar": 1,
        },
        {
            "unit_name": "Hydrothermal batch reaction",
            "unit_type": "hydrothermal_reactor",
            "process_step": "hydrothermal batch reaction",
            "phase": "liquid-solid slurry",
            "temperature_c": reaction_temp,
            "pressure_bar": HYDROTHERMAL_DESIGN_PRESSURE_BAR,
        },
        {
            "unit_name": "Controlled cooling and safe depressurization",
            "unit_type": "hydrothermal_reactor",
            # Performed in the same sealed reactor, so it screens against the
            # same equipment as the hydrothermal reaction step.
            "process_step": "hydrothermal batch reaction",
            "phase": "liquid-solid slurry",
            "temperature_c": reaction_temp,
            "pressure_bar": HYDROTHERMAL_DESIGN_PRESSURE_BAR,
        },
        {
            "unit_name": "Solid-liquid separation",
            "unit_type": "solid_liquid_separation",
            "process_step": "solid-liquid separation",
            "phase": "fine particle suspension",
            "temperature_c": 25,
            "pressure_bar": 1,
        },
        {
            "unit_name": "Washing to neutral pH",
            "unit_type": "washing",
            # Matches "washing to neutral pH" in the equipment database.
            "process_step": "washing to neutral pH",
            "phase": "liquid-solid slurry",
            "temperature_c": 25,
            "pressure_bar": 1,
        },
        {
            "unit_name": "Vacuum drying",
            "unit_type": "drying",
            # Matches "vacuum drying" in the equipment database.
            "process_step": "vacuum drying",
            "phase": "wet cake",
            "temperature_c": drying_temp,
            # Vacuum operation, so well below atmospheric. MVP assumption.
            "pressure_bar": 0.1,
        },
        {
            "unit_name": "Powder collection",
            "unit_type": "powder_collection",
            "process_step": "powder collection",
            "phase": "dry powder",
            "temperature_c": 25,
            "pressure_bar": 1,
        },
    ]

    # Attach a stable id, the shared volume requirement, and the relevant
    # process concerns to every unit.
    concerns = process_input.get("known_process_concerns", [])
    for index, unit in enumerate(units, start=1):
        unit["unit_id"] = "U-{:02d}".format(index)
        unit["required_volume_l"] = target_volume_l
        unit["related_concerns"] = _related_concerns(unit, concerns)

    # Put unit_id first for readability when the dict is serialized.
    ordered = []
    for unit in units:
        ordered.append(_reorder_unit(unit))
    return ordered


def _related_concerns(unit, concerns):
    """Pick process concerns that are clearly relevant to this unit.

    Uses simple keyword matching so the link between a unit and a concern is
    transparent and easy to audit.
    """
    keywords = {
        "hydrothermal_reactor": ["pressure", "temperature", "morphology", "cooling"],
        "solid_liquid_separation": ["separate", "filter", "particle"],
        "washing": ["washing", "contamination", "residual", "soluble"],
        "drying": ["drying", "vacuum", "hydration"],
        "precursor_mixing": ["contamination", "metallic"],
        "powder_collection": ["reproducibility", "contamination"],
    }.get(unit["unit_type"], [])

    matched = []
    for concern in concerns:
        lowered = concern.lower()
        if any(word in lowered for word in keywords):
            matched.append(concern)
    return matched


def _reorder_unit(unit):
    """Return the unit dict with a readable key order."""
    key_order = [
        "unit_id",
        "unit_name",
        "unit_type",
        "process_step",
        "phase",
        "temperature_c",
        "pressure_bar",
        "required_volume_l",
        "related_concerns",
    ]
    return {key: unit[key] for key in key_order}
