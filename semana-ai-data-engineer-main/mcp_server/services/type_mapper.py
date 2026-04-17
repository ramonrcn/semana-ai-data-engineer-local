def map_sql_type(sql_type: str):
    sql_type = sql_type.lower()

    if "uuid" in sql_type:
        return "UUID"
    if "numeric" in sql_type or "decimal" in sql_type:
        return "Decimal"
    if "int" in sql_type:
        return "int"
    if "timestamp" in sql_type:
        return "datetime"
    if "text" in sql_type:
        return "str"

    return "str"