# Audit terarah — "What Can the Public Actually See When Two Accounts Make a Private Transfer on Rayls Enygma?"

**Tanggal audit:** 22 Nov 2026, ~13:24–14:10 WIB
**Ruang lingkup:** eksperimen dua akun 21 Nov 2026 yang dilakukan
dengan akun @anara (pengirim, menurut aplikasi) dan @kittynim
(penerima, menurut aplikasi), 6 RLS (menurut aplikasi) + video
eksperimen + paket bukti TX `0x09edab2b…` SAJA. Atribusi transaksi
on-chain kepada kedua akun tersebut adalah **reconstruction**
(bukti aplikasi + registry + kecocokan transaksi) — bukan fakta
on-chain, karena tidak ada alamat pengguna di dalam transaksi
(lihat koreksi 1, §6 F15).
**Bukan ruang lingkup:** audit Rayls keseluruhan; inventaris 511 transaksi
jaringan; eksperimen baru; transaksi on-chain baru.
**Metode:** video ditonton penuh (final 185,5 dtk + footage mentah 241,7 dtk,
transkripsi VO lokal + 24 frame dibaca); seluruh angka/alamat diturunkan
ulang dari file raw (bukan dari laporan sebelumnya); laporan lama hanya
dipakai sebagai pembanding, dan setiap penyimpangan dicatat.
**Status:** laporan audit + daftar calon commit. BELUM di-commit, BELUM
di-push. Menunggu review Anara.

**Revisi r3 (22 Nov 2026, ~14:00 WIB):** file ini merevisi
`ARTICLE-AUDIT-2026-11-22-r2.md` (dipertahankan sebagai catatan)
berdasarkan review Anara atas r2 — empat koreksi:
(1) baris §4.1 dan seluruh penyebutan 4,416 dibedakan tiga lapis:
integer mentah di statement, interpretasi unit RLS, dan interpretasi
"total fee";
(2) klaim §7.5 nomor 4 memakai "user-level sender/receiver" agar
tidak tertukar dengan relayer sebagai public transaction sender;
(3) ukuran dan SHA-256 r2 dicocokkan ke file canonical
(48.097 byte, SHA `00e464f2…`) — angka 47.530 byte di §8.5 r2
adalah pengukuran intermediate sebelum §8.4 dipulihkan (lihat §8.5);
(4) daftar persis file yang diusulkan masuk commit ditambahkan
(§8.6), beserta output lengkap `git status --short`.

## 1. Pencocokan video ↔ transaksi

### 1.1 Urutan aktivitas (video final, diverifikasi ke footage mentah)

Label akun (@anara / @kittynim) dan angka saldo di tabel ini adalah
**tampilan aplikasi** (direct observation). Kaitan aktivitas-aktivitas
ini dengan transaksi on-chain `0x09edab2b…` adalah **reconstruction**
(koreksi 1): aplikasi menampilkan tx yang sama di Activity kedua akun,
registry memetakan kedua username ke alamat, dan waktu/blok cocok —
tetapi tidak ada field on-chain yang menyatakan "tx ini adalah
pembayaran @anara ke @kittynim".

| # | Waktu video | Aktivitas | Bukti layar | Cocok on-chain |
|---|---|---|---|---|
| 1 | ~0–15 dtk | Akun @anara: $RLS Public 260,1335 / Shielded 14,324 / Total 274,4576; $USDr 0,01 / 4,9775 / 4,9875 | frame f_001 + raw_001 | Saldo adalah tampilan aplikasi (bukan data on-chain langsung) — lihat 1.3 |
| 2 | ~15–30 dtk | Akun @kittynim: $RLS Public 17,8252 / Shielded 321,4 / Total 339,2252; $USDr 5 / 7 / 12 | frame f_002 + raw_003 | Sama — tampilan aplikasi |
| 3 | ~30–45 dtk | Halaman Send $RLS, Shielded, To @kittynim (0x680D…8eFC), "can receive shielded payments", Shielded: 14,324, Amount 0,00 | frame f_003 + raw_005 | Username→alamat cocok dengan registry (lihat 2.3) |
| 4 | ~45–60 dtk | Amount 6 $RLS; Fees 4,42 $RLS ("3.84 gas + 0.58 Rayls Foundation (15%)") | frame f_004 | 4,42 = 3,84 + 0,58 (tampilan dompet; lihat §3) |
| 5 | ~60–75 dtk | Passkey confirm → "Approve" ✓ → "Pick your notes and encrypt" ✓ → "Make the zero-knowledge proof" (loading proving key, 4,8 dtk) | frame f_005 + raw_006 (prompt passkey) + raw_007 (tooltip ZK) | Prompt passkey + tooltip hanya ada di footage mentah, tidak di final |
| 6 | ~75–90 dtk | Sukses: "Sent 6 $RLS to @kittynim, privately", proof 256 bytes, "Made in 10 s, in this tab", fee 4,42 $RLS, tx 0x09edab2b…eff525bb | frame f_006 + raw_008 | Tx cocok penuh (lihat §2) |
| 7 | ~90–105 dtk | @anara: Shielded 14,324 → 3,908; Total 264,0416; $USDr tidak berubah | frame f_007 | Selisih 10,416 = 6 + 4,416 (aritmetika dari tampilan saldo) |
| 8 | ~105–120 dtk | @kittynim Activity: "Received +6 $RLS, 21 Nov 2026, 16:40", tx 0x09edab2b…; panel "What the explorer shows" | frame f_008 + raw_011 (panel lengkap) | Tx + waktu cocok (lihat 2.1); panel berisi 2 ketidaksesuaian (lihat §4.4, §4.5) |
| 9 | ~120–135 dtk | Explorer: Success, transferV2, Block 24825928, 175 confirmations, "Nov 21 2026 16:40:42 (+07:00 UTC)", From 0xa5f0C684…, SharedVault | frame f_009 + f_011 | Cocok penuh dengan raw (lihat 2.1) |
| 10 | ~135–150 dtk | Activity @kittynim: +6 RLS (16:40), +250 RLS Shielded (16:31), +2 USDr (13 Nov) | frame f_010 + raw_010 | +6 cocok; +250 dan +2 adalah aktivitas TERPISAH (lihat 1.2) |
| 11 | ~150–185 dtk | Penutup narasi: tx tidak invisible; yang tercatat adalah kejadian, blok, dan relayer; bukan transfer publik biasa | frame f_011 + f_012 + transkrip 147–184 dtk | Klaim narasi dinilai di §4 |

### 1.2 Yang TIDAK boleh dicampur ke dalam cerita pembayaran 6 RLS

- **Shielded +250 $RLS, 21 Nov 2026, 16:31, tx `0xa917fdcc…4104bd38`.**
  Aktivitas @kittynim sendiri (shielding), 9 menit SEBELUM transfer.
  Saldo "sebelum" 321,4 SUDAH mencakup +250 ini (321,4 + 6 = 327,4 pas).
  Bukan bagian dari pembayaran; tidak diverifikasi on-chain dalam audit ini.
- **Received +2 $USDr, 13 Nov 2026, 09:20, tx `0x2be744ca…8b6e1fc9`.**
  Aktivitas 8 hari sebelumnya. Bukan bagian dari pembayaran.
- Video final tidak membedakan ketiganya secara eksplisit (semuanya tampil
  di daftar Activity). Artikel harus menyebut +250/+2 sebagai aktivitas
  lain di akun yang sama, bukan sebagai bagian dari transfer.

### 1.3 Yang belum bisa dicocokkan / batas pencocokan

- **Saldo aplikasi (Public/Shielded/Total) adalah direct observation,
  bukan data terverifikasi on-chain (koreksi 3).** Saldo shielded
  adalah hasil dekripsi note oleh aplikasi dari kunci pengguna; tidak
  ada satu pun field on-chain yang menyatakan "saldo shielded @anara
  = 14,324" atau "saldo shielded @kittynim = 321,4". Yang dapat
  dikatakan: aplikasi menampilkan perubahan saldo tersebut, dan
  perubahannya konsisten secara aritmetika dengan 6 + 4,416
  (pemeriksaan konsistensi atas nilai tampilan, bukan verifikasi
  on-chain). Demikian pula "+6 $RLS" di Activity penerima adalah
  tampilan aplikasi (aplikasi mendekripsi note untuk akun itu),
  bukan field on-chain.
- **Waktu "16:40" di Activity adalah waktu lokal browser (WIB).**
  Cocok dengan block timestamp 16:40:42 WIB (raw `block.json`).
  Waktu pengambilan raw (16:13–16:29 UTC) adalah jam UTC yang berbeda —
  jangan dicampur.
- **"175 confirmations" dan "Confirmed within <= 0.545 secs"** adalah
  snapshot tampilan explorer saat direkam, bukan fakta yang stabil.
- **"Made in 10 s"** adalah timer tampilan aplikasi, bukan durasi yang
  diukur independen.

### 1.4 Footage mentah vs video final (apakah ada pengurutan ulang?)

