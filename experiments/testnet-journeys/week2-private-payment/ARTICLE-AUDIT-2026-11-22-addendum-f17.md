# Addendum — koreksi §6 F17 + pemeriksaan pra-commit (22 Nov 2026)

**Addendum untuk:** `ARTICLE-AUDIT-2026-11-22-r3.md`
(59.742 byte, SHA-256 `6a1be437ce51227286f23861615781c01d8e394c5a3b07ea34262ba785c6638f` —
file r3 TIDAK diubah; addendum ini mengoreksinya dengan merujuk.)
**Tanggal:** 22 Nov 2026, ~14:20 WIB.
**Ruang lingkup:** (A) koreksi klasifikasi §6 F17; (B) sapuan klasifikasi
serupa; (C) pemeriksaan isi dan kelayakan publikasi untuk daftar calon
commit 80 file (r3 §8.6). Tidak ada pengulangan audit, tidak ada
perubahan raw evidence, VO, atau comparator tersertifikasi. File video
asli (final 720p/1080p) dan chk-21/22 asli tidak diubah — versi publik
(`…-public.mp4`, `chk-21/22-public.jpg`) adalah turunan yang dibuat
pada ronde sanitasi (lihat C.6).
Tidak ada staging, commit, push, atau pengiriman tiket.
**Status:** review Anara selesai 22 Nov 2026 — substansi audit dan
seluruh keputusan disetujui. Otorisasi commit dan otorisasi push (dua persetujuan terpisah) masih menunggu.

## A. Koreksi §6 F17 — klasifikasi dipecah

**F17 di r3 (baris 486) — SALAH (menggabungkan):**

| # | Temuan | Label | Sumber + alasan |
|---|---|---|---|
| F17 | Statement[3–8] = nullifier, 3 commitment, alamat vault, fee | Verified fact | pencocokan nilai segar (§2.2) |

Masalahnya: baris ini menggabungkan statement[3–8] dalam satu label
"Verified fact", sehingga makna "fee" pada statement[8] ikut
terbaca sebagai fakta terverifikasi. Itu tidak benar.

**F17 yang benar (menggantikan baris di atas):**

| # | Temuan | Label | Sumber + alasan |
|---|---|---|---|
| F17a | Statement[3–7]: nullifier, tiga commitment, dan alamat vault | Verified fact | pencocokan nilai segar (§2.2): statement[3] = nullifier (sama dengan topic[3] log[0]); statement[4–6] = 3 commitment (sama dengan topic[2] log[1–3]); statement[7] = alamat vault `0x9c5ad5e5…` |
| F17b | Statement[8]: integer 4.416 × 10¹⁸ | Verified fact (integernya); unit RLS = interpretasi; makna "total fee" = inference | integer dibaca segar dari calldata (§2.2); unit RLS berasal dari tampilan aplikasi (lihat §3.2); makna "total fee" ditetapkan lewat tampilan aplikasi + aritmetika, bukan skema on-chain terverifikasi (§3.2) |

**Konsekuensi untuk klaim artikel:** klaim §7.5 nomor 3 di r3 sudah
benar ("the integer 4.416 × 10¹⁸ appears in the transaction's
statement. The app presents that integer as 4.416 RLS and as the
total fee" — verified fact untuk integer; inference untuk label RLS
dan makna total fee) dan tidak perlu diubah. Yang berubah hanyalah
klasifikasi F17 di §6.

## B. Sapuan klasifikasi serupa — F17 satu-satunya yang tersisa

Diperiksa seluruh penyebutan "total fee" dan 4,416 di r3 (grep,
22 Nov 2026). Hasil: **F17 adalah satu-satunya klasifikasi yang
masih menyebut 4,416 sebagai total fee terverifikasi.** Semua yang
lain sudah benar:

| Lokasi di r3 | Isi | Verdict |
|---|---|---|
| §2.2, baris 149 (statement[8]) | integer + "unit RLS dan makna 'total fee' adalah interpretasi" | benar |
| §3.1, baris 240–241 | integer = verified fact; unit RLS = interpretasi; "total fee" = inference | benar |
| §3.2, baris 249–288 | tiga lapis dipisahkan; "total fee" = inference | benar |
| §4.1, baris 339 | integer = verified fact; unit + makna = inference, "BUKAN fakta on-chain" | benar |
| §6 F6a/F6b, baris 474–475 | F6a integer = verified fact; F6b "total fee" = inference | benar |
| §6 F8, baris 477 | 3,84 = 4,416 − 0,576 = reconstruction; unit tiap suku dari sumber berbeda | benar |
| §6 F16, baris 485 | pemetaan 3 note = reconstruction; unit + makna "fee" = interpretasi | benar |
| §7.1, baris 511–512 | integer = verified fact; label RLS + makna "total fee" = inference | benar |
| §7.3, baris 587 | arti semantik "total fee" — integer terverifikasi, interpretasi inference | benar |
| §7.5 klaim 3, baris 631–635 | integer = verified fact; label RLS + "total fee" = inference | benar |
| §6 F17, baris 486 | statement[3–8] digabung sebagai verified fact, termasuk "fee" | **SALAH — diperbaiki di §A di atas** |

