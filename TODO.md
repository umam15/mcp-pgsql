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

- [ ] Tool `list_schemas` (daftar skema di database)
- [ ] Tool `describe_table` (detail satu tabel: kolom, tipe, PK, FK, default)
- [ ] Tool `list_views` (daftar view di skema)
- [ ] Tool `list_extensions` (daftar extension PostgreSQL terpasang)
- [ ] Tool `get_table_stats` (estimasi row count & ukuran tabel)
- [ ] Tool `explain_query` (jalankan `EXPLAIN` query untuk melihat rencana eksekusi)
- [ ] Tool `get_running_queries` (lihat query aktif via `pg_stat_activity`)
- [ ] Tool `kill_query` (terminate query berjalan via `pg_terminate_backend`)
- [ ] Uji coba semua tool baru & update `CHANGELOG.md` (versi berikutnya)
