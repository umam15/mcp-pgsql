import os

import psycopg2
from dotenv import load_dotenv
from mcp.server import MCPServer

load_dotenv()

PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = os.getenv("PGPORT", "5432")
PGDATABASE = os.getenv("PGDATABASE", "postgres")
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", "")
PGSSL = os.getenv("PGSSL", "disable")

mcp = MCPServer(name="mcp-pgsql", version="0.1.0")


def get_connection(autocommit: bool = False):
    conn = psycopg2.connect(
        host=PGHOST,
        port=PGPORT,
        database=PGDATABASE,
        user=PGUSER,
        password=PGPASSWORD,
        sslmode=PGSSL,
    )
    conn.autocommit = autocommit
    return conn


def rows_to_dicts(cursor):
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


@mcp.tool()
def execute_sql(query: str, autocommit: bool = False) -> dict:
    """Menjalankan query SQL sembarang (SELECT, INSERT, UPDATE, DELETE, DDL, dll)."""
    conn = None
    try:
        conn = get_connection(autocommit=autocommit)
        with conn.cursor() as cur:
            cur.execute(query)
            if cur.description:
                result = rows_to_dicts(cur)
            else:
                conn.commit()
                result = [{"rowcount": cur.rowcount}]
        return {"query": query, "rows": result, "count": len(result)}
    except Exception as e:
        if conn is not None:
            conn.rollback()
        return {"query": query, "error": str(e)}
    finally:
        if conn is not None:
            conn.close()


@mcp.tool()
def list_databases() -> dict:
    """Menampilkan daftar database yang tersedia di server PostgreSQL."""
    conn = None
    try:
        conn = get_connection(autocommit=True)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT datname AS name,
                       pg_get_userbyid(datdba) AS owner,
                       pg_catalog.pg_encoding_to_char(encoding) AS encoding
                FROM pg_database
                ORDER BY datname
                """
            )
            result = rows_to_dicts(cur)
        return {"databases": result, "count": len(result)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn is not None:
            conn.close()


@mcp.tool()
def get_schema(table_pattern: str = "%", schema: str = "public") -> dict:
    """Menampilkan skema database: tabel, kolom, indeks, dan constraint."""
    conn = None
    try:
        conn = get_connection(autocommit=True)
        tables = _fetch_tables(conn, table_pattern, schema)
        result = {"schema": schema, "tables": tables, "count": len(tables)}
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn is not None:
            conn.close()


def _fetch_tables(conn, table_pattern, schema):
    tables = []
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_name, table_type
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name LIKE %s
            ORDER BY table_name
            """,
            (schema, table_pattern),
        )
        for table_name, table_type in cur.fetchall():
            tables.append(
                {
                    "name": table_name,
                    "type": table_type,
                    "columns": _fetch_columns(conn, schema, table_name),
                    "indexes": _fetch_indexes(conn, schema, table_name),
                    "constraints": _fetch_constraints(conn, schema, table_name),
                }
            )
    return tables


def _fetch_columns(conn, schema, table_name):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name,
                   data_type,
                   is_nullable,
                   COALESCE(column_default, '')
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
            """,
            (schema, table_name),
        )
        return [
            {
                "name": name,
                "type": dtype,
                "nullable": nullable == "YES",
                "default": default,
            }
            for name, dtype, nullable, default in cur.fetchall()
        ]


def _fetch_indexes(conn, schema, table_name):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE schemaname = %s AND tablename = %s
            ORDER BY indexname
            """,
            (schema, table_name),
        )
        return [{"name": name, "definition": definition} for name, definition in cur.fetchall()]


def _fetch_constraints(conn, schema, table_name):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT tc.constraint_name, tc.constraint_type, tc.is_deferrable
            FROM information_schema.table_constraints tc
            WHERE tc.table_schema = %s AND tc.table_name = %s
            ORDER BY tc.constraint_name
            """,
            (schema, table_name),
        )
        return [
            {"name": name, "type": ctype, "deferrable": deferrable}
            for name, ctype, deferrable in cur.fetchall()
        ]


if __name__ == "__main__":
    mcp.run(transport="stdio")