Sapuan frasa terkait di r3: 0 kemunculan "transfer lanjutan",
"moved 0.576 RLS to", dan "fee settlement" sebagai pernyataan fakta
(grep, 22 Nov 2026).

## C. Pemeriksaan isi dan kelayakan publikasi — daftar commit 80 file

**Metode.** Daftar file dari r3 §8.6.4 (71 untracked) + 9 tracked-modified
(§8.6.2) = 80 file, direkonstruksi dari `git status` dan diverifikasi
jumlahnya (80 baris). Pemeriksaan: (1) sapuan pola rahasia di seluruh
80 file (mnemonic, seed phrase, private key, api key, password,
bearer token, recovery phrase); (2) sapuan email dan nomor telepon;
(3) pencarian alamat wallet Binance Anara (`0x3D9F…`); (4) pembacaan
langsung 3 screenshot, draf tiket, dan sampel raw RPC responses;
(5) pemeriksaan `.gitignore`, ukuran total, dan sumber PDF.
Tidak ada file yang diubah dalam pemeriksaan ini.

### C.1 Hasil sapuan umum (80 file)

| Pemeriksaan | Hasil |
|---|---|
| Kecocokan pola rahasia | **10 kecocokan pola, bukan temuan rahasia.** Semuanya pernyataan meta: pernyataan di header script dan laporan run bahwa script tidak membutuhkan kredensial; satu kalimat pedoman di `scripts/README.md`; daftar hal yang tidak boleh disertakan (`RESEARCH-TRAIL.md:405`); dan uraian metode sapuan di dokumen ini sendiri (bagian C di atas) yang menyebut pola yang dicari. **Tidak ada rahasia asli.** |
| Email / nomor telepon | **0 temuan.** |
| Alamat wallet Binance Anara (`0x3D9F…`) | **0 temuan** di 80 file. |
| Ukuran total 80 file | **31.837.274 byte (~30,4 MB)** — angka untuk daftar ASLI (sebelum sanitasi). Terbesar saat itu: video 1080p asli 20.622.942 B, video 720p asli 8.523.526 B, PDF 904.036 B, `.src/index.html` 506.135 B. Daftar baru setelah sanitasi: **32.977.402 byte (~31,4 MB)** (lihat catatan ronde sanitasi di akhir dokumen); terbesar kini video 1080p publik 20.153.708 B dan video 720p publik 10.041.261 B. |

**Yang sengaja bersifat publik di dalam file-file ini** (bukan temuan):
username @anara / @kittynim, alamat EVM `0x0c5b…` / `0x680d…`
(dari registry publik + video), alamat relayer/vault/kontrak
(data on-chain publik), dan alamat `0x71af…` (argumen transfer
on-chain). Semua itu sudah publik melalui registry, explorer,
dan video eksperimen.

### C.2 runs/ — 20 file (3 run + README)

| Isi | Hasil |
|---|---|
| `runs/*/datasets/` (csv, checksums sha256, metadata json) — 9 file | Kecil (285–801 B). Data identitas jaringan (chain id, genesis, RPC). Layak publik. |
| `runs/*/findings/verified-facts/` (verification + complete report) — 4 file | Laporan Module 01 (2.964–33.459 B). Tidak ada data pribadi. Layak publik. |
| `runs/*/raw-data/rpc-responses/01_network_identity_raw.json` — 3 file (6.046 / 6.374 / 6.374 B; total 18.794 B) | **Dibaca langsung.** JSON-RPC publik testnet: `eth_chainId`, `eth_getBlockByNumber`, `eth_getCode`, dsb., beserta `rpc_endpoint`, `retrieved_at_utc`, `http_status`, `attempts`. Sapuan sensitif di ketiganya: **0 temuan**. Layak publik. |
| `runs/*/scripts/01_network_identity.py` — 3 file | Stdlib, read-only; header menyatakan "No private key, no wallet, no API secret". Layak publik. |
| `runs/README.md` (7.705 B) | Dokumentasi run. Layak publik. |

