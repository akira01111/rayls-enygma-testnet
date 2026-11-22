# Laporan Perubahan — Modul 01: Perbaikan No-Overwrite (v1.0.0 → v2.0.0)

Tanggal: 21 Nov 2026 ~12:55 WIB
Status: perbaikan selesai, belum commit/push, menunggu review kedua Anara.
Modul 02 tidak dimulai.

## Masalah yang ditemukan (review Anara, 21 Nov 2026)

Script v1.0.0 memakai nama file tetap dan mode write (`"w"`), sehingga
menjalankannya ulang akan menimpa raw JSON, CSV, metadata, checksums,
dan report dari run sebelumnya. Tidak ada identitas run, dan manifest
checksum tidak mencakup script maupun verification report.

## Yang diubah — per poin permintaan

### 1. Unique run ID berdasarkan timestamp UTC
- Setiap execution membuat `run_id` dari waktu mulai dalam UTC,
  format `YYYYMMDDTHHMMSSZ` (contoh: `20261121T054711Z`).
- Fungsi `new_run_id()`; run ID dicatat di raw JSON, metadata, dan report.

### 2. Setiap run menyimpan output di lokasi berbeda
- Semua output kini berada di `runs/<run_id>/` dengan layout yang sama
  seperti sebelumnya di dalam direktori run itu:
  `raw-data/rpc-responses/`, `datasets/`, `findings/verified-facts/`,
  plus `scripts/` untuk salinan script.
- Tidak ada lagi penulisan ke lokasi kanonik `raw-data/`, `datasets/`,
  `findings/` di root repo.

### 3. Script menolak overwrite jika file bukti sudah ada
- Direktori run dibuat dengan `exist_ok=False`; direktori yang sudah
  ada tidak pernah dipakai ulang.
- Jika `runs/<run_id>` sudah ada, run ID mendapat akhiran `-2`, `-3`,
  dst. sehingga run baru tidak pernah menyentuh run lama.
- Semua file ditulis dengan mode eksklusif (`"x"`, via
  `write_text_exclusive` / `write_bytes_exclusive` /
  `write_json_exclusive`). Jika sebuah file sudah ada, script berhenti
  dengan exit code 2 dan tidak menulis file lain.
- Terbukti dengan tes terisolasi (tanpa menjalankan script): penulisan
  kedua ke file yang sama ditolak dan isi file tidak berubah.

### 4. Raw JSON tidak boleh dimodifikasi setelah capture selesai
- Raw JSON ditulis sekali (mode `"x"`) segera setelah 4 RPC call
  selesai, lalu langsung `chmod 0o444` (read-only).
- Script tidak pernah membuka raw JSON untuk ditulis lagi.
- Salinan script di dalam run dir juga `chmod 0o444`.
- Perubahan apa pun setelahnya tetap terdeteksi lewat manifest SHA256.

### 5. SHA256 script Python dan verification report masuk ke manifest
- `datasets/01_network_identity_checksums.sha256` kini berisi 5 entri:
  raw JSON, metadata, CSV, salinan script, dan verification report.
- Manifest ditulis PALING AKHIR (setelah report selesai) agar hash
  report bisa ikut tercatat. Report sendiri mencantumkan hash raw,
  metadata, CSV, dan script, plus catatan bahwa manifest mencakup
  report itu sendiri.
- Script juga menyimpan salinan byte-identik dari dirinya sendiri di
  `runs/<run_id>/scripts/01_network_identity.py`, sehingga setiap run
  mandiri: kode yang menghasilkannya ikut tersimpan.

### 6. Metadata mencatat run ID dan versi script
- `datasets/01_network_identity_metadata.json` kini berisi `run_id`,
  `run_dir`, `script_version` (v2.0.0), `script`, `script_copy`, dan
  `script_sha256`.
- Report juga menampilkan Run ID, Run directory, dan versi script.

### 7. Bukti run sebelumnya tidak dihapus atau diganti
- Bukti run PASS 21 Nov 05:47:11 UTC dipindahkan byte-identik dari
  lokasi kanonik ke `runs/20261121T054711Z/` (bukan disalin lalu dihapus
  isinya — `mv`, isi byte sama).
- SHA256 diverifikasi sama sebelum dan sesudah pemindahan:
  - script v1.0.0: `39caa42b31b928b814c3317ded316fbade8db498bcf7031619d272702a05be4b`
  - raw JSON: `2131d69031ca3b8e085004a807e8ebd169780c12c25b68afd1c0f3e8124fb85c`
  - CSV: `156c0b719499d212f3ba096c38b188c669463f6fd0069cf42b34aaadc4db9282`
  - metadata: `8d4e60119fce820f605007684ac834c3f50e1e1523d8a470a43405578620208f`
  - checksums: `7b730708c59c7f848fad8d2a5d5e3c7304287d081db050cb82b2f000ef5c84b6`
  - verification report: `aa544d470d734c90b154e099d50bff23bbf6cc590ca6eced83dbadc898a74eb8`
- Raw JSON dan salinan script v1.0.0 di run dir berstatus read-only
  (`-r--r--r--`).
- File gabungan (complete report) diregenerasi ke dalam run dir dengan
  isi pengamatan yang sama; yang berubah hanya referensi path dan satu
  catatan pemindahan/versi. File gabungan lama di
  `findings/verified-facts/` dihapus karena sudah digantikan versi
  run-dir.
- Satu pengecualian yang disengaja: metadata run lama TIDAK ditambahi
  field `run_id`/`script_version`, karena mengubahnya akan mengubah
  hash dan merusak bukti. Run ID dan versi script run lama dicatat di
  `runs/README.md` dan di file gabungan.

## Yang TIDAK dilakukan
- Script v2.0.0 TIDAK dijalankan ulang (tidak ada run baru). Yang
  dicek: `python3 -m py_compile` (lolos) dan tes logika terisolasi
  untuk run ID, tabrakan direktori, dan penolakan overwrite (lolos,
  tanpa network dan tanpa menyentuh bukti).
- Hasil pengamatan sebelumnya TIDAK diubah (chain ID, blok, hash,
  timestamp, dan status PASS tetap sama).
- TIDAK ada commit atau push.
- Modul 02 TIDAK dimulai.

## Verifikasi yang dilakukan
1. `python3 -m py_compile scripts/01_network_identity.py` — OK.
2. Tes terisolasi (import modul, tanpa network):
   - format run ID `YYYYMMDDTHHMMSSZ` — OK;
   - direktori run yang sudah ada → akhiran `-2` — OK;
   - run ID bebas dipakai apa adanya — OK;
   - penulisan teks kedua ke file yang sama ditolak, isi tidak berubah — OK;
   - penulisan bytes kedua ditolak — OK.
3. SHA256 keenam file bukti sama persis sebelum dan sesudah pemindahan
   (daftar di atas).
4. `git status`: hanya file baru yang belum terlacak (`runs/`,
   `scripts/01_network_identity.py`); tidak ada commit/push.

## File yang berubah / ditambah
- Diubah: `scripts/01_network_identity.py` (v1.0.0 → v2.0.0, 23.497 byte).
- Dipindah (byte-identik): 6 file bukti run 20261121T054711Z ke
  `runs/20261121T054711Z/` + salinan script v1.0.0 ke
  `runs/20261121T054711Z/scripts/`.
- Diregenerasi: `runs/20261121T054711Z/findings/verified-facts/01_network_identity_complete_report.md`
  (33.445 byte; path diperbarui + catatan pemindahan).
- Ditambah: `runs/README.md` (layout run + tabel run).
- Dihapus: `findings/verified-facts/01_network_identity_complete_report.md`
  (versi lama, sudah digantikan versi run-dir).
- Ditambah: file laporan ini, `01-no-overwrite-fix-report.md`.

## Catatan
- File gabungan untuk review saat ini berformat Markdown (.md). Jika
  Anara menginginkan ekspor PDF sungguhan dari file gabungan itu,
  tinggal diminta — belum dibuat.
- Perilaku run berikutnya: `python3 scripts/01_network_identity.py`
  akan membuat `runs/<timestamp-UTC-sekarang>/` yang baru dan tidak
  menyentuh `runs/20261121T054711Z/` sama sekali.

## Pembaruan — 21 Nov 2026 (review kedua Anara)

Review kedua Anara (21 Nov 2026 ~13:18 WIB): hasil umum bagus, data run
pertama PASS 9/9 dan perbaikan no-overwrite sudah dilakukan. Sebelum
commit/push, diminta tugas A–D di bawah. Belum ada commit/push.
Modul 02 tidak dimulai.

### A. Verifikasi checksum sumber (tugas A)

- Perintah yang diminta dijalankan dari root repo: manifest tercetak,
  tetapi `sha256sum -c datasets/01_network_identity_checksums.sha256`
  dari dalam `runs/20261121T054711Z/` GAGAL dengan "No such file or
  directory" untuk ketiga file. Penyebab: manifest v1.0.0 memakai nama
  file telanjang (tanpa path), sedangkan file berada di
  `raw-data/rpc-responses/` dan `datasets/`. Manifest v1.0.0 tidak
  bisa diverifikasi langsung dengan `sha256sum -c` dari direktori
  mana pun — ini cacat format manifest v1.0.0, bukan kerusakan bukti.
- Verifikasi pengganti (tidak mengubah file): keenam file lama dihitung
  SHA256-nya dan dicocokkan dengan daftar hash di laporan ini (§7) —
  keenamnya OK (script v1.0.0, raw JSON, CSV, metadata, checksums,
  verification report). Ketiga entri manifest juga dicocokkan satu per
  satu dengan file sebenarnya — ketiganya OK.
- Manifest v2.0.0 ke atas memakai path relatif terhadap run dir
  (5 entri) dan bisa diverifikasi langsung dengan `sha256sum -c` dari
  dalam run dir (lihat `runs/README.md`).

### B. Script v2.0.1 (tugas B)

- Versi baru: `2.0.1` (patch atas 2.0.0). Data run v1.0.0 TIDAK diubah.
- Validasi respons JSON-RPC (baru): setiap respons diperiksa — versi
  `jsonrpc` harus `"2.0"`, `id` respons harus sama dengan `id`
  request, tidak ada objek `error`, field `result` harus ada, dan
  result harus berbentuk sesuai metode (hex string untuk
  eth_chainId/eth_blockNumber; objek blok dengan number/hash/timestamp
  untuk eth_getBlockByNumber). Hasil validasi dicatat per call di raw
  JSON (`validation: {ok, problems}`) dan sebagai 4 check
  `response_valid_*` baru. Total check kini 13 (sebelumnya 9).
- Validasi hash penuh (baru): hash harus `0x` + tepat 64 digit hex
  (`is_full_hash`); hash pendek atau bukan hex membuat check FAIL
  dengan detail yang menyebut nilainya.
- Nama check drift diperjelas (diubah): `block_number_matches_latest_block`
  → `block_number_within_drift_of_latest_block`. Nama lama memberi kesan
  kedua angka harus sama persis; nyatanya check mengizinkan blok latest
  0–10 blok di depan, tidak pernah di belakang. Detail check menyebut
  batasnya secara eksplisit.
- Penanganan malformed response / nilai tidak valid (baru): semua parsing
  lewat helper aman (`parse_hex_int`, `is_full_hash`,
  `block_timestamp_iso`) yang mengembalikan None, bukan exception.
  Evaluasi check dipindah ke fungsi `evaluate()` yang tidak pernah raise
  atas data malformed: nilai tidak valid menjadi FAIL dengan detail jelas
  (mis. "hash is not a full 64-hex hash", "cannot compare"), dan run
  tetap menulis semua output dengan status FAIL (exit 1).
- Klarifikasi raw JSON (baru): docstring + report menjelaskan raw JSON
  adalah struktur response yang ditangkap dan diserialisasi (objek
  request + respons JSON yang sudah di-parse + metadata transport),
  BUKAN byte-level HTTP capture (tidak ada byte HTTP mentah, header,
  atau data TLS).
- Root path arsip (baru): `find_repo_root()` berjalan naik dari file
  script sampai menemukan direktori yang berisi `scripts/` DAN `runs/`.
  Salinan arsip yang dijalankan dari `runs/<run_id>/scripts/` tetap
  menemukan root repo dan menulis run baru di `runs/` repo, tidak pernah
  di dalam run arsip. Jika tidak ditemukan, script menolak jalan
  (exit 2) dengan pesan jelas.
- Metadata kini juga mencatat `checks_total` dan `checks_passed`.
- Tes terisolasi (tanpa network, tanpa menyentuh bukti): 39/39 lolos —
  validasi respons (baik/salah id/salah versi/error object/result
  hilang/result bukan hex/blok null/blok bukan dict/hash pendek/
  transport gagal/respons bukan dict/HTTP 500), parsing aman,
  `evaluate()` dengan data bagus (PASS 13/13), data sampah (FAIL tanpa
  exception), semua call mati (FAIL, 0 lolos), root path (live, arsip,
  di luar repo), run ID, tabrakan direktori, penolakan overwrite.
  `python3 -m py_compile` lolos. Script v2.0.1: 35.544 byte.

### C. Dokumentasi (tugas C)

- `runs/README.md`: dibedakan file yang dibuat otomatis oleh script
  (6 file; 5 di antaranya tercakup manifest) dengan combined review
  report (dibuat proses terpisah, BUKAN oleh script, TIDAK tercakup
  manifest, hanya salinan baca). Ditambah instruksi verifikasi manifest
  (`sha256sum -c` dari dalam run dir) dan penjelasan bahwa manifest
  tidak meng-hash dirinya sendiri, plus catatan cacat format manifest
  v1.0.0 (nama file telanjang).
- Catatan pembaruan ini: PDF gabungan SUDAH diekspor pada 21 November
  2026 — 9 PDF di `pdf/` (file gabungan 16 halaman, script v2.0.0
  11 halaman, raw JSON 4 halaman, laporan perubahan 3 halaman,
  verification report 2 halaman, sisanya 1 halaman). Semua lolos gate
  render dan dicek isi + halamannya. Catatan lama di § Catatan ("PDF
  gabungan belum dibuat") tetap dipertahankan sebagai riwayat dan kini
  sudah tidak berlaku.
- Seluruh catatan historis di laporan ini dipertahankan; bagian ini
  hanya menambah, tidak menulis ulang.

### D. Run validasi v2.0.1 (tugas D)

- Dua run RPC read-only (hanya eth_chainId, eth_blockNumber,
  eth_getBlockByNumber; tanpa transaksi testnet, tanpa wallet):
  - Run 1 — `20261121T063234Z` (06:32:34 UTC): PASS 13/13. Chain ID
    7295799, blok latest 24805207 (drift +5), genesis hash sama dengan
    run lama. Manifest 5/5 OK (`sha256sum -c` dari run dir).
  - Run 2 (final) — `20261121T063327Z` (06:33:27 UTC): PASS 13/13.
    Chain ID 7295799, blok latest 24805303 (drift +4), genesis hash
    sama dengan run lama. Manifest 5/5 OK. Script live dan salinan
    script di run dir memiliki hash yang sama
    (`5ff78700346b2ebd0c1a1e14c2f615b3fd4d422bb7cbbec489b3d48743260ae0`).
- Koreksi nama check di antara kedua run (bukan perubahan perilaku):
  run 1 memakai nama pendek `response_valid_latest` /
  `response_valid_genesis`, sedangkan docstring v2.0.1 sudah menulis
  nama panjang. Kode diselaraskan ke docstring (label saja) dan
  validasi diulang sebagai run 2. Tes terisolasi diperbarui (40/40
  lolos, termasuk assert nama check persis).
- Bukti run lama TIDAK tersentuh: keenam hash run 20261121T054711Z
  masih sama dengan daftar §7; manifest run 1 juga masih 5/5 OK
  setelah run 2 dibuat.
- Retry tercatat di raw JSON run final: eth_chainId 3 attempt,
  eth_getBlockByNumber latest 2 attempt, sisanya 1 attempt
  (proxy sempat memutus koneksi; semua berhasil).
- Tidak ada combined report untuk run baru (dibuat proses terpisah,
  bila diminta).
- Belum ada commit/push. Modul 02 tidak dimulai.

## Pembaruan — 21 Nov 2026 (review ketiga Anara)

Review ketiga Anara (21 Nov 2026 ~14:17 WIB): paket PDF riwayat lengkap
dan struktur audit diterima. Sebelum review commit, diminta klarifikasi
ukuran build di bawah. Belum ada commit/push. Modul 02 tidak dimulai.

### Klarifikasi ukuran build v2.0.1

- Angka "Script v2.0.1: 35.544 byte" di §B di atas mengacu pada build
  yang dipakai run pertama v2.0.1, `20261121T063234Z`: salinan script
  `runs/20261121T063234Z/scripts/01_network_identity.py`, 35.544 byte,
  SHA256
  `c09d88eb835ba69d9a6bf4ee8d976584a709b97d140fd379b39385f5050701e0`.
- Build yang dipakai run final v2.0.1, `20261121T063327Z`, berukuran
  35.650 byte: salinan script
  `runs/20261121T063327Z/scripts/01_network_identity.py`, SHA256
  `5ff78700346b2ebd0c1a1e14c2f615b3fd4d422bb7cbbec489b3d48743260ae0`.
  Script live (`scripts/01_network_identity.py`) byte-identik dengan
  build ini (35.650 byte, hash sama).
- Selisih 106 byte adalah perubahan label dua nama check
  (`response_valid_latest` / `response_valid_genesis` →
  `response_valid_eth_getBlockByNumber_latest` /
  `response_valid_eth_getBlockByNumber_genesis`); bukan perubahan
  perilaku validasi. Kedua hash script tetap dicantumkan di atas dan
  di `runs/README.md` (bagian "Two v2.0.1 script builds"), dan keduanya
  tercakup manifest run masing-masing (terverifikasi 5/5 OK).

### Erratum docstring raw JSON

- Documentation erratum untuk kalimat terakhir docstring v2.0.1
  ("Raw data is written exactly as received...") dicatat di
  `runs/README.md` (bagian "Documentation erratum — v2.0.1 docstring
  (raw data wording)"), beserta kalimat pengganti yang direkomendasikan
  untuk versi berikutnya. Script v2.0.1 dan salinan historisnya tidak
  diubah.
- PDF riwayat lengkap Modul 01 dibuat ulang dalam putaran ini dengan
  `runs/README.md` terbaru (7.705 byte) dan laporan perubahan ini,
  termasuk erratum tersebut; file bukti tidak diubah.
