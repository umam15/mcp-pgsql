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


@mcp.tool()
def list_schemas() -> dict:
    """Menampilkan daftar skema yang tersedia di database."""
    conn = None
    try:
        conn = get_connection(autocommit=True)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT schema_name, schema_owner
                FROM information_schema.schemata
                ORDER BY schema_name
                """
            )
            result = rows_to_dicts(cur)
        return {"schemas": result, "count": len(result)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn is not None:
            conn.close()


@mcp.tool()
def describe_table(table: str, schema: str = "public") -> dict:
    """Menampilkan detail satu tabel: kolom, tipe, PK/FK, dan default."""
    conn = None
    try:
        conn = get_connection(autocommit=True)
        columns = _fetch_columns(conn, schema, table)
        primary_keys = _fetch_primary_keys(conn, schema, table)
        foreign_keys = _fetch_foreign_keys(conn, schema, table)
        indexes = _fetch_indexes(conn, schema, table)
        return {
            "schema": schema,
            "table": table,
            "columns": columns,
            "primary_keys": primary_keys,
            "foreign_keys": foreign_keys,
            "indexes": indexes,
            "column_count": len(columns),
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn is not None:
            conn.close()


def _fetch_primary_keys(conn, schema, table_name):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            WHERE tc.table_schema = %s
              AND tc.table_name = %s
              AND tc.constraint_type = 'PRIMARY KEY'
            ORDER BY kcu.ordinal_position
            """,
            (schema, table_name),
        )
        return [row[0] for row in cur.fetchall()]


def _fetch_foreign_keys(conn, schema, table_name):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT kcu.column_name,
                   ccu.table_schema AS foreign_schema,
                   ccu.table_name AS foreign_table,
                   ccu.column_name AS foreign_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tc.constraint_name
             AND ccu.table_schema = tc.table_schema
            WHERE tc.table_schema = %s
              AND tc.table_name = %s
              AND tc.constraint_type = 'FOREIGN KEY'
            ORDER BY kcu.ordinal_position
            """,
            (schema, table_name),
        )
        return [
            {
                "column": column,
                "references": {
                    "schema": foreign_schema,
                    "table": foreign_table,
                    "column": foreign_column,
                },
            }
            for column, foreign_schema, foreign_table, foreign_column in cur.fetchall()
        ]


@mcp.tool()
def list_views(schema: str = "public", view_pattern: str = "%") -> dict:
    """Menampilkan daftar view di skema tertentu."""
    conn = None
    try:
        conn = get_connection(autocommit=True)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT table_name, view_definition
                FROM information_schema.views
                WHERE table_schema = %s AND table_name LIKE %s
                ORDER BY table_name
                """,
                (schema, view_pattern),
            )
            result = [
                {"name": name, "definition": definition}
                for name, definition in cur.fetchall()
            ]
        return {"schema": schema, "views": result, "count": len(result)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn is not None:
            conn.close()


@mcp.tool()
def list_extensions() -> dict:
    """Menampilkan daftar extension PostgreSQL yang terpasang."""
    conn = None
    try:
        conn = get_connection(autocommit=True)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT extname AS name,
                       extversion AS version,
                       n.nspname AS schema
                FROM pg_extension e
                JOIN pg_namespace n ON n.oid = e.extnamespace
                ORDER BY extname
                """
            )
            result = rows_to_dicts(cur)
        return {"extensions": result, "count": len(result)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn is not None:
            conn.close()


@mcp.tool()
def get_table_stats(table: str, schema: str = "public") -> dict:
    """Menampilkan estimasi ukuran & row count sebuah tabel."""
    conn = None
    try:
        conn = get_connection(autocommit=True)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT pg_size_pretty(pg_total_relation_size(%s)) AS total_size,
                       pg_size_pretty(pg_relation_size(%s)) AS table_size,
                       pg_size_pretty(pg_total_relation_size(%s) - pg_relation_size(%s)) AS index_size,
                       reltuples::bigint AS estimated_rows,
                       relpages AS pages
                FROM pg_class
                JOIN pg_namespace n ON n.oid = relnamespace
                WHERE n.nspname = %s AND relname = %s
                """,
                (
                    f"{schema}.{table}",
                    f"{schema}.{table}",
                    f"{schema}.{table}",
                    f"{schema}.{table}",
                    schema,
                    table,
                ),
            )
            result = rows_to_dicts(cur)
        return {"schema": schema, "table": table, "stats": result}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn is not None:
            conn.close()


@mcp.tool()
def explain_query(query: str, analyze: bool = False) -> dict:
    """Menampilkan rencana eksekusi query (`EXPLAIN`). Opsional `analyze` untuk eksekusi nyata."""
    conn = None
    try:
        conn = get_connection(autocommit=True)
        with conn.cursor() as cur:
            plan_query = f"EXPLAIN {'ANALYZE ' if analyze else ''}({query})"
            cur.execute(plan_query)
            plan = [row[0] for row in cur.fetchall()]
        return {"query": query, "analyze": analyze, "plan": plan}
    except Exception as e:
        return {"query": query, "error": str(e)}
    finally:
        if conn is not None:
            conn.close()


@mcp.tool()
def get_running_queries() -> dict:
    """Menampilkan query yang sedang berjalan (via pg_stat_activity)."""
    conn = None
    try:
        conn = get_connection(autocommit=True)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT pid,
                       usename,
                       datname,
                       state,
                       waiting,
                       LEFT(query, 200) AS query,
                       (NOW() - query_start)::text AS duration
                FROM pg_stat_activity
                WHERE query NOT LIKE '%pg_stat_activity%'
                  AND pid <> pg_backend_pid()
                ORDER BY query_start DESC
                """
            )
            result = rows_to_dicts(cur)
        return {"running_queries": result, "count": len(result)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn is not None:
            conn.close()


@mcp.tool()
def kill_query(pid: int) -> dict:
    """Menghentikan query berjalan pada pid tertentu (pg_terminate_backend)."""
    conn = None
    try:
        conn = get_connection(autocommit=True)
        with conn.cursor() as cur:
            cur.execute("SELECT pg_terminate_backend(%s)", (pid,))
            terminated = cur.fetchone()[0]
        return {"pid": pid, "terminated": terminated}
    except Exception as e:
        return {"pid": pid, "error": str(e)}
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    mcp.run(transport="stdio")
