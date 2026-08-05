# Changelog

Semua perubahan penting pada proyek ini akan dicatat di file ini.

Format mengikuti [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) dan
[semantic versioning](https://semver.org/).

## [0.2.0] - 2026-08-05

### Added

- `requirements.txt` dengan dependensi `mcp`, `psycopg2-binary`, `python-dotenv`
- `server.py`: inisialisasi MCP server + koneksi PostgreSQL
- Tool `execute_sql` untuk menjalankan query SQL sembarang
- Tool `list_databases` untuk menampilkan daftar database
- Tool `get_schema` untuk membaca skema database (tabel, kolom, indeks, constraint)
- Konfigurasi via env var: `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGSSL`

## [0.1.0] - 2026-08-05

### Added

- Inisialisasi proyek MCP server untuk PostgreSQL
- Tool `execute_sql` untuk menjalankan query SQL
- Tool `list_databases` untuk menampilkan daftar database
- Tool `get_schema` untuk membaca skema database
- Workflow Auto Release (GitHub Actions & Gitea Actions)

[0.2.0]: https://github.com/owner/mcp-pgsql/releases/tag/v0.2.0
[0.1.0]: https://github.com/owner/mcp-pgsql/releases/tag/v0.1.0
