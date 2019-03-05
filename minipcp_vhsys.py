import psycopg2
from imports import definitions as defs
from imports import actions
from db.db import init_db, exec_sql
from local_settings import(
    MINIPCP_DB_HOST,
    MINIPCP_DB_PORT,
    MINIPCP_DB_NAME,
    MINIPCP_DB_USER,
    MINIPCP_DB_PASSWORD
)
from imports.definitions import(
    SOURCE_TYPE__ALL,
    SOURCE_TYPE__SINCE,
    SOURCE_TYPE__BY_ID,
)


def run(args):
    db_conn, db_error = get_db_conn()
    if db_error:
        print(db_error)
        return
    db_conn.autocommit = False

    import_source(db_conn, args, "clientes", defs.clientes)
    import_source(db_conn, args, "produtos", defs.produtos)
    import_source(db_conn, args, "pedidos de venda", defs.pedidos)

    if not args.dry_run:
        db_conn.commit()
    else:
        db_conn.rollback()


def get_db_conn():
    try:
        db_conn = init_db(get_db_settings())
    except psycopg2.OperationalError:
        return None, format_error("Parâmetros de conexão incorretos ou banco de dados não disponível")
    return db_conn, None

def get_db_settings():
    return {
        "host": MINIPCP_DB_HOST,
        "post": MINIPCP_DB_PORT,
        "dbname": MINIPCP_DB_NAME,
        "user": MINIPCP_DB_USER,
        "password": MINIPCP_DB_PASSWORD,
    }


def import_source(db_conn, args, source_name, defs_fn):
    source_type, source_param = get_type_and_param(args)
    verbose_type_and_param(args, source_name, source_type, source_param)
    import_data(db_conn, args, defs_fn, source_type, source_param)


def import_data(db_conn, args, def_fn, source_type, source_param):
    import_def = def_fn(source_type, source_param)
    process_upserts(db_conn, args, actions.process_data(db_conn, import_def), import_def.get("description"))


def get_type_and_param(args):
    if args.all:
        return SOURCE_TYPE__ALL, None
    elif args.since:
        return SOURCE_TYPE__SINCE, args.since

def verbose_type_and_param(args, source_name, source_type, source_param):
    display_verbose(
        args.verbose,
        "Importando {}".format(source_name),
        [("source_type", source_type), ("source_param", source_param)]
    )


def process_upserts(db_conn, args, upsert_list, data_description):
    if not upsert_list:
        print ("Não existem {} novos na condição solicitada".format(data_description))
    else:
        sql = "\n".join(upsert_list)
        display_verbose(args.verbose or args.dry_run, data_description, [(None, sql)])
        exec_sql(db_conn, sql)


def format_error(msg):
    return "ERRO: {}".format(msg)


def display_verbose(verbose, title, data):
    if verbose:
        print("*** {} ***".format(title))
        for name, value in data:
            if name is None:
                print(value)
            else:
                print("- {}: {}".format(name, value))
        print("")