Urutan substansi SAMA. Yang dipotong dari final (hanya ada di footage):
(1) halaman Send mula-mula $USDr lalu diganti ke $RLS (raw_002);
(2) prompt passkey (raw_006); (3) tooltip penjelasan zero-knowledge proof
(raw_007 — teksnya dikutip di §5.2); (4) halaman Receive @kittynim dengan
QR + alamat lengkap (raw_004); (5) dialog "Halaman Tidak Merespons"
(browser freeze sesaat, raw_010); (6) explorer masih loading di akhir
rekaman (raw_012) — artinya segmen explorer di video final direkam pada
take terpisah (setelah halaman termuat), bukan pada momen yang sama dengan
rekaman aktivitas. Tidak ada pengurutan ulang urutan eksperimen; pemotongan
bersifat editorial. Freeze browser dan take terpisah dicatat sebagai
observasi rekaman, bukan sebagai temuan eksperimen.

## 2. Audit paket JSON dan transaksi (diturunkan ulang dari raw)

Semua nilai di bawah ini dibaca langsung dari
`experiments/transactions/tx-09edab2b/raw/*.json` pada 22 Nov 2026, bukan
dari `TX-AUDIT-REPORT.md` atau `decoded/*`.

### 2.1 Transaksi utama `0x09edab2b…`

| Field | Nilai (raw) | Cocok video |
|---|---|---|
| hash | `0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb` | ya (f_006, f_009, f_011) |
| block | 24825928 (0x17ad048), timestamp 1795254042 = **2026-11-21 16:40:42 WIB** | ya, persis (f_009: "16:40:42 (+07:00 UTC)") |
| from | `0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8` (relayer) | ya (f_009) — BUKAN @anara |
| to | `0x9c5ad5e5ea5b5910e7fd1e1cc7b70ce0e4bf06c2` (SharedVaultProxy) | ya ("SharedVault", f_009) |
| value | 0x0 (0) | ya ("Value 0", f_008/raw_011) |
| gas / gasPrice | gasLimit 1.630.484; gasPrice 48.000.000.000 wei (48 Gwei) | — (bukan di video) |
| input | 4.804 byte; selector `0xaacd552c` | "transferV2" (f_009/f_011) |
| receipt | status 0x1 (sukses); gasUsed 1.316.001; 7 logs; contractAddress null | "Success" (f_009) |
| blok | hanya berisi 1 transaksi ini (gasUsed blok = 1.316.001; gasLimit blok 500.000.000) | — |

### 2.2 Selector + struktur calldata (verifikasi segar)

- `keccak256("transferV2((((uint256,uint256),(uint256[2],uint256[2]),(uint256,uint256)),uint256[],uint256,uint256),bytes[],bytes[])")`
  4 byte pertama = **`0xaacd552c`** — cocok dengan selector di calldata.
  (Tanda tangan kanonis diambil dari `decoded/bundle-abi-extract.json`,
  yaitu ABI client-side dari demo bundle — lihat §5.)
- Proof: struct 8 word = **256 byte** (byte 100–356 calldata) — cocok dengan
  tampilan "256 bytes" di video.
- Statement: array 10 word (panjang 10, byte 452–804):

| Posisi | Nilai | Status |
|---|---|---|
| [0] | 0 | belum teridentifikasi |
| [1] | 0 | belum teridentifikasi |
| [2] | `0x0d6edc87…` (hash) | belum teridentifikasi (bacaan Merkle/binding = inferensi) |
| [3] | `0x0c0f23a6…` | **nullifier** — sama dengan topic[3] log[0] |
| [4] | `0x094b233a…` | **commitment 1** — sama dengan topic[2] log[1] |
| [5] | `0x2304db2e…` | **commitment 2** — sama dengan topic[2] log[2] |
| [6] | `0x206ed94a…` | **commitment 3** — sama dengan topic[2] log[3] |
| [7] | `0x9c5ad5e5…` (alamat vault) | terverifikasi |
| [8] | **4.416 × 10¹⁸** (integer) | terverifikasi (kemunculan integernya); unit RLS dan makna "total fee" adalah interpretasi (lihat §3.2) |
| [9] | `0x0f58ff41…` (hash) | belum teridentifikasi (bacaan binding = inferensi) |

- Dua uint256 lain di struct (byte 388 = **1**, byte 420 = **3**):
  konsisten dengan "1 note masuk, 3 note keluar" (1 nullifier + 3
  commitment), tetapi label itu adalah **inferensi**, bukan nama field
  yang terverifikasi (tidak ada layout statement yang diterbitkan).
- Ciphertext: dari tiap log EncryptedNote, ciphertextI (1.088 byte) dan
  ciphertextII (92 byte) **hadir verbatim di dalam calldata**
  (dicek substring + SHA-256 segar untuk ketiganya). Data log 1.312 byte
  bukan salinan mentah calldata — ia adalah pembungkus ABI (offset +
  panjang) di sekitar kedua ciphertext yang sama.

### 2.3 Event logs (7 log, semua dari vault proxy)

| Log | Event (topic0 diverifikasi keccak segar) | Isi |
|---|---|---|
| [0] | Nullifier `0x437885c0…` | vaultId=2, treeNumber=0, nullifier `0x0c0f23a6…` |
| [1–3] | Commitment `0x28ec6d3c…` (×3) | vaultId=2, commitment (sama dengan statement[4–6]) |
| [4–6] | EncryptedNote `0x3703497a…` (×3) | vaultId=2, commitment, ciphertextI 1.088 B + ciphertextII 92 B |

Topic0 ketiga event diverifikasi segar dengan keccak256 atas tanda tangan
dari bundle ABI (Commitment, EncryptedNote, Nullifier — ketiganya cocok).
`eth_getLogs` independen juga mengembalikan 7 log yang sama.
Tidak ada event PaidOut / CoinLocked / PartialWithdrawal pada tx ini.

### 2.4 Registry username → alamat (verifikasi segar)

- Registry `0xA473291FFb33e2276F364fAE169f03c4406719e9`, 195 log UsernameSet
  (chunk [28, 26, 9, 0, 25, 46, 33, 28, 0] = 195).
- `@anara`: 1 log, blok 23353951, topic alamat
  `0x0c5b369ad7d0c4e051a2887575f7fc85e0ccd0b5` — cocok dengan EVM di video
  (0x0C5B…D0B5).
- `@kittynim`: 1 log, blok 23575688, topic alamat
  `0x680d90983da58bcb7d127e3421193274e84e0efc` — cocok dengan EVM di video
  (0x680D…8eFC) dan alamat lengkap di halaman Receive footage (raw_004).
- **Identitas @anara → 0x0c5b… dan @kittynim → 0x680d… adalah fakta
  on-chain dari registry** (bukan sekadar klaim video). Kaitan
  tx → @anara tetap rekonstruksi: tidak ada alamat pengguna di dalam
  tx (lihat §4.3).

### 2.5 Transaksi terpisah dari relayer yang sama `0xacc7d175…` (koreksi 5)

Transaksi ini ditulis sebagai **transaksi terpisah**, bukan sebagai
bagian dari transaksi utama. Yang terverifikasi dari raw:

- From `0xa5f0c684…` (alamat yang SAMA dengan pengirim tx utama),
  to `0x07e17e17…` (token RLS), blok 24825932 (4 blok setelah tx
  utama), 09:40:45 UTC — **3 detik setelah tx utama** (selisih
  timestamp blok; verified fact).
- Input `0xa9059cbb…` = ERC-20 `transfer(address,uint256)` dengan
  argumen alamat `0x71af09966cbed4434cca97c40fa38b8083548b95` dan jumlah
  **0,576 RLS persis** (576.000.000.000.000.000 wei, dibaca dari input,
  bukan dari laporan). Alamat dan jumlah sebagai **argumen pemanggilan**
  adalah verified fact; keduanya bukan kesimpulan tentang siapa
  penerima itu atau untuk apa transfer tersebut.
- Receipt sukses, gasUsed 41.806, 1 log (event Transfer ERC-20).
- Txlist relayer (2 panggilan explorer independen) mengembalikan tepat
  2 tx di jendela blok: tx utama + tx ini. Tidak ada tx relayer lain
  di jendela tersebut.

Yang TIDAK disimpulkan (tanpa bukti):

- **Siapa `0x71af…` itu.** Peta audit sebelumnya menyebutnya
  "Auditor EOA" — itu rekonstruksi, bukan tautan on-chain yang
  terbukti. Apakah alamat ini milik Rayls Foundation, auditor,
  atau pihak lain: **unknown**.
- **Untuk apa transfer ini.** Kecocokan aritmetika 3,84 × 15% = 0,576
  persis dan tampilan dompet "15% Rayls Foundation fee" adalah
  **petunjuk yang konsisten** dengan dugaan bahwa transfer ini
  berkaitan dengan fee — tetapi kecocokan angka bukan bukti tujuan.
  Tujuan pembayaran: **unknown**. Artikel tidak boleh menulis
  transfer ini sebagai "pembayaran fee ke Foundation" atau "fee
  settlement" sebagai fakta; penulisan yang benar: "transaksi terpisah
  dari relayer yang sama, tiga detik kemudian, yang memanggil
  transfer() dengan argumen (0x71af…, 0,576 RLS)".

### 2.6 Yang TIDAK ada di dalam tx (dicek segar)

- Alamat `0x0c5b…` (@anara) dan `0x680d…` (@kittynim): **tidak ada** di
  calldata, di data log mana pun, maupun di topic mana pun.
