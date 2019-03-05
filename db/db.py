import psycopg2
from psycopg2 import extras

conn_str = None
conn = None


def init_db(settings, cursor_factory=extras.DictCursor):
    conn_str = get_conn_str(settings)
    conn = connect_db(conn_str, cursor_factory)
    return conn


def get_conn_str(settings):
    return "dbname='{}' user='{}' host='{}' password='{}' port='{}'".format(
        settings.get("dbname", ""),
        settings.get("user", ""),
        settings.get("host", ""),
        settings.get("password", ""),
        settings.get("port", "5432"),
    )


def exec_sql(db_conn, sql):
    db_conn.autocommit = True
    cur = db_conn.cursor()
    cur.execute(sql)
    return cur


def current_conn():
    if conn is None:
        raise Exception("Nenhuma conexão iniciada")
    return conn


def refresh_conn():
    return connect_db(conn_str)


def connect_db(_conn_str, cursor_factory=None):
    conn = psycopg2.connect(_conn_str, cursor_factory=cursor_factory)
    return conn


def exec_sql_with_result(db_conn, sql):
    return dictfetchall(exec_sql(db_conn, sql))


def exec_sql(db_conn, sql):
    cursor = db_conn.cursor()
    cursor.execute(sql)
    return cursor


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]