### C.3 Screenshots — 3 file dalam batch (dilihat langsung)

| File | Isi | Verdict |
|---|---|---|
| `raw-data/screenshots/chk-21-public.jpg` (121.762 B) | Home wallet @kittynim: saldo, EVM `0x680D…0eFC`; baris kunci "Enygma Spend" dan "Enygma View" disamarkan (blur) — nilai heksanya tidak dicantumkan dalam addendum ini | Layak publik (versi sanitasi — lihat C.6) |
| `raw-data/screenshots/chk-22-public.jpg` (127.132 B) | Home wallet @kittynim, scroll sedikit berbeda: saldo + "NFTs: None yet"; baris kunci Spend/View yang sama disamarkan (blur) | Layak publik (versi sanitasi — lihat C.6) |
| `raw-data/screenshots/chk-23.jpg` (86.426 B) | Halaman Receive @kittynim: QR + alamat EVM lengkap `0x680D90983da58Bcb7d127e3421193274e84E0eFC` | Layak publik (alamat sudah di registry + video) |

File asli `chk-21.jpg` (86.116 B) dan `chk-22.jpg` (92.135 B) adalah **local-only**: tidak diubah, tidak disanitasi, dan dikecualikan dari batch (lihat C.6).

### C.4 Sumber PDF — `.src/index.html` (506.135 B)

- Sumber build PDF 21 Nov (`01_tx_audit_complete_history.pdf`, 904.036 B).
  Menyebut `09edab2b` 125×. Teks lama "(the check has not been run yet)"
  muncul **tepat 1×** — sudah didokumentasikan di finalisasi 22 Nov
  sebagai artefak historis yang sengaja dipertahankan (mengeditnya
  akan membuat sumber berbeda dari PDF yang sudah dibangun).
- Layak publik **dengan catatan itu** (tidak ada perubahan yang
  diusulkan di ronde ini).

### C.5 Draf tiket — `tickets/rayls-team-questions-draft-2026-11-22.md` (10.268 B, dibaca penuh)

Draf ini **belum dikirim** dan ditandai DRAFT. Isinya sudah diperiksa:
tidak ada data pribadi, rahasia, atau alamat wallet Anara. Namun
draf ini memuat **5 klasifikasi yang sudah kedaluwarsa terhadap r3**
dan harus diperbarui sebelum commit atau sebelum dikirim:

| Lokasi di draf | Tertulis sekarang | Seharusnya (menurut r3 + addendum ini) |
|---|---|---|
| Q5, Verified facts | "Calldata `statement[8]` = 4.416 RLS total fee (verified fact, on-chain)" | Integer 4.416 × 10¹⁸ = verified fact; unit RLS = interpretasi; "total fee" = inference |
| Q5, Verified facts | "Chain gas for the tx = 0.063168048 RLS (verified fact, receipt)" | 0.063168048 unit gas native (verified fact angkanya); unit RLS belum pasti — teks aplikasi bertentangan (RLS vs USDr, r3 §3.3 / Q-B) |
| Q6, Verified facts | "statement[3]–statement[8] are verified by value matching (vault binding, fee total 4.416 RLS, etc.)" | statement[3–7] verified by value matching; statement[8] integer verified, "fee total" inference (koreksi F17, §A) |
| Q7, Verified facts | "It received the 0.576 RLS settlement 4 blocks after the shielded transfer" | Transaksi terpisah memanggil transfer() dengan argumen (`0x71af…`, 0.576 RLS); tujuan transfer unknown — jangan sebut "settlement" sebagai fakta (r3 koreksi 5) |
| Q10, Verified facts | "The 0.576 RLS settlement arrived as a separate ERC-20 transfer 4 blocks later." | Sama seperti Q7: netralkan "settlement" menjadi pemanggilan transfer() dengan argumennya |

**Rekomendasi:** perbarui draf dulu (butuh persetujuan Anara untuk
mengedit — tidak dilakukan di ronde ini), ATAU keluarkan draf dari
batch commit ini dan commit setelah diperbarui. Jangan commit draf
apa adanya, karena klasifikasinya bertentangan dengan r3.
**Resolusi (22 Nov 2026, keputusan Anara): dikeluarkan dari batch
commit ini.** Draf disimpan sebagai draf lokal untuk revisi terpisah;
tidak diperbarui atau dikirim pada tahap ini.

### C.6 Temuan dan resolusi sanitasi

