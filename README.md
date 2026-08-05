# MCP PostgreSQL (mcp-pgsql)

MCP (Model Context Protocol) server untuk mengakses database PostgreSQL.

## Fitur

- Menjalankan query SQL (SELECT, INSERT, UPDATE, DELETE, dll)
- Membaca skema database (tabel, kolom, indeks, constraint)
- Listing database yang tersedia

## Prasyarat

- Python 3.10+
- PostgreSQL yang bisa diakses

## Instalasi

```bash
pip install -r requirements.txt
```

## Konfigurasi

Server ini dikonfigurasi lewat environment variable:

| Variable         | Deskripsi                    | Default       |
|------------------|------------------------------|---------------|
| `PGHOST`         | Host PostgreSQL              | `localhost`   |
| `PGPORT`         | Port PostgreSQL              | `5432`         |
| `PGDATABASE`     | Nama database default        | `postgres`    |
| `PGUSER`         | Username PostgreSQL          | `postgres`    |
| `PGPASSWORD`     | Password PostgreSQL          | *(kosong)*    |
| `PGSSL`          | Mode SSL (`disable`/`require`) | `disable`   |
| `PGREADONLY`     | Mode read-only default (`true`/`false`) | `true` |

## Mode Read-Only

Secara default server berjalan dalam mode **read-only** (`PGREADONLY=true`):

- Tool `execute_sql` menolak query yang mengubah data (INSERT, UPDATE, DELETE, DDL, dsb.)
- Koneksi juga di-set `default_transaction_read_only=on` oleh PostgreSQL sebagai lapisan keamanan kedua
- Untuk mengizinkan query yang menulis data, set env `PGREADONLY=false` **atau** panggil tool dengan parameter `allow_write=True`

Untuk uji coba lokal:

```bash
python server.py
```

Kemudian daftarkan server MCP ini ke client MCP (misal: Claude Desktop, Cursor, dll).

## Daftar Tool

| Tool                   | Deskripsi                                     |
|------------------------|-----------------------------------------------|
| `execute_sql`          | Menjalankan query SQL sembarang               |
| `list_databases`       | Menampilkan daftar database                   |
| `get_schema`           | Menampilkan skema database                    |
| `list_schemas`         | Menampilkan daftar skema                      |
| `describe_table`       | Detail satu tabel (kolom, PK, FK, default)    |
| `list_views`           | Menampilkan daftar view                       |
| `list_extensions`      | Menampilkan extension terpasang               |
| `get_table_stats`      | Ukuran & estimasi row count tabel             |
| `explain_query`        | Rencana eksekusi query (`EXPLAIN`)            |
| `get_running_queries`  | Query aktif (`pg_stat_activity`)              |
| `kill_query`           | Menghentikan query via `pg_terminate_backend` |

## Lisensi

MIT
