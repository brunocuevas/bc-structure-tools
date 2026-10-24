def parse_yaml_input(yaml_path):
    """Load a YAML input file."""
    import yaml

    with open(yaml_path, "r") as f:
        input_data = yaml.load(f, yaml.Loader)

    return input_data


def parse_json_input(json_path):
    """Load a JSON input file."""
    import json

    with open(json_path) as f:
        input_data = json.load(f)
    return input_data


def input_validation(input: dict):
    try:
        components = input["sequences"]
    except KeyError:
        raise IOError("Input missed the field sequences")

    for i, (component_type, component_content) in enumerate(components):
        if component_type not in ["protein", "ligand"]:
            raise IOError(f"Type {component_type} not supported on component {i}")
        if "id" not in component_content:
            raise IOError(f"Missing id on component {i}")
        if component_type == "protein" and "sequence" not in component_content:
            raise IOError(f"Missing sequence on protein component {i}")
        if component_type == "ligand" and "ccd" not in component_content:
            raise IOError(f"Missing ccd on ligand component {i}")

    try:
        input["name"]
    except KeyError:
        raise IOError("Missing name")

    try:
        input["dialect"]
    except KeyError:
        raise IOError("Missing dialect")

    try:
        input["version"]
    except KeyError:
        raise IOError("Missing version")

    return


def build_structure_input(item: dict):
    """Convert a validated AF3-like entry into StructurePredictionInput."""
    from esm.utils.structure.input_builder import (
        LigandInput,
        ProteinInput,
        StructurePredictionInput,
    )

    components = []
    for component_type, component_content in item["sequences"]:
        kind = component_type.lower()
        if kind == "protein":
            for chain in component_content["id"]:
                components.append(
                    ProteinInput(id=chain, sequence=component_content["sequence"])
                )
        elif kind == "ligand":
            ccd = component_content["ccd"]
            if isinstance(ccd, str):
                ccd = [ccd]
            for chain in component_content["id"]:
                components.append(LigandInput(id=chain, ccd=list(ccd)))
        else:
            raise IOError(f"Type {component_type} not supported")

    return StructurePredictionInput(sequences=components)