- chk-21 dan chk-22 menampilkan fragmen kunci **Enygma Spend**
  dan **Enygma View** milik akun @kittynim — yang tampak hanya
  10 karakter awal + 8 karakter akhir dari tiap kunci, sehingga kunci
  lengkap **tidak dapat dipulihkan** dari gambar tersebut. Nilai
  heksanya tidak dicantumkan dalam addendum ini. File asli **tidak
  disanitasi** (tidak diubah sama sekali); yang disamarkan hanyalah
  versi publiknya (lihat resolusi di bawah). Akunnya adalah testnet
  publik tanpa nilai nyata.
- **Yang sama juga ada di video:** frame footage mentah `raw_003.jpg`
  (layar home @kittynim yang sama, yang masuk ke video final)
  menampilkan fragmen kunci yang sama. Jadi mengeluarkan kedua
  screenshot saja **tidak** menghilangkan fragmen itu dari repo —
  video final **asli** (720p + 1080p, sebelum sanitasi) memuatnya juga.
  Video **publik** hasil sanitasi tidak lagi menampilkan fragmen
  tersebut (baris kunci di-blur pada rentang kemunculannya).
- Ini bukan kebocoran kunci lengkap, tetapi materi yang berkaitan
  dengan kunci. **Resolusi (22 Nov 2026, keputusan Anara): sanitasi
  sebelum publikasi.** Salinan publik `chk-21-public.jpg` dan
  `chk-22-public.jpg` dibuat dengan baris kunci disamarkan (blur);
  versi publik video 720p dan 1080p dibuat dengan fragmen yang sama
  disamarkan pada rentang waktu kemunculannya. File asli (chk-21,
  chk-22, kedua video final) **tidak** ditimpa atau dihapus — hash
  aslinya dipertahankan — tetapi **dikeluarkan dari batch publik**
  dan dikecualikan lewat `.gitignore` (exact-path).

### C.7 Ringkasan verdict per kelompok (80 file)

| Kelompok | Jumlah | Verdict |
|---|---|---|
| 9 tracked-modified (README) | 9 | Layak publik |
| `.gitignore`, INDEX, REPRODUCE, RESEARCH-TRAIL, 01-no-overwrite-fix-report | 5 | Layak publik (INDEX/TRAIL/REPRODUCE sudah diperbarui untuk merujuk r3 + addendum ini — lihat catatan ronde sanitasi) |
| `audit-reports/` (laporan awal + README) | 2 | Layak publik |
| `contracts/addresses/addresses.json` | 1 | Layak publik (alamat publik) |
| `experiments/g1-g6-decision-table.md` | 1 | Layak publik |
| Journey (r3 + addendum + EDIT-PLAN + QA + README + 2 build script + 2 video publik + manifest + subs) | 11 | Layak publik (r3 = laporan berlaku; addendum = koreksi F17; video publik sudah disanitasi — lihat C.6; video asli dikeluarkan dari batch) |
| TX package (`.src/` + PDF + laporan + decoded + manifest + raw) | 24 | Layak publik (`.src/index.html` dengan catatan teks lama ×1 — lihat C.4) |
| `raw-data/screenshots/` | 3 | chk-23 layak; chk-21/22 asli dikeluarkan, diganti versi publik yang sudah disanitasi (lihat C.6) |
| `runs/` | 20 | Layak publik |
| `scripts/` (4 script) | 4 | Layak publik |
| `tickets/` draf | 0 | **Dikeluarkan dari batch commit ini** (draf lokal, revisi terpisah — lihat C.5) |
| **Total diusulkan** | **80** | — |

## D. Status keputusan Anara

1. Koreksi F17 di §A — **DISETUJUI** (22 Nov 2026). Gunakan pemisahan
   F17a/F17b; klaim §7.5 nomor 3 tetap.
2. chk-21/chk-22 — **DIPUTUSKAN: sanitasi sebelum publikasi** (lihat C.6).
   Versi publik dibuat; file asli dikeluarkan dari batch.
3. Draf tiket — **DIPUTUSKAN: dikeluarkan dari batch commit ini.**
   Disimpan sebagai draf lokal untuk revisi terpisah; tidak diperbarui
   atau dikirim pada tahap ini.
4. Pembaruan INDEX/TRAIL/REPRODUCE untuk merujuk r3 (+ addendum ini) — **SELESAI** (22 Nov 2026). INDEX, RESEARCH-TRAIL, dan REPRODUCE sudah diperbarui; journey README juga diperbarui.
5. Persetujuan commit — **belum ada**.
6. Persetujuan push — **belum ada** (persetujuan terpisah dari commit; push hanya dilakukan setelah commit disetujui dan dibuat).

