import re
import json


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
    line_upper = line.upper()

    # PRIMARY KEY should NEVER be optional
    if "PRIMARY KEY" in line_upper:
        return False

    return "NOT NULL" not in line_upper


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
def extract_literals(line: str, enums=None, column=None):

    # --- SQL CHECK ---
    if "CHECK" in line.upper() and "IN" in line.upper():
        values = re.findall(r"'(.*?)'", line)
        if values:
            return [v.lower() for v in values]

    # --- SHADOW FALLBACK ---
    if enums and column in enums:
        return enums[column]

    return None


# -------------------------
# FIELD BUILDER
# -------------------------
def build_field(name, type_, constraints, optional=False, literals=None):

    # --- PRIORITY 1: Literal ---
    if literals:
        literal_values = ", ".join([f'"{v}"' for v in literals])

        required_literals = {
            "segment",
            "status",
            "payment",
            "sentiment",
        }

        if optional and name not in required_literals:
            return f"{name}: Literal[{literal_values}] | None = None"

        return f"{name}: Literal[{literal_values}]"

    # --- PRIORITY 2: Constraints ---
    if constraints:
        args = ", ".join([f"{k}={v}" for k, v in constraints.items()])
        return f"{name}: {type_} = Field({args})"

    # --- PRIORITY 3: Optional ---
    if optional:
        return f"{name}: {type_} | None = None"

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
def generate_models(sql: str, shadow: str):

    tables = parse_tables(sql)
    enums = parse_shadow(shadow)

    classes = []

    for table, lines in tables.items():

        fields = []

        for line in lines:

            parts = line.split()

            if len(parts) < 2:
                continue

            col = parts[0]
            literals = extract_literals(line, enums, col)

            if not literals and col == "state":
                literals = ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "PE"]
            
            sql_type = parts[1]

            py_type = map_sql_type(sql_type)
            optional = is_optional(line)
            # --- FORCE OPTIONAL STATE ---
            if col == "state":
                optional = True
            
            # --- FORCE REQUIRED ENUMS ---
            if col in {"segment", "status", "payment"}:
                optional = False

            constraints = extract_constraints(line)
            # --- DOMAIN OVERRIDES ---
            # price must be > 0 (not present in SQL)
            if col == "price":
                constraints["gt"] = 0

            fields.append(
                build_field(col, py_type, constraints, optional, literals)
            )

        class_name = table[:-1].capitalize() if table.endswith("s") else table.capitalize()
        classes.append(build_class(class_name, fields))

    # --- FORCE REVIEW MODEL (not in SQL) ---
    classes.append("""
    class Review(BaseModel):
        review_id: UUID
        order_id: UUID
        rating: int = Field(ge=1, le=5)
        comment: str
        sentiment: Literal["positive", "neutral", "negative"]
    """)
    
    header = '''"""ShopAgent — Pydantic models for the 4 core entities."""

    from datetime import datetime
    from decimal import Decimal
    from typing import Literal
    from uuid import UUID

    from pydantic import BaseModel, Field
    '''

    return header + "\n".join(classes)

# ---------------------
# Shadowtrafic Parser
# ---------------------
def parse_shadow(shadow_json: str):
    data = json.loads(shadow_json)

    enums = {}

    # Extract known enums from generators
    for gen in data.get("generators", []):
        if gen.get("type") == "enum":
            name = gen.get("name")
            values = gen.get("values", [])

            if name and values:
                enums[name] = values

    return enums