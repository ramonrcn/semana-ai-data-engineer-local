import re
from services.files import read_file


KB_PATH = ".claude/kb/python/"


def load_kb_file(name: str) -> str:
    path = f"{KB_PATH}/{name}"
    return read_file(path)


# -------------------------
# RULES (hard-coded parsing)
# -------------------------

def validate_uuid_usage(code: str):
    return "UUID" in code


def validate_decimal_usage(code: str):
    return "Decimal" in code


def validate_no_float(code: str):
    return "float" not in code


def validate_literal_usage(code: str):
    return "Literal[" in code


def validate_no_enum(code: str):
    return "Enum" not in code


def validate_field_constraints(code: str):
    return "Field(ge=" in code or "Field(le=" in code


def validate_no_required_field(code: str):
    return "Field(...)" not in code


# -------------------------
# MAIN VALIDATOR
# -------------------------

def validate_models_code(code: str) -> dict:
    results = {
        "uuid": validate_uuid_usage(code),
        "decimal": validate_decimal_usage(code),
        "no_float": validate_no_float(code),
        "literal": validate_literal_usage(code),
        "no_enum": validate_no_enum(code),
        "field_constraints": validate_field_constraints(code),
        "no_required_field": validate_no_required_field(code),
    }

    results["valid"] = all(results.values())

    return results