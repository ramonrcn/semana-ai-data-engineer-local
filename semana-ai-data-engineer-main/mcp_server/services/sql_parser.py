import re


def parse_tables(sql: str):
    tables = {}

    current_table = None

    for line in sql.splitlines():
        line = line.strip()

        # detecta tabela
        match_table = re.match(r"CREATE TABLE IF NOT EXISTS (\w+)", line, re.IGNORECASE)
        if match_table:
            current_table = match_table.group(1).lower()
            tables[current_table] = []
            continue

        if current_table and line.startswith(")"):
            current_table = None
            continue

        if current_table and line:
            tables[current_table].append(line)

    return tables

def parse_column(line: str):
    parts = line.split()

    name = parts[0]
    type_ = parts[1]

    return {
        "name": name,
        "type": type_,
        "raw": line
    }

def extract_literal(line: str):
    match = re.search(r"CHECK \((.*?) IN \((.*?)\)\)", line)

    if match:
        values = match.group(2)
        values = [v.strip().strip("'") for v in values.split(",")]

        return f"Literal[{', '.join([f'\"{v}\"' for v in values])}]"

    return None

def is_optional(line: str):
    return "NOT NULL" not in line

def extract_check_values(line: str):
    match = re.search(r"IN\s*\((.*?)\)", line, re.IGNORECASE)

    if not match:
        return None

    values = match.group(1)

    return [
        v.strip().replace("'", "").lower()
        for v in values.split(",")
    ]