**Catatan hitungan (diperbarui ronde sanitasi, 22 Nov 2026):** daftar
80 file di r3 §8.6 adalah baseline yang direview. Setelah keputusan
sanitasi, daftar calon commit menjadi **80 file baru** (jumlah sama,
komposisi berubah): draf tiket keluar (−1), 4 file asli keluar (−4:
2 video final + chk-21/22), 4 versi publik masuk (+4: 2 video publik
+ chk-21/22-public), dan addendum ini masuk (+1). Jadi 80 − 1 − 4 + 4
+ 1 = 80 file (9 tracked + 71 untracked). Tabel C.7 di atas sudah
mencerminkan komposisi baru ini. r3 §8.6 tidak diubah dalam ronde ini.

## Lampiran — verifikasi ronde ini

- r3 tidak diubah: SHA-256 `6a1be437ce51227286f23861615781c01d8e394c5a3b07ea34262ba785c6638f`
  (diperiksa ulang ronde ini). r2: 48.097 byte / `00e464f2…` (tidak berubah).
  r1: 35.269 byte / `bd54c362…` (tidak berubah).
- Comparator v2.1.1 tidak disentuh: `bfef1f667408b227cac5b33e27c9352b5ad721ca0b78ed91899d8befdcac08a3`.
- Footage `610a5cd3…` + VO `ebb2fdda…` tidak berubah (diperiksa ulang ronde ini).
- Manifest journey 12/12 adalah hasil pemeriksaan pra-commit ronde ini, sebelum sanitasi (12 entri). Setelah sanitasi, manifest diperbarui menjadi 16 entri (12 entri lama + 4 versi publik baru; 4 file asli ditandai local-only) dan terverifikasi 16/16 — lihat catatan ronde sanitasi. TX 20/20, verifier 23/23 PASS (dijalankan ulang).
- Git: 28 baris status, 0 staged, tidak ada commit/push.

## Catatan ronde sanitasi (22 Nov 2026, ~14:30 WIB)

Keputusan Anara (review addendum r3) dilaksanakan penuh di ronde ini:

1. F17 disetujui — pemisahan F17a/F17b sesuai §A; klaim §7.5 nomor 3 tetap.
2. Sanitasi: versi publik `chk-21-public.jpg` (121.762 B,
   `f62fd012…`) dan `chk-22-public.jpg` (127.132 B, `9158ffa9…`) dibuat
   (PIL GaussianBlur r=25 pada baris kunci; diverifikasi dengan melihat
   langsung — baris kunci tidak terbaca, saldo dan UI lain utuh);
   video publik 720p (10.041.261 B, `b5c91ee1…`) dan 1080p
   (20.153.708 B, `e1e7a339…`) dibuat (ffmpeg boxblur pita header pada
   t 20–24, 82–88, 109–115, 138–144, 176–185,533 dtk; diverifikasi satu
   frame per rentang + kontrol t=60 dtk tanpa blur). File asli tidak
   ditimpa/dihapus (hash dipertahankan di manifest journey) dan
   dikeluarkan dari batch lewat `.gitignore` exact-path.
3. Draf tiket dikeluarkan dari batch commit saat ini; disimpan sebagai
   draf lokal untuk revisi terpisah; tidak diperbarui atau dikirim.
4. INDEX, RESEARCH-TRAIL, REPRODUCE diperbarui untuk merujuk r3 +
   addendum ini dan versi publik; journey README diperbarui; manifest
   journey 16/16 terverifikasi.
5. Daftar calon commit baru: **80 file, 32.977.402 byte (~31,4 MB)**
   (9 tracked + 71 untracked). Dikeluarkan: draf tiket (klasifikasi
   kedaluwarsa), 2 video final asli + chk-21/22 asli (fragmen kunci),
   r1/r2 (superseded). Verifikasi akhir ronde ini: manifest journey
   16/16, TX 20/20, verifier 23/23 PASS; r3 `6a1be437…`, comparator
   `bfef1f66…`, footage `610a5cd3…`, VO `ebb2fdda…` tidak berubah;
   sapuan fragmen kunci di daftar baru: 0; sapuan rahasia: hanya
   pernyataan meta; email/telepon: 0; wallet Binance `0x3D9F…`: 0.
   Git: 28 baris status, 0 staged. Tidak ada staging, commit, push,
   atau pengiriman tiket. Otorisasi commit dan otorisasi push (dua
   persetujuan terpisah) masih menunggu.