- Nilai 6 RLS (6 × 10¹⁸ sebagai word 32-byte): **tidak ada** di calldata.
- Kata "anara" / "kittynim": tidak ada di tx.

## 3. Audit biaya

### 3.1 Tiga komponen — dipisahkan

| Komponen | Nilai | Sumber | Klasifikasi |
|---|---|---|---|
| Chain gas | 1.316.001 gas × 48 Gwei = **0,063168048 unit gas native** | receipt + tx (raw) | **Verified fact** untuk angkanya; **Unknown** untuk nama tokennya (lihat 3.3) |
| Integer 4,416 × 10¹⁸ di statement[8] | **4.416 × 10¹⁸** sebagai word di statement[8] | calldata (raw) | **Verified fact** — hanya kemunculan integernya; unit RLS = **interpretasi** (tampilan aplikasi + 18 desimal token); makna "total fee" = **inference** (lihat §3.2) |
| Interpretasi "4,416 = total fee" | angka di statement[8] ADALAH total fee pembayaran | tampilan aplikasi + aritmetika (lihat §3.2) | **Inference** (kuat, terkoroborasi — bukan fakta on-chain) |
| Transaksi terpisah 0,576 RLS | transfer() dengan argumen (`0x71af…`, 0,576 RLS), tx terpisah dari relayer yang sama, 3 detik kemudian | related-tx input + receipt (raw) | **Verified fact** — argumen + waktu; penerima (siapa) dan tujuan: **Unknown** (lihat §2.5) |
| Sisa aritmetika | **3,84 RLS** = 4,416 − 0,576 | aritmetika | **Reconstruction** (tidak pernah muncul sebagai word sendiri di data on-chain) |
| Tampilan dompet | "3.84 gas + 0.58 Rayls Foundation (15%)" = 4,42 | UI video (f_004/f_006) | **Direct observation** (klaim UI) |
| 15% | 3,84 × 15% = 0,576 (persis) | aritmetika | **Verified fact** (hitungannya); bahwa 15% adalah tarif Foundation = **Official claim** (UI + docs); bahwa transfer 0,576 RLS adalah pembayaran tarif itu = **Unknown** |

### 3.2 Pola 4,416 = 3,84 + 0,576 — fakta dan interpretasi dipisahkan (koreksi 2)

**Fakta (verified fact):** integer 4.416 × 10¹⁸ muncul sebagai word
di statement[8] calldata; integer 0,576 × 10¹⁸ muncul sebagai argumen
jumlah di transaksi terpisah `0xacc7d175…`; selisih keduanya adalah
3,84 × 10¹⁸. **Tiga lapis yang harus dibedakan:** (a) integer mentah
— fakta; (b) unit RLS — **interpretasi**, dan sumbernya berbeda per
suku: unit RLS untuk 0,576 dijangkar oleh kontrak token RLS
(`transfer()` dipanggil pada kontrak token RLS `0x07e17e17…`, jadi
jumlahnya dinyatakan dalam unit token itu), sedangkan unit RLS untuk
4,416 berasal dari tampilan aplikasi (dompet + detailed activity
menyebut fee dalam RLS) — calldata tidak membawa label unit;
3,84 mewarisi unit dari tampilan aplikasi; (c) makna "total fee" —
**inference** (lihat di bawah). Persamaan 4,416 = 3,84 + 0,576
menutup pada angkanya; label RLS pada tiap suku berasal dari sumber
yang berbeda dan tidak boleh dibaca sebagai satu fakta on-chain yang
sama.

**Interpretasi (inference, terkoroborasi tetapi bukan fakta on-chain):**
bahwa word di statement[8] adalah "total fee", bahwa 3,84 adalah
bagian fee yang ditahan relayer, dan bahwa 0,576 adalah bagian yang
diteruskan sebagai fee Foundation. Koroborasi untuk interpretasi ini:
(i) tampilan dompet menunjukkan total fee 4,42 (3,84 + 0,58) dan
penjelasan detailed activity menunjukkan 4,416 sebagai fee menurut
aplikasi; (ii) aritmetika saldo menutup: 6 + 4,416 = 10,416 sama
dengan penurunan saldo shielded yang ditampilkan aplikasi;
(iii) 3,84 × 15% = 0,576 persis.

**Batas verifikasi interpretasi ini:** tidak ada layout statement yang
diterbitkan dan tidak ada verified source kontrak vault — jadi arti
semantik word statement[8] tidak dapat dibuktikan dari skema on-chain
yang terverifikasi; ia ditetapkan lewat pencocokan nilai + tampilan
aplikasi + ABI client-side dari demo bundle (kode referensi, bukan
sumber terverifikasi). Dengan kata lain: **integer 4.416 × 10¹⁸ di
statement[8] adalah fakta; label RLS untuk integer itu dan makna
"total fee" adalah interpretasi yang kuat tetapi tetap interpretasi.**
Artikel harus menulis ketiganya secara terpisah: "the integer
4.416 × 10¹⁸ appears in the transaction's statement; the app presents
it as 4.416 RLS and as the total fee" — bukan "the on-chain fee is
4.416 RLS" tanpa kualifikasi.

- Integer 4,416 × 10¹⁸ (statement) dan 0,576 RLS (transfer ERC-20 pada
  kontrak token RLS) keduanya terverifikasi independen dari raw —
  dengan catatan unit RLS untuk keduanya berasal dari sumber yang
  berbeda (lihat di atas).
- 3,84 hanya muncul sebagai selisih. Sifat pastinya (fee layanan relayer
  vs penggantian gas) **unknown** — dompet menyebutnya "gas", laporan
  TX sebelumnya menyebutnya "relayer service fee, not chain gas"
  (TX-AUDIT-REPORT.md:206), tetapi tidak ada kata on-chain yang
  membuktikan salah satunya.
- Perhatian: 3,84 RLS ≠ chain gas 0,063168048. Keduanya berbeda ~60×.
  Artikel harus menjaga keduanya tetap terpisah.

### 3.3 TEMUAN BARU — token gas: RLS atau USDr? (belum terjawab)

Dua teks resmi aplikasi saling bertentangan:

- **Untuk RLS:** daftar aset dompet melabeli "$RLS — Pays gas"
  (observasi langsung, f_001); pilot blog Rayls (12 Nov, dikutip di
  audit awal:193) menyatakan "semua fee dalam $RLS" (official claim);
  kontrak bernama `RlsGasForwarder` (0x753cc3…); laporan TX
  melabeli chain gas "0,063168048 RLS".
- **Untuk USDr:** panel "What the explorer shows" menyatakan relayer
  "pays the gas in $USDr" dan "Value counts only the chain's own coin,
  $USDr" (raw_011). Alamat token USDr `0x0000…0400` adalah alamat gaya
  precompile (0x400), konsisten dengan token tingkat protokol — tetapi
  itu bukan bukti nama token gas.

Tx mentah tidak dapat menyelesaikan ini: gasPrice/gasUsed dinyatakan
dalam unit native tanpa nama token. **Label "0,063168048 RLS" di
TX-AUDIT-REPORT.md:144 adalah asumsi (tertulis "(18 decimals assumed)"
untuk desimal, tetapi identitas tokennya tidak pernah diperiksa).**
Untuk artikel, penulisan yang aman: "chain gas 1.316.001 × 48 Gwei =
0,063168048 unit gas native" + catatan bahwa teks aplikasi sendiri
tidak sepakat soal tokennya. Jangan menyatakan RLS atau USDr sebagai
fakta yang sudah pasti. (Kandidat pertanyaan untuk tiket — lihat §7.4.)

## 4. Audit visibilitas data publik

### 4.1 Yang dapat dilihat pengamat publik biasa (dari tx + explorer)

| Data | Terlihat publik? | Bukti |
|---|---|---|
| Bahwa sebuah transfer terjadi | ya | tx sukses, method transferV2 |
| Blok + waktu | ya | blok 24825928, 16:40:42 WIB |
| Relayer pengirim | ya | from `0xa5f0c684…` |
| Kontrak yang dipanggil | ya | SharedVaultProxy `0x9c5ad5e5…` |
| Value field | ya — **0** | tx value 0x0 |
| Gas yang dipakai + harga gas | ya | 1.316.001 × 48 Gwei |
| 1 nullifier (hash) | ya | log[0] topic[3] `0x0c0f23a6…` |
| 3 commitment (hash) | ya | log[1–3] topic[2] |
| 3 encrypted note / ciphertext | ya (sebagai byte) | log[4–6] data; sama dengan byte di calldata |
| Integer 4,416 × 10¹⁸ di statement[8] | ya — sebagai word calldata | statement[8] (raw). Unit RLS untuk integer ini adalah interpretasi (tampilan aplikasi), dan maknanya sebagai "total fee" adalah inference (lihat §3.2) — keduanya BUKAN fakta on-chain |
| Transaksi terpisah 0,576 RLS | ya — sebagai pemanggilan transfer() | tx `0xacc7d175…` (transfer ERC-20 publik); tujuan transfer: unknown (lihat §2.5) |
| Argumen alamat `0x71af…` di transfer itu | ya — sebagai argumen pemanggilan | input transfer ERC-20; siapa pemilik alamat itu: unknown |

### 4.2 Yang TIDAK dapat dibaca pengamat publik biasa dari tx ini

| Data | Status |
|---|---|
| Jumlah pembayaran (6 RLS) | tidak ada sebagai plaintext di tx (dicek segar, §2.6) |
| Siapa pengirim (@anara) | alamat tidak ada di tx (dicek segar, §2.6) |
| Siapa penerima (@kittynim) | alamat tidak ada di tx (dicek segar, §2.6) |
| Token apa (RLS) | tidak ada penanda token di tx utama (token hanya diketahui dari konteks aplikasi + saldo) |
| Nilai tiap note / pemetaan 3 note → (bayar / kembalian / fee) | rekonstruksi dari saldo, bukan fakta on-chain |
| Isi ciphertext (jumlah, pemilik note) | terenkripsi; tidak dapat dibaca tanpa kunci |

### 4.3 Pemegang kunci / auditor — apa yang berbeda

- **Pemegang kunci (pengirim/penerima):** dapat mendekripsi note miliknya
  dan melihat saldo shielded-nya di aplikasi. Itu sebabnya Activity
  penerima menampilkan "+6 $RLS" dengan tx yang sama — aplikasi
  penerima mendekripsi note untuk akun itu. Kemampuan ini adalah
  klaim desain (dokumen + UI), bukan sesuatu yang dibuktikan oleh tx.
- **Auditor:** panel aplikasi mengklaim "Auditor sees it" untuk
  pengirim, penerima, dan jumlah. **Klaim ini tidak terverifikasi
  on-chain dalam audit ini.** Yang terverifikasi: ada peran auditor
  di registry (7 AuditorAdded, 4 AuditorKeyGiven — dari audit awal),
  dan transaksi terpisah `0xacc7d175…` memanggil transfer() dengan
  argumen alamat `0x71af…` (disebut "Auditor EOA" di peta audit —
  kaitan alamat itu dengan peran auditor adalah rekonstruksi, bukan
  tautan on-chain yang terbukti). Artikel harus menyajikan
  "auditor dapat melihat" sebagai klaim aplikasi, bukan sebagai
  fakta yang diverifikasi.
- **Pihak berwenang:** tidak ada bukti dalam paket ini tentang akses
  pihak berwenang. Jangan menyimpulkan apa pun ke arah itu.
- Prinsip yang dipakai di sini (sesuai instruksi): tidak menyimpulkan
  "mustahil diketahui" hanya karena tidak tampil sebagai plaintext.
  Ciphertext ada di chain; apakah seseorang dapat mendekripsinya
  bergantung pada kunci — dan itu di luar bukti paket ini.

### 4.4 TEMUAN BARU — alamat relayer di panel ≠ alamat relayer on-chain

Panel "What the explorer shows" (raw_011, juga f_008) menulis:
"From — The relayer, @rayls-relayer **0x25f8…8ac5**, not you."
Tetapi pengirim tx on-chain adalah **`0xa5f0c684…`**, dan alamat itu
pula yang tercatat sebagai relayer di `contracts/addresses/addresses.json`
(`other_addresses[1]`) serta di endpoint txlist explorer.
Pencarian `25f8` di seluruh repo tidak menemukan alamat itu di file
mana pun (yang cocok hanya potongan hex di dalam blob ciphertext —
false positive). Alamat lengkap `0x25f8…` tidak terlihat di video
(ditampilkan terpotong), jadi tidak dapat dicari lebih lanjut dari
bukti ini. **Kemungkinan:** (a) panel menampilkan alamat layanan
relayer yang berbeda dari alamat penandatangan tx; (b) alamat usang/
cache; (c) panel salah. Tidak ada yang dapat diputuskan dari bukti
ini. **Artikel harus memakai alamat on-chain `0xa5f0c684…` dan
menyebutkan ketidaksesuaian ini sebagai pertanyaan terbuka**
(kandidat tiket — lihat §7.4). Jangan mengutip `0x25f8…` sebagai
relayer.

### 4.5 TEMUAN BARU — "Hidden" di panel bukan berarti "tidak ada di chain"

Panel menandai "Amount: 3 commitments: 0x094b233a…, 0x2304db2e…,
0x206ed94a…" sebagai **Hidden / Auditor sees it** — padahal ketiga
nilai commitment itu ADALAH topic publik di log[1–3] (diverifikasi
segar, §2.3). Artinya: "Hidden" dalam bahasa panel berarti
"tidak dapat diartikan sebagai jumlah oleh pengamat biasa", BUKAN
"tidak ada di blockchain". Artikel harus menulisnya dengan tepat:
commitment dan ciphertext **ada dan publik sebagai byte**; yang
tersembunyi adalah **maknanya** (jumlah, pemilik). Jangan menulis
"commitment tidak terlihat" atau "note tidak ada di chain".

### 4.6 Catatan tentang klaim narasi video

- "The public transaction sender is the relayer, not @anara" — **benar**
  (from = relayer).
- "The value field shows 0" — **benar** (value 0x0). (Transkrip Whisper
  menulis "0 U.S.D.R." — itu artefak transkripsi, bukan kesalahan video;
  subtitle di frame f_008 menulis "Value — 0, the value field is empty".)
- "The explorer shows commitments and encrypted notes, rather than a
  conventional public transfer" — **benar** (log + calldata).
- "The transaction itself isn't invisible. The blockchain still records
  that it happened, which block included it, and which relayer submitted
  it." — **benar dan merupakan tesis artikel yang tepat**.
- "The receiver can confirm the payment, while the public transaction
  record shows a different picture" — **benar** (Activity penerima
  vs tampilan explorer).

## 5. Dokumentasi dan implementasi

### 5.1 Tiga lapis yang harus dibedakan

| Lapis | Contoh | Status untuk tx ini |
|---|---|---|
| **Klaim resmi** (docs, blog, UI aplikasi) | docs.rayls.com: shielded send hanya menunjukkan kejadian, relayer, gas fee; fee relayer 15% ke Foundation; pilot blog: "semua fee dalam $RLS"; UI: "Quantum-private", "Auditor sees it", panel explorer | Dikutip sebagai klaim, bukan bukti on-chain |
| **Kode referensi** (demo bundle client-side) | `bundle-abi-extract.json` (IEnygmaDvp, bundle SHA `7530bbc2…`, diambil 21 Nov 16:17 UTC); tanda tangan event + transferV2 | Selector/topic cocok dengan on-chain (verifikasi segar §2.2–2.3); logika internal kontrak TIDAK terbukti dari bundle |
| **Implementasi deployed** | SharedVaultProxy `0x9c5ad5e5…`, implementasi dari slot EIP-1967 `0xAd966704…` (dibaca segar dari `contracts.json`), registry yx `0xA473291F…` | Alamat + bytecode + slot terverifikasi; **tidak ada verified source** untuk implementasi vault (dari audit awal, tidak diverifikasi ulang di ronde ini — lihat 5.3) |

### 5.2 Teks aplikasi yang relevan (observasi langsung dari footage)

- Tooltip ZK proof (raw_007): "A zero-knowledge proof shows something
  is true without showing why. Here it shows the vault that you may
  spend these notes and that nothing is created, without saying which
  notes, whose they are, or how much. This tab computes it from your
  keys and notes. Onchain go the proof, the new notes, encrypted, and
  a nullifier per note spent." — Klaim resmi (copy UI). Konsisten
  dengan yang teramati on-chain (1 proof 256 B, 3 note baru terenkripsi,
  1 nullifier) — tetapi "shows the vault that you may spend" adalah
  pernyataan tentang pembuktian, bukan sesuatu yang dapat diperiksa
  dari tx.
- Baris Public/Hidden/Auditor di halaman Send (f_003/f_004): "That
  payment happened" (Public) / "Who paid whom, and how much —
  Quantum-private" (Hidden) / "@anara paid @kittynim 6 $RLS" (Auditor).
  Ini adalah **label UI**, bukan klasifikasi on-chain.

### 5.3 Batasan yang dibawa dari audit sebelumnya (tidak diverifikasi ulang)

- Tidak ada verified source untuk implementasi vault `0xAd966704…`
  (audit awal; `contracts/verified-source/README.md`). Ronde ini tidak
  memeriksa ulang status verifikasi explorer (di luar ruang lingkup
  artikel; membutuhkan pengecekan live terpisah).
- Implementasi bx vs yx: tx ini memakai deployment yx yang aktif
  (vault proxy `0x9c5ad5e5…`); ketidaksesuaian bx tidak relevan
  untuk artikel ini.
- 4byte.directory tidak memiliki entri untuk selector/event ini
  (dari audit sebelumnya) — resolusi mengandalkan bundle ABI +
  keccak lokal (diverifikasi segar di ronde ini).

## 6. Klasifikasi temuan

| # | Temuan | Label | Sumber + alasan |
|---|---|---|---|
| F1 | Tx sukses, transferV2, blok 24825928, 16:40:42 WIB | Verified fact | `transaction.json` + `receipt.json` + `block.json` + explorer frame |
| F2 | Pengirim publik = relayer `0xa5f0c684…`, bukan @anara | Verified fact | tx `from` (raw) + explorer frame |
| F3 | Value field = 0 | Verified fact | tx `value` 0x0 (raw) |
| F4 | 1 nullifier + 3 commitment + 3 encrypted note | Verified fact | receipt 7 log + topic0 keccak segar |
| F5 | Ciphertext log = byte di calldata | Verified fact | substring + SHA-256 segar (§2.2) |
| F6a | Integer 4.416 × 10¹⁸ muncul di statement[8] | Verified fact | word di calldata (raw) — hanya kemunculan integernya; unit RLS = interpretasi (tampilan aplikasi); makna "total fee" = inference (F6b) |
| F6b | Angka itu ADALAH total fee pembayaran | Inference | tampilan aplikasi + aritmetika saldo + 3,84 × 15% = 0,576; arti semantik word tidak dibuktikan skema on-chain terverifikasi (§3.2) |
| F7 | Transaksi terpisah dari relayer yang sama, 3 detik kemudian, memanggil transfer() dengan argumen (`0x71af…`, 0,576 RLS) | Verified fact (argumen + waktu) | related-tx input + receipt + timestamp blok (raw); siapa `0x71af…` dan untuk apa transfer itu: Unknown (F31, F32) |
| F8 | 3,84 = 4,416 − 0,576 | Reconstruction | aritmetika pada angka; tidak ada word on-chain sendiri; unit RLS tiap suku berasal dari sumber berbeda (lihat §3.2) |
| F9 | 3,84 adalah "gas" / fee layanan relayer | Unknown | dompet menyebut "gas"; sifat pastinya tidak terbukti on-chain |
| F10 | Chain gas 0,063168048 unit native | Verified fact (angka) | gasUsed × gasPrice (raw) |
| F11 | Chain gas = 0,063168048 **RLS** | Unknown | label TX report; teks aplikasi bertentangan (§3.3) |
| F12 | Jumlah 6 RLS tidak ada di tx sebagai plaintext | Verified fact | pencarian segar di calldata/log/topic (§2.6) |
| F13 | Alamat @anara/@kittynim tidak ada di tx | Verified fact | pencarian segar (§2.6) |
| F14 | @anara = `0x0c5b…`, @kittynim = `0x680d…` | Verified fact | registry UsernameSet (raw), didekode segar |
| F15 | Tx `0x09edab2b…` adalah pembayaran @anara → @kittynim sebesar 6 RLS | Reconstruction | tiga pilar: (1) aplikasi menampilkan tx yang sama di Activity kedua akun; (2) registry memetakan @anara → `0x0c5b…` dan @kittynim → `0x680d…`; (3) waktu/blok cocok. BUKAN fakta on-chain: tidak ada alamat pengguna atau jumlah di dalam tx (F12, F13) |
| F16 | 3 note keluar = (6 bayar / 3,908 kembalian / 4,416 [nilai statement[8]]) | Reconstruction | saldo + jumlah note; bukan fakta on-chain; unit RLS dan makna "fee" untuk 4,416 adalah interpretasi (lihat §3.2) |
| F17 | Statement[3–8] = nullifier, 3 commitment, alamat vault, fee | Verified fact | pencocokan nilai segar (§2.2) |
| F18 | Statement[0,1,2,9] = (0, 0, hash, hash) | Verified fact (nilainya); Unknown (artinya) | nilai dibaca segar; tidak ada layout yang diterbitkan |
| F19 | Struct (1, 3) = 1 note masuk, 3 note keluar | Inference | konsisten dengan 1 nullifier + 3 commitment; label tidak terverifikasi |
| F20 | Proof berukuran 256 byte | Verified fact | struktur calldata: proof adalah tuple statis 8 word (byte 100–356) menurut skema ABI bundle; tampilan UI "256 bytes" mengkoroborasi. Catatan: identifikasi "proof" bergantung pada skema ABI client-side (kode referensi, bukan verified source) |
| F21 | Proof dibuat dalam 10 detik di browser | Direct observation | HANYA tampilan timer aplikasi ("Made in 10 s, in this tab"). Bukan durasi yang diukur independen; audit ini tidak mengukur waktu proving dengan instrumen apa pun |
| F22 | Saldo shielded 14,324 → 3,908 dan 321,4 → 327,4 | Direct observation | tampilan aplikasi (video); konsisten secara aritmetika dengan 6 + 4,416 — tetapi BUKAN data terverifikasi on-chain; tidak ada field on-chain yang menyatakan saldo shielded |
| F23 | Panel relayer `0x25f8…8ac5` ≠ relayer on-chain `0xa5f0c684…` | Verified fact (ketidaksesuaiannya); Unknown (penyebabnya) | panel video vs tx raw; `0x25f8` tidak ada di repo |
| F24 | "Auditor sees it" (pengirim/penerima/jumlah) | Official claim | copy UI aplikasi; tidak terverifikasi on-chain |
| F25 | Commitment "Hidden" di panel padahal topic publik | Verified fact (ketidaksesuaiannya) | panel vs log raw (§4.5) |
| F26 | "Semua fee dalam $RLS" (pilot blog) | Official claim | dikutip di audit awal:193 |
| F27 | Panel: relayer "pays the gas in $USDr" | Official claim | copy UI (raw_011); bertentangan dengan F26 |
| F28 | Tidak ada verified source implementasi vault | Official claim (carried) | audit awal; tidak diverifikasi ulang ronde ini |
| F29 | +250 RLS (16:31) dan +2 USDr (13 Nov) bukan bagian pembayaran | Verified fact | daftar Activity video; +250 sudah termasuk di saldo "sebelum" |
| F30 | Blok 24825928 hanya berisi tx ini | Verified fact | `block.json` (1 transaksi) |
| F31 | Kecocokan 3,84 × 15% = 0,576 menunjukkan transfer `0xacc7d175…` berkaitan dengan fee | Inference | kecocokan angka persis + tampilan dompet "15%"; kecocokan angka bukan bukti tujuan transfer |
| F32 | `0x71af…` adalah alamat fee Rayls Foundation / Auditor | Unknown | tidak ada tautan on-chain; label "Auditor EOA" di peta audit adalah rekonstruksi |

## 7. Laporan hasil audit

### 7.1 Temuan yang sudah kuat (boleh dipakai di artikel — dengan klasifikasi)

- Transaksi terjadi dan tercatat publik: transferV2 sukses, blok
  24825928, 16:40:42 WIB, pengirim publik relayer `0xa5f0c684…`,
  vault `0x9c5ad5e5…`, value 0. (**Verified fact.**)
- Yang terlihat publik: 1 nullifier, 3 commitment, 3 encrypted note,
  dan integer 4.416 × 10¹⁸ di statement[8]. (**Verified fact** untuk
  kemunculan integernya; label RLS dan makna "total fee" adalah
  **inference** — lihat §3.2.)
- Yang tidak terbaca publik dari tx: jumlah 6 RLS, pengirim, penerima,
  token — semuanya tidak ada sebagai plaintext (dicek segar).
  (**Verified fact** — hasil pencarian di calldata/log/topic.)
- Kaitan tx ini dengan pembayaran @anara → @kittynim 6 RLS adalah
  **reconstruction** (aplikasi + registry + kecocokan tx), bukan
  fakta on-chain (koreksi 1).
- Aplikasi menampilkan "+6 $RLS" di Activity penerima untuk tx yang
  sama, dan saldo shielded yang ditampilkan bergerak 321,4 → 327,4
  (penerima) dan 14,324 → 3,908 (pengirim); selisih 10,416 = 6 + 4,416
  secara aritmetika. (**Direct observation** dari aplikasi, bukan
  data terverifikasi on-chain — koreksi 3.)
- Proof berukuran 256 byte menurut struktur calldata; aplikasi
  melaporkan waktu pembuatan 10 detik. (**Verified fact** untuk ukuran
  dengan sumber calldata; **direct observation** untuk waktu —
  koreksi 4.)
- Identitas username→alamat terverifikasi dari registry on-chain
  (@anara → `0x0c5b…`, @kittynim → `0x680d…`). (**Verified fact.**)
- Transaksi terpisah dari relayer yang sama, 3 detik kemudian,
  memanggil transfer() dengan argumen (`0x71af…`, 0,576 RLS).
  (**Verified fact** untuk argumen + waktu; siapa `0x71af…` dan
  untuk apa transfer itu: **unknown** — koreksi 5.)
- Deskripsi docs Rayls sendiri (shielded send menunjukkan kejadian,
  relayer, dan gas fee) cocok dengan yang teramati. (**Official claim**
  yang konsisten dengan bukti.)

### 7.2 Temuan yang perlu koreksi (sebelum dipakai di artikel)

- **K1. Alamat relayer:** jangan kutip `0x25f8…8ac5` dari panel sebagai
  relayer. Alamat on-chain adalah `0xa5f0c684…`. Ketidaksesuaian panel
  harus disebut sebagai pertanyaan terbuka, bukan diabaikan.
- **K2. Unit chain gas:** jangan tulis "chain gas 0,063168048 RLS"
  sebagai fakta. Tulis "1.316.001 gas × 48 Gwei = 0,063168048 unit gas
  native" dan catat bahwa teks aplikasi tidak sepakat (RLS vs USDr).
  Label RLS di TX-AUDIT-REPORT.md:144 adalah asumsi yang belum diperiksa
  identitas tokennya.
- **K3. "Hidden" ≠ "tidak ada di chain":** jangan tulis commitment/
  encrypted note "tidak terlihat" atau "invisible". Tulis: byte-nya
  publik, maknanya (jumlah, pemilik) yang tidak terbaca.
- **K4. Pemetaan 3 note:** jangan tetapkan "note 1 = pembayaran 6 RLS,
  note 2 = kembalian 3,908, note 3 = fee 4,416" sebagai fakta. Itu
  rekonstruksi. Tulis sebagai "konsisten dengan" atau jangan dipetakan.
- **K5. "3,84 gas":** jangan tulis 3,84 sebagai chain gas atau sebagai
  fee yang terverifikasi on-chain. Tulis: selisih aritmetika
  4,416 − 0,576; dompet menyebutnya "gas"; sifat pastinya belum diketahui.
- **K6. "Auditor sees it":** sajikan sebagai klaim aplikasi, bukan
  sebagai kemampuan yang sudah diverifikasi. Jangan menulis bahwa
  auditor "dapat melihat" sebagai fakta audit ini.
- **K7. Aktivitas lain:** jangan sajikan +250 RLS (16:31) atau +2 USDr
  (13 Nov) sebagai bagian dari pembayaran 6 RLS.
- **K8. Atribusi @anara → @kittynim (koreksi 1):** jangan menulis
  "transaksi on-chain ini adalah pembayaran @anara ke @kittynim"
  sebagai fakta. Tulis: transaksi `0x09edab2b…` tercatat on-chain;
  kaitannya dengan kedua akun adalah reconstruction dari bukti
  aplikasi + registry + kecocokan transaksi.
- **K9. Transfer 0,576 RLS (koreksi 5):** jangan menulis "0,576 RLS
  dikirim ke Auditor/Foundation sebagai fee" sebagai fakta. Tulis:
  transaksi terpisah dari relayer yang sama, 3 detik kemudian,
  memanggil transfer() dengan argumen (`0x71af…`, 0,576 RLS);
  siapa `0x71af…` dan untuk apa transfer itu belum diketahui.
  Kecocokan 3,84 × 15% = 0,576 boleh disebut sebagai petunjuk
  aritmetika, bukan sebagai bukti tujuan.

### 7.3 Bukti yang belum cukup

- Identitas token gas (RLS vs USDr) — teks aplikasi bertentangan; tx
  tidak memberi nama token.
- Arti statement[0,1,2,9] dan field struct (1, 3) — tidak ada layout
  yang diterbitkan.
- Apakah `0x71af…` adalah alamat fee Rayls Foundation — tidak ada
  tautan on-chain; hanya peta audit yang menyebutnya "Auditor EOA".
- Tujuan transfer terpisah `0xacc7d175…` (0,576 RLS dengan argumen
  alamat `0x71af…`) — kecocokan 3,84 × 15% = 0,576 hanya petunjuk
  aritmetika, bukan bukti tujuan.
- Arti semantik word statement[8] sebagai "total fee" — integer
  terverifikasi, interpretasinya inference (lihat §3.2).
- Unit RLS untuk integer statement[8] — berasal dari tampilan
  aplikasi, bukan dari calldata; calldata tidak membawa label unit.
- Sifat komponen 3,84 (fee layanan vs penggantian gas).
- Kemampuan auditor yang sebenarnya (dekripsi/identifikasi) — hanya
  klaim UI.
- Verifikasi ulang status "tidak ada verified source" implementasi vault
  (dibawa dari audit awal; bukan diverifikasi ulang di sini).

### 7.4 Pertanyaan yang belum terjawab (kandidat tiket / artikel)

Dua pertanyaan terbuka yang dipertahankan (sesuai review):

- **Q-A:** Mengapa panel "What the explorer shows" menyebut relayer
  `0x25f8…8ac5`, sedangkan pengirim tx adalah `0xa5f0c684…`?
  Apakah ada dua alamat relayer, atau panel menampilkan alamat lain?
- **Q-B:** Token apa yang membayar chain gas — RLS atau USDr?
  Dompet + pilot blog berkata RLS; panel explorer berkata USDr.

Pertanyaan lain yang masih terbuka:

- **Q-C:** Apa arti statement[0,1,2,9] dan field struct (1, 3)?
- **Q-D:** Apakah `0x71af09966cbed4434cca97c40fa38b8083548b95` adalah
  alamat fee Rayls Foundation?
- **Q-E:** Apa tepatnya komponen 3,84 RLS (fee layanan relayer vs
  penggantian gas)?
- **Q-F:** Untuk apa transaksi terpisah `0xacc7d175…` (transfer 0,576
  RLS dengan argumen alamat `0x71af…`)? Kecocokan 3,84 × 15% = 0,576
  adalah petunjuk aritmetika, bukan bukti tujuan.

### 7.5 Daftar klaim yang aman digunakan dalam artikel (diperbaiki, beserta klasifikasi)

1. "On 21 Nov 2026, transaction `0x09edab2b…` was recorded on-chain
   in block 24825928 (16:40:42 WIB) as a successful transferV2 call."
   — **Verified fact.** "The experiment links this transaction to a
   shielded payment of 6 RLS from @anara to @kittynim." —
   **Reconstruction** (aplikasi + registry + kecocokan tx; bukan
   fakta on-chain).
2. "The public sender of that transaction is not @anara. It is the
   relayer, `0xa5f0c684…`, calling the SharedVault contract
   (`0x9c5ad5e5…`) with a value of 0." — **Verified fact** (tx `from`
   adalah relayer; alamat @anara tidak ada di dalam tx).
3. "What the chain records is one nullifier, three commitments and
   three encrypted notes — and the integer 4.416 × 10¹⁸ appears in
   the transaction's statement. The app presents that integer as
   4.416 RLS and as the total fee." — **Verified fact** untuk catatan
   on-chain dan kemunculan integer; **inference** untuk label RLS
   dan makna "total fee".
4. "The amount (6 RLS), the user-level sender and the user-level
   receiver do not appear in the transaction in plaintext. (The public
   transaction sender — the relayer — does appear; see claim 2.)" —
   **Verified fact** (dicek segar di calldata, log, dan topic).
   Istilah "user-level" dipakai di sini agar tidak tertukar dengan
   relayer sebagai public transaction sender.
5. "A separate transaction by the same relayer, three seconds later,
   called transfer() on the RLS token contract with the arguments
   (`0x71af…`, 0.576 RLS)." — **Verified fact** untuk pemanggilan
   dan waktunya; siapa `0x71af…` dan untuk apa transfer itu:
   **unknown**.
6. "The receiver's app shows +6 RLS for the same transaction, and the
   app shows the shielded balances moving 321.4 → 327.4 (receiver)
   and 14.324 → 3.908 (sender)." — **Direct observation** (tampilan
   aplikasi, bukan data terverifikasi on-chain).
7. "The proof is 256 bytes, according to the transaction's calldata
   structure. The app reported it was generated in 10 seconds in the
   browser." — **Verified fact** (ukuran, sumber calldata) dan
   **direct observation** (waktu, sumber tampilan aplikasi).
8. "The usernames map to addresses on-chain in the public registry
   (@anara → `0x0c5b…`, @kittynim → `0x680d…`)." — **Verified fact**
   (registry UsernameSet).
9. "Rayls' own documentation describes a shielded send as showing
   only that a transfer happened, the relayer, and the gas fee." —
   **Official claim** (docs.rayls.com, dikutip di audit awal).
10. "The commitments and ciphertexts are public as bytes; what is
    hidden is what they mean — the amounts and the owners." —
    **Verified fact** untuk keberadaan byte publik; **inference**
    untuk "maknanya tersembunyi" (didasarkan pada sifat enkripsi
    ciphertext, bukan pada pemeriksaan isi).

## 8. Daftar calon commit (untuk artikel; BELUM di-commit)

Verifikasi integritas (22 Nov 2026, ronde ini):
- Manifest journey: **12/12 entri OK** (SHA-256 + ukuran cocok).
- Manifest TX: **20/20 entri OK**.
- Verifier TX: **23/23 PASS, exit 0**.
- Comparator v2.1.1: tidak disentuh (hash `bfef1f66…` — tidak
  diverifikasi ulang di ronde ini karena tidak dipakai; comparator
  tetap tersertifikasi dan tidak diubah).
- Raw evidence: tidak diubah (semua hash manifest cocok).

### 8.1 File baru (audit ini)

| File | Alasan | Status pemeriksaan |
|---|---|---|
| `experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r3.md` (file ini) | Laporan audit terarah revisi r3 untuk artikel; memuat empat koreksi review atas r2 + daftar klaim + pertanyaan + daftar commit persis (§8.6) | Ditulis 22 Nov 2026; seluruh angka/alamat sama dengan r2 (tidak ada penurunan ulang baru — revisi ini hanya memperbaiki klasifikasi dan redaksi); ukuran final diperiksa di §8.5 |
| `experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r2.md` | Revisi r2 (22 Nov 2026); dipertahankan sebagai catatan revisi | **Superseded oleh r3**; tidak diubah sejak ditulis (48.097 byte, SHA-256 `00e464f29a3615e6…` — terverifikasi, lihat §8.5); **tidak diusulkan masuk commit** (lihat §8.6) |
| `experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22.md` (r1) | Versi pertama audit (22 Nov 2026); dipertahankan sebagai catatan revisi | **Superseded oleh r2/r3**; tidak diubah sejak ditulis (35.269 byte, SHA-256 `bd54c362c0418e10…`); **tidak diusulkan masuk commit** (lihat §8.6) |

### 8.2 File yang sudah ada dan relevan untuk artikel

| File | Alasan | Status pemeriksaan |
|---|---|---|
| `experiments/testnet-journeys/week2-private-payment/enygma-week2-private-payment-final.mp4` (720p) + `…-final-1080p.mp4` | Video eksperimen yang diaudit (bukti visual utama) | Manifest journey 12/12 OK; video final ditonton penuh ronde r1 (12 frame + transkrip) |
| `experiments/testnet-journeys/week2-private-payment/subs.ass` | Subtitle video | Manifest 12/12 OK; regenerasi terbukti byte-identik (audit sebelumnya) |
| `experiments/testnet-journeys/week2-private-payment/manifest.json` | Manifest + SHA video/manifest (12 entri) | **12/12 OK** (diperiksa ulang ronde r1) |
| `experiments/testnet-journeys/week2-private-payment/README.md` | Dokumentasi perjalanan + temuan + batasan | Isi diperiksa ronde r1 (panel relayer + saldo cocok dengan frame) |
| `experiments/testnet-journeys/week2-private-payment/EDIT-PLAN.md`, `QA-REPORT-V2.md` | Rencana edit + QA video | Manifest 12/12 OK |
| `experiments/testnet-journeys/week2-private-payment/build-*.sh` | Skrip build video (reproducibility) | Manifest 12/12 OK |
| `experiments/transactions/tx-09edab2b/raw/*.json` (9 file) | Bukti mentah tx (tidak diubah) | Manifest TX **20/20 OK**; seluruh nilai kunci diturunkan ulang dari file-file ini ronde r1 |
| `experiments/transactions/tx-09edab2b/decoded/*.json` (4 file) | Decode + ABI bundle + lookup | Manifest 20/20 OK; selector/topic diverifikasi segar via keccak ronde r1 |
| `experiments/transactions/tx-09edab2b/TX-AUDIT-REPORT.md`, `gaps.md`, `TODO.md`, `ADDENDUM-2026-11-22.md`, `manifest.json` | Laporan + batasan + manifest TX (20 entri) | Manifest 20/20 OK; TODO diperbarui 22 Nov (stage-1 close) + manifest diperbarui; catatan: label "0,063168048 RLS" di TX-AUDIT-REPORT.md:144 adalah asumsi identitas token (lihat §3.3) |
| `scripts/tx_audit_09edab2b.py`, `scripts/decode_tx_09edab2b.py`, `scripts/verify_tx_audit_09edab2b.py` | Skrip pengambilan + decode + verifier | Manifest 20/20 OK; verifier **23/23 PASS** (dijalankan ulang ronde r1) |
| `contracts/addresses/addresses.json` | Peta alamat (relayer, vault, registry, token RLS) | Hash INDEX cocok (9.202 B / `f78f0128…` — diperiksa ulang di §8.5); relayer `0xa5f0c684…` cocok dengan tx |
| `contracts/verified-source/README.md` | Status "tidak ada verified source" implementasi vault | Isi diperiksa (audit awal); tidak diverifikasi ulang ronde ini (lihat §5.3) |
| `audit-reports/ENYGMA-TESTNET-AUDIT-REPORT.md` | Audit awal (docs, pilot blog, registry) — konteks | Byte-identik dengan salinan luar repo (cmp, audit awal); tidak diubah ronde ini |
| `tickets/rayls-team-questions-draft-2026-11-22.md` | Draf tiket (Q-A/Q-B dari §7.4 adalah kandidat tambahan) | Ditulis 22 Nov; **belum dikirim** |
| `INDEX.md`, `RESEARCH-TRAIL.md`, `REPRODUCE.md`, `README.md` | Entri indeks/trail/repro untuk file audit baru | **Diperbarui saat commit, setelah review** (bukan sekarang) |

### 8.3 Yang TIDAK masuk commit (tetap local-only)

- Footage mentah `raw-data/videos/week2-source-footage-….mp4`
  (24.777.960 B) dan VO mp3 `raw-data/videos/ElevenLabs_….mp3`
  (2.953.936 B) — sudah di-`.gitignore` (exact-path); tidak diubah,
  tidak dipindah, tidak dikompres.
- File kerja audit ini (`~/workspace/rayls-article-audit-2026-11-22/`:
  frame JPG, transkrip Whisper, `derive.py`) — catatan kerja di luar
  repo; frame adalah turunan dari footage yang di-gitignore.

### 8.4 Catatan commit

- Tidak ada file yang di-staging/commit/push dalam ronde ini maupun
  ronde revisi ini.
- Saat commit (setelah review Anara): sertakan file baru §8.1 (r3
  sebagai laporan audit yang berlaku; r1/r2 tidak ikut) + file §8.6
  yang diusulkan; perbarui INDEX/TRAIL/REPRODUCE untuk file audit
  baru (r3) — pembaruan itu BELUM dilakukan dalam ronde ini (di luar
  batas: "jangan mengubah file lain"); jalankan verifier 23/23
  sekali lagi sebelum commit.
- Pertanyaan terbuka §7.4 (Q-A, Q-B) dapat ditambahkan ke draf tiket
  setelah Anara menyetujui — bukan sekarang.

### 8.5 Verifikasi ronde revisi r3 (22 Nov 2026)

**Penjelasan perbedaan ukuran r2 (koreksi 4).** §8.5 r2 menyebut
47.530 byte, sedangkan file canonical r2 adalah **48.097 byte**
(SHA-256 `00e464f29a3615e6cd2fdef0b1b8bd2cc930917486fc00d26ae3a6711c36cd9d`,
diukur ulang ronde ini). Penyebabnya: angka 47.530 diukur pada keadaan
intermediate r2 — setelah draf §8.5 pertama ditulis, tetapi SEBELUM
§8.4 dipulihkan ke dalam file. Pemulihan §8.4 menambahkan 567 byte
(48.097 − 47.530), sehingga ukuran dan SHA berubah, tetapi teks §8.5
tidak diperbarui setelah pemulihan itu. Angka 47.530 adalah pengukuran
intermediate yang usang, bukan ukuran final. File r2 sendiri tidak
pernah diubah sesudahnya (terverifikasi: masih 48.097 byte /
`00e464f2…`). File r1 juga tidak berubah: 35.269 byte, SHA-256
`bd54c362c0418e10…`.

**Ukuran dan SHA r3.** Ukuran final r3: **59742 byte** (diukur setelah
edit terakhir; pengisian angka ini mengganti digit dengan panjang yang
sama sehingga ukuran tidak berubah). SHA-256 r3 **tidak ditulis di
dalam file ini dengan sengaja**: sebuah file tidak dapat memuat
hash-nya sendiri tanpa menjadi usang, karena menulis hash mengubah
isi file sehingga hash-nya berubah. SHA-256 final r3 tercantum dalam
pesan pengiriman laporan ini (diukur setelah edit terakhir) dan dapat
diverifikasi mandiri dengan:
`sha256sum experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r3.md`.

**Integritas (diperiksa ulang ronde ini, read-only):**
- Footage mentah: 24.777.960 byte, SHA-256
  `610a5cd30d3cdc457ea836e69c74229a6fb42d3530f4227a2269a00f4af311fa`
  — **tidak berubah**.
- VO mp3: 2.953.936 byte, SHA-256
  `ebb2fdda3d84ea99fece015ca075cd7b74f3f96a6630c13182b5eb6f2b5c6a7c`
  — **tidak berubah**.
- Raw evidence TX: manifest **20/20 OK** (SHA + ukuran cocok);
  manifest journey **12/12 OK**.
- Comparator v2.1.1: SHA-256
  `bfef1f667408b227cac5b33e27c9352b5ad721ca0b78ed91899d8befdcac08a3`
  — **tidak berubah** (tersertifikasi, tidak disentuh).
- Verifier TX: **23/23 PASS, exit 0** (dijalankan ulang).
- `contracts/addresses/addresses.json`: 9.202 byte /
  `f78f012886035836` — cocok dengan INDEX.
- Git: 28 baris status (9 modified + 19 untracked), **0 staged**,
  tidak ada commit/push (lihat §8.6).
- Sapuan redaksi r3: tidak ada pernyataan faktual bahwa transfer
  0,576 RLS adalah pembayaran fee atau ditujukan ke penerima yang
  sudah disimpulkan; seluruh penyebutan "4,416"/"4.416" berada dalam
  konteks tiga lapis (§3.2) atau sebagai aritmetika atas nilai
  tampilan aplikasi / contoh redaksi yang dilarang (K4, §3.2).

### 8.6 Daftar persis file yang diusulkan masuk commit

Pengukuran: 22 Nov 2026 ~14:10 WIB. Tidak ada staging, commit, atau
push dalam ronde ini.

#### 8.6.1 Output lengkap `git status --short` (28 baris)

```
 M README.md
 M contracts/abis/README.md
 M contracts/addresses/README.md
 M contracts/verified-source/README.md
 M experiments/README.md
 M experiments/transactions/README.md
 M findings/README.md
 M raw-data/videos/README.md
 M scripts/README.md
?? .gitignore
?? 01-no-overwrite-fix-report.md
?? INDEX.md
?? REPRODUCE.md
?? RESEARCH-TRAIL.md
?? audit-reports/
?? contracts/addresses/addresses.json
?? experiments/g1-g6-decision-table.md
?? experiments/testnet-journeys/week2-private-payment/
?? experiments/transactions/tx-09edab2b/
?? raw-data/screenshots/chk-21.jpg
?? raw-data/screenshots/chk-22.jpg
?? raw-data/screenshots/chk-23.jpg
?? runs/
?? scripts/01_network_identity.py
?? scripts/decode_tx_09edab2b.py
?? scripts/tx_audit_09edab2b.py
?? scripts/verify_tx_audit_09edab2b.py
?? tickets/rayls-team-questions-draft-2026-11-22.md
```

#### 8.6.2 Perubahan tracked: 9 file (97 insertions, 2 deletions)

| File | Perubahan |
|---|---|
| README.md | +24/−2 (status + tautan finalisasi) |
| contracts/abis/README.md | +11 (dokumentasi ABI) |
| contracts/addresses/README.md | +10 (dokumentasi peta alamat) |
| contracts/verified-source/README.md | +14 (status verified source) |
| experiments/README.md | +4 |
| experiments/transactions/README.md | +8 |
| findings/README.md | +8 |
| raw-data/videos/README.md | +11 (penanda local-only footage + VO) |
| scripts/README.md | +9 |

#### 8.6.3 File untracked: 73 file (expanded, setelah r3)

73 = 72 (sebelum r3) + r3. Rinciannya ada di §8.6.4 (71 diusulkan)
dan §8.6.5 (2 tidak diusulkan: r1, r2).

#### 8.6.4 Diusulkan masuk commit: 80 file

9 tracked-modified (§8.6.2) + 71 untracked berikut:

```
.gitignore
01-no-overwrite-fix-report.md
INDEX.md
REPRODUCE.md
RESEARCH-TRAIL.md
audit-reports/ENYGMA-TESTNET-AUDIT-REPORT.md
audit-reports/README.md
contracts/addresses/addresses.json
experiments/g1-g6-decision-table.md
experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r3.md
experiments/testnet-journeys/week2-private-payment/EDIT-PLAN.md
experiments/testnet-journeys/week2-private-payment/QA-REPORT-V2.md
experiments/testnet-journeys/week2-private-payment/README.md
experiments/testnet-journeys/week2-private-payment/build_subs.py
experiments/testnet-journeys/week2-private-payment/build_video_v2.py
experiments/testnet-journeys/week2-private-payment/enygma-week2-private-payment-final-1080p.mp4
experiments/testnet-journeys/week2-private-payment/enygma-week2-private-payment-final.mp4
experiments/testnet-journeys/week2-private-payment/manifest.json
experiments/testnet-journeys/week2-private-payment/subs.ass
experiments/transactions/tx-09edab2b/.src/build_tx_pdf.py
experiments/transactions/tx-09edab2b/.src/index.html
experiments/transactions/tx-09edab2b/.src/render-report-pass1.json
experiments/transactions/tx-09edab2b/.src/render-report-pass2.json
experiments/transactions/tx-09edab2b/.src/toc-pages.json
experiments/transactions/tx-09edab2b/01_tx_audit_complete_history.pdf
experiments/transactions/tx-09edab2b/ADDENDUM-2026-11-22.md
experiments/transactions/tx-09edab2b/TODO.md
experiments/transactions/tx-09edab2b/TX-AUDIT-REPORT.md
experiments/transactions/tx-09edab2b/decoded/audit_summary.json
experiments/transactions/tx-09edab2b/decoded/bundle-abi-extract.json
experiments/transactions/tx-09edab2b/decoded/decoded_events.json
experiments/transactions/tx-09edab2b/decoded/lookups-4byte.json
experiments/transactions/tx-09edab2b/gaps.md
experiments/transactions/tx-09edab2b/manifest.json
experiments/transactions/tx-09edab2b/raw/block.json
experiments/transactions/tx-09edab2b/raw/contracts.json
experiments/transactions/tx-09edab2b/raw/explorer-relayer-txlist.json
experiments/transactions/tx-09edab2b/raw/explorer.json
experiments/transactions/tx-09edab2b/raw/logs.json
experiments/transactions/tx-09edab2b/raw/receipt.json
experiments/transactions/tx-09edab2b/raw/registry-usernames.json
experiments/transactions/tx-09edab2b/raw/related-tx-0xacc7d175.json
experiments/transactions/tx-09edab2b/raw/transaction.json
raw-data/screenshots/chk-21.jpg
raw-data/screenshots/chk-22.jpg
raw-data/screenshots/chk-23.jpg
runs/20261121T054711Z/datasets/01_network_identity.csv
runs/20261121T054711Z/datasets/01_network_identity_checksums.sha256
runs/20261121T054711Z/datasets/01_network_identity_metadata.json
runs/20261121T054711Z/findings/verified-facts/01_network_identity_complete_report.md
runs/20261121T054711Z/findings/verified-facts/01_network_identity_verification.md
runs/20261121T054711Z/raw-data/rpc-responses/01_network_identity_raw.json
runs/20261121T054711Z/scripts/01_network_identity.py
runs/20261121T063234Z/datasets/01_network_identity.csv
runs/20261121T063234Z/datasets/01_network_identity_checksums.sha256
runs/20261121T063234Z/datasets/01_network_identity_metadata.json
runs/20261121T063234Z/findings/verified-facts/01_network_identity_verification.md
runs/20261121T063234Z/raw-data/rpc-responses/01_network_identity_raw.json
runs/20261121T063234Z/scripts/01_network_identity.py
runs/20261121T063327Z/datasets/01_network_identity.csv
runs/20261121T063327Z/datasets/01_network_identity_checksums.sha256
runs/20261121T063327Z/datasets/01_network_identity_metadata.json
runs/20261121T063327Z/findings/verified-facts/01_network_identity_verification.md
runs/20261121T063327Z/raw-data/rpc-responses/01_network_identity_raw.json
runs/20261121T063327Z/scripts/01_network_identity.py
runs/README.md
scripts/01_network_identity.py
scripts/decode_tx_09edab2b.py
scripts/tx_audit_09edab2b.py
scripts/verify_tx_audit_09edab2b.py
tickets/rayls-team-questions-draft-2026-11-22.md
```

(9 tracked dari §8.6.2 + 71 di atas = **80 file**.)

#### 8.6.5 Yang TIDAK diusulkan masuk commit

| File | Alasan |
|---|---|
| `experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22.md` (r1) | Superseded oleh r2/r3; catatan revisi lokal |
| `experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r2.md` | Superseded oleh r3; catatan revisi lokal |
| `raw-data/videos/week2-source-footage-610a5cd30d3cdc457ea836e69c74229a6fb42d3530f4227a2269a00f4af311fa.mp4` (24.777.960 byte) | Local-only, dikecualikan `.gitignore` (exact-path); hash `610a5cd3…` tidak berubah |
| `raw-data/videos/ElevenLabs_2026-11-21T13_44_30_Zara_-_The_Warm__Real-World_Conversationalist_pvc_s50_sim75_v4.mp3` (2.953.936 byte) | Local-only, dikecualikan `.gitignore` (exact-path); hash `ebb2fdda…` tidak berubah |

Tidak ada file lain di working tree di luar daftar §8.6.4 dan §8.6.5.

#### 8.6.6 Catatan sebelum commit (belum dilakukan)

- `INDEX.md`, `REPRODUCE.md`, `RESEARCH-TRAIL.md` (termasuk dalam
  §8.6.4) perlu pembaruan untuk merujuk file audit r3 — pembaruan itu
  BELUM dilakukan dalam ronde ini, sesuai batas "jangan mengubah file
  lain". Lakukan pembaruan itu sebelum commit, setelah review ini.
- `experiments/transactions/tx-09edab2b/.src/index.html` berisi teks
  lama "(the check has not been run yet)" — sengaja dipertahankan
  sebagai sumber build PDF 21 Nov (lihat finalisasi 22 Nov); jangan
  diedit tanpa keputusan rebuild PDF.
- `tickets/rayls-team-questions-draft-2026-11-22.md` termasuk sebagai
  draf — tiket BELUM dikirim.
- Jalankan verifier 23/23 sekali lagi tepat sebelum commit.

## Lampiran — bukti kerja ronde ini (di luar repo)

- `~/workspace/rayls-article-audit-2026-11-22/frames/` — 12 frame video
  final + 12 frame footage mentah (JPG, 960 px).
- `~/workspace/rayls-article-audit-2026-11-22/transcript/` — transkrip
  VO lengkap 183,56 dtk (faster-whisper-small, 4 chunk).
- `~/workspace/rayls-article-audit-2026-11-22/derive.py` — skrip
  penurunan ulang dari raw (selector, statement, ciphertext, fee,
  registry, logs).
