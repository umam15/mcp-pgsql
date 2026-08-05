# Todo Proyek MCP PostgreSQL (mcp-pgsql)

- [x] Buat `requirements.txt` (mcp, psycopg2, python-dotenv)
- [x] Buat `server.py`: inisialisasi MCP server + koneksi PostgreSQL
- [x] Implementasikan tool `execute_sql` (jalankan query SQL sembarang)
- [x] Implementasikan tool `list_databases` (daftar database)
- [x] Implementasikan tool `get_schema` (skema tabel/kolom/indeks/constraint)
- [x] Konfigurasi env var: PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD, PGSSL
- [x] Uji coba server jalan & 3 tool merespons
- [x] Update `CHANGELOG.md` (fitur yang sudah jadi) & commit ke main
- [x] Verifikasi workflow Auto Release jalan (tag + release otomatis)

## Pengembangan Tool Lanjutan

- [x] Tool `list_schemas` (daftar skema di database)
- [x] Tool `describe_table` (detail satu tabel: kolom, tipe, PK, FK, default)
- [x] Tool `list_views` (daftar view di skema)
- [x] Tool `list_extensions` (daftar extension PostgreSQL terpasang)
- [x] Tool `get_table_stats` (estimasi row count & ukuran tabel)
- [x] Tool `explain_query` (jalankan `EXPLAIN` query untuk melihat rencana eksekusi)
- [x] Tool `get_running_queries` (lihat query aktif via `pg_stat_activity`)
- [x] Tool `kill_query` (terminate query berjalan via `pg_terminate_backend`)
- [x] Uji coba semua tool baru & update `CHANGELOG.md` (versi berikutnya)
