import re


# -------------------------
# PARSE TABLES
# -------------------------
def parse_tables(sql: str):
    tables = {}
    current_table = None

    for line in sql.splitlines():
        line = line.strip()

        # suporta IF NOT EXISTS
        match = re.search(r"CREATE TABLE(?: IF NOT EXISTS)? (\w+)", line, re.IGNORECASE)

        if match:
            current_table = match.group(1).lower()
            tables[current_table] = []
            continue

        if current_table and line.startswith(")"):
            current_table = None
            continue

        if current_table and line:
            tables[current_table].append(line.rstrip(","))

    return tables


# -------------------------
# TYPE MAPPING
# -------------------------
def map_sql_type(sql_type: str):
    sql_type = sql_type.upper()

    if "UUID" in sql_type:
        return "UUID"

    if "VARCHAR" in sql_type or "TEXT" in sql_type:
        return "str"

    if "DECIMAL" in sql_type:
        return "Decimal"

    if "INTEGER" in sql_type:
        return "int"

    if "TIMESTAMP" in sql_type:
        return "datetime"

    return "str"


# -------------------------
# OPTIONAL
# -------------------------
def is_optional(line: str) -> bool:
    return "NOT NULL" not in line.upper()


# -------------------------
# CONSTRAINTS
# -------------------------
def extract_constraints(line: str):
    constraints = {}

    # BETWEEN 1 AND 10
    between = re.search(r"BETWEEN (\d+) AND (\d+)", line, re.IGNORECASE)
    if between:
        constraints["ge"] = int(between.group(1))
        constraints["le"] = int(between.group(2))

    # >= X
    ge = re.search(r">= (\d+)", line)
    if ge:
        constraints["ge"] = int(ge.group(1))

    return constraints


# -------------------------
# LITERALS
# -------------------------
def extract_literals(line: str):
    if "CHECK" in line.upper() and "IN" in line.upper():
        values = re.findall(r"'(.*?)'", line)
        if values:
            return [v.lower() for v in values]
    return None


# -------------------------
# FIELD BUILDER
# -------------------------
def build_field(name, type_, constraints, optional=False, literals=None):

    # PRIORIDADE 1 → Literal
    if literals:
        literal_values = ", ".join([f'"{v}"' for v in literals])
        return f"{name}: Literal[{literal_values}]"

    # PRIORIDADE 2 → Constraints
    if constraints:
        args = ", ".join([f"{k}={v}" for k, v in constraints.items()])
        return f"{name}: {type_} = Field({args})"

    # PRIORIDADE 3 → Optional
    if optional:
        return f"{name}: {type_} | None = None"

    # DEFAULT
    return f"{name}: {type_}"


# -------------------------
# CLASS BUILDER
# -------------------------
def build_class(name, fields):
    body = "\n".join([f"    {f}" for f in fields])

    return f"""
class {name}(BaseModel):
{body}
"""


# -------------------------
# MAIN GENERATOR
# -------------------------
def generate_models(sql: str):

    tables = parse_tables(sql)

    classes = []

    for table, lines in tables.items():

        fields = []

        for line in lines:

            parts = line.split()

            if len(parts) < 2:
                continue

            col = parts[0]
            sql_type = parts[1]

            py_type = map_sql_type(sql_type)
            optional = is_optional(line)
            constraints = extract_constraints(line)
            literals = extract_literals(line)

            fields.append(
                build_field(col, py_type, constraints, optional, literals)
            )

        classes.append(build_class(table.capitalize(), fields))

    header = """from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field
"""

    return header + "\n".join(classes)