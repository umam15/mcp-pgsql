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

## Penggunaan

Jalankan server:

```bash
python server.py
```

Kemudian daftarkan server MCP ini ke client MCP (misal: Claude Desktop, Cursor, dll).

## Daftar Tool

| Tool            | Deskripsi                          |
|-----------------|------------------------------------|
| `execute_sql`   | Menjalankan query SQL sembarang    |
| `list_databases`| Menampilkan daftar database        |
| `get_schema`    | Menampilkan skema database         |

## Lisensi

MIT
