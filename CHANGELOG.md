# Changelog

Semua perubahan penting pada proyek ini akan dicatat di file ini.

Format mengikuti [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) dan
[semantic versioning](https://semver.org/).

## [0.4.0] - 2026-08-05

### Added

- Mode **read-only default** (`PGREADONLY`, default `true`): `execute_sql` menolak query write, didukung lapisan keamanan `default_transaction_read_only=on` di level koneksi
- Parameter `allow_write=True` pada `execute_sql` sebagai override eksplisit per-panggilan

## [0.3.1] - 2026-08-05

### Fixed

- Tool `get_running_queries`: kompatibel dengan PostgreSQL < 9.6 (ganti `wait_event_type`/`wait_event` dengan `waiting`)

### Added

- `.env.example` sebagai template konfigurasi env var

## [0.3.0] - 2026-08-05

### Added

- Tool `list_schemas` untuk menampilkan daftar skema
- Tool `describe_table` untuk detail satu tabel (kolom, PK, FK, default)
- Tool `list_views` untuk menampilkan daftar view
- Tool `list_extensions` untuk menampilkan extension terpasang
- Tool `get_table_stats` untuk ukuran & estimasi row count tabel
- Tool `explain_query` untuk rencana eksekusi query (`EXPLAIN`/`EXPLAIN ANALYZE`)
- Tool `get_running_queries` untuk query aktif (`pg_stat_activity`)
- Tool `kill_query` untuk menghentikan query via `pg_terminate_backend`

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

[0.4.0]: https://github.com/owner/mcp-pgsql/releases/tag/v0.4.0
[0.3.1]: https://github.com/owner/mcp-pgsql/releases/tag/v0.3.1
[0.3.0]: https://github.com/owner/mcp-pgsql/releases/tag/v0.3.0
[0.2.0]: https://github.com/owner/mcp-pgsql/releases/tag/v0.2.0
[0.1.0]: https://github.com/owner/mcp-pgsql/releases/tag/v0.1.0
