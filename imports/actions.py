from db.db import exec_sql, exec_sql_with_result


def process_data(db_conn, definition):
    source_data = definition.get("source")()
    if not source_data:
        return source_data
    init_statement = definition.get("init_statement")
    upsert_list = [init_statement] if init_statement else []
    for source_record in source_data:
        upsert = process_record(db_conn, source_record, definition)
        if upsert:
            upsert_list.append(upsert)
            if definition.get("children_defs"):
                upsert_list += process_children_defs(db_conn, source_record, definition)
    return upsert_list


def process_children_defs(db_conn, parent_source_record, parent_def):
    children_upserts = []
    for child_def_meta in parent_def.get("children_defs"):
        args = [resolve_def_arg(db_conn, parent_source_record, f) for f in child_def_meta.get("def_args")]
        child_def = child_def_meta.get("def_fn")(*args)
        try:
            children_upserts += process_data(db_conn, child_def)
        except TypeError:
            pass
    return children_upserts


def resolve_def_arg(db_conn, source_record, field):
    if callable(field):
        return field(db_conn, source_record)
    return source_record.get(field)


def process_record(db_conn, source_record, definition):
    return get_upsert_sql(db_conn, source_record, definition)


def get_upsert_sql(db_conn, source_record, definition):
    mapping = definition.get("mapping")
    fields, values = resolved_map_to_fields_and_values(resolve_mapping(source_record, mapping))
    existing_record = record_exists(db_conn, source_record, definition)
    if should_abort_update(existing_record, definition.get("abort_update_condition")):
        return False
    if existing_record:
        return fields_and_values_to_sql_update(fields, values).format(
            table_name=definition.get("target"),
            where=get_where_record(source_record, definition)
        )
    return fields_and_values_to_sql_insert(fields, values).format(table_name=definition.get("target"))


def should_abort_update(existing_record, abort_update_condition):
    if not existing_record or not abort_update_condition:
        return False
    check_field, check_fn = abort_update_condition
    check_value = existing_record.get(check_field)
    return check_fn(check_value)


def record_exists(db_conn, source_record, definition):
    sql = existing_record_sql(source_record, definition)
    if sql is False:
        return False
    results = exec_sql_with_result(db_conn, sql)
    try:
        return results[0]
    except IndexError:
        return False


def existing_record_sql(source_record, definition):
    base_sql = "select * from {table_name} where {where}"
    where = get_where_record(source_record, definition)
    if where is False:
        return False
    return base_sql.format(table_name=definition.get("target"), where=where)


def get_where_record(source_record, definition):
    try:
        target_pk_field, source_pk_field = definition.get("check_attrs")
        transform_fn = definition.get("check_transform_fn", lambda x: x)
        source_pk_value = transform_fn(source_record.get(source_pk_field))
        return "{pk_field} = {pk}".format(pk_field=target_pk_field, pk=value_to_sql(source_pk_value))
    except TypeError:
        return False


def resolved_map_to_fields_and_values(resolved_map):
    fields = []
    values = []
    for field, value in resolved_map.items():
        fields.append(field)
        values.append(value_to_sql(value))
    return fields, values


def fields_and_values_to_sql_insert(fields, values):
    inserts = "({fields}) values ({values})".format(fields=", ".join(fields), values=", ".join(values))
    return "insert into {table_name} " + inserts + ";"


def fields_and_values_to_sql_update(fields, values):
    updates = ["{} = {}".format(field, values[index]) for index, field in enumerate(fields)]
    return "update {table_name} set " + ", ".join(updates) + " where {where};"


def value_to_sql(value):
    if value is None:
        return 'null'
    if type(value) == str:
        return "'{}'".format(value)
    return str(value)


def resolve_mapping(source_record, mapping):
    result = {}
    for target_field, source_mapping in mapping.items():
        source_field, resolving_fn = [source_mapping[0], source_mapping[1]]
        target_value = resolving_fn(
            source_record.get(source_field),
            *mapping_aditional_args(source_record, source_mapping)
        )
        result[target_field] = target_value
    return result


def mapping_aditional_args(source_record, source_mapping):
    """
    source_mapping may contain a third element
    with the names of source fields which values
    must be passed as arguments to the resolving function
    """
    if len(source_mapping) < 3:
        return []
    return [source_record.get(f) for f in source_mapping[2]]
