# G.1–G.6 — decision table (NOT run; needs Anara's approval per experiment)

Source: initial audit `audit-reports/ENYGMA-TESTNET-AUDIT-REPORT.md` §G
(22 Nov 2026). Nothing here has been executed. Each row states what
the experiment would do, what it needs, whether it is read-only or
changes state, the risks, a rough cost/time estimate, and the decision
still needed. **Estimates are estimates** (based on the Week 2 TX audit:
chain gas ~0.063 RLS per tx; faucet 1×/hour per the pilot blog; testnet
RLS is faucet-funded, not bought). Nothing is a commitment.

## Table

| # | Tujuan | Hipotesis | Kebutuhan data | Read-only / transaksi | Risiko | Estimasi biaya / waktu | Keputusan yang diperlukan |
|---|---|---|---|---|---|---|---|
| G.1 | Alur lengkap shield → transfer → unshield pada wallet testnet baru, tiap langkah dalam jumlah kecil dan berbeda agar dapat dilacak; cocokkan pola event dengan klasifikasi D.7 | Ketiga aksi memang terpisah seperti yang diklasifikasikan (event log berbeda per aksi) | Wallet testnet baru; faucet RLS; tx hash + blok + event log tiap langkah | **Transaksi** (4 tx: registrasi, shielding, transfer, unshielding) + perubahan state | Wallet baru + faucet; jumlah kecil tapi tetap ada biaya gas testnet; risiko salah langkah pada alur (mitigasi: jumlah kecil, satu langkah per satu, verifikasi tiap receipt) | Biaya: gas testnet ~0.06 RLS/tx × 4 ≈ 0.25 RLS (faucet, $0). Waktu: ~1–2 jam kerja aktif + jeda faucet 1×/jam | Setujui/tolak; jumlah per langkah; apakah memakai wallet baru atau wallet yang sudah ada |
| G.2 | Uji apakah jumlah shielding terlihat publik lewat log token ERC-20 (Transfer RLS + USDr) pada rentang blok yang sama dengan vault yx, dicocokkan dengan 272 tx shielding | Jumlah shielding terlihat lewat log token meskipun log vault tidak menunjukkannya — atau tidak terlihat | Log `Transfer` RLS (`0x07e17E17…`) + USDr (`0x0000…0400`) pada rentang blok vault yx; daftar 272 tx shielding | **Read-only** (hanya baca log via RPC/Explorer; tanpa transaksi, tanpa signature) | Tidak ada risiko dana; risiko hanya waktu analisis + volume log besar (272 tx × rentang blok) | Biaya: $0. Waktu: ~1–2 jam analisis (fetch log + pencocokan) | Setujui/tolak; rentang blok yang dipakai |
| G.3 | Ukur fee aktual per aksi (registrasi, shielding, transfer, unshielding) dari receipt; bandingkan dengan klaim docs (relayer 15% ke Foundation; USDr +0,25%); selidiki asal selisih 0,0001 RLS | Fee per aksi dapat diukur dan dijelaskan; selisih 0,0001 RLS punya komponen yang teridentifikasi (bukan rounding) | Receipt tx eksperimen per aksi; breakdown fee wallet vs on-chain; data demo 13 Nov (catatan: tx hash demo tidak tercatat) | **Transaksi** (memakai tx dari G.1; tanpa tx baru jika G.1 sudah jalan) + analisis read-only | Sama seperti G.1 jika butuh tx baru; jika memakai tx G.1, tidak ada risiko tambahan | Biaya: $0 tambahan jika memakai tx G.1 (jika tx baru: ~0.06 RLS/tx). Waktu: ~1 jam analisis | Setujui/tolak; apakah digabung dengan G.1 atau berdiri sendiri |
| G.4 | Ukur waktu proving secara lokal (atau catat waktu dari UI demo); bandingkan dengan 4 angka resmi yang saling berbeda (408 ms / ~2,2 dtk / ~3 dtk / "under 4 s") | Angka-angka resmi diukur dalam kondisi berbeda (perangkat, ukuran input, jaringan) | Waktu proving lokal + perangkat + ukuran input + kondisi jaringan; 4 angka resmi + sumbernya | **Read-only** (pengukuran lokal; tanpa transaksi, tanpa signature) | Tidak ada risiko dana; angka tanpa konteks tidak bermakna (mitigasi: catat perangkat + input + jaringan) | Biaya: $0. Waktu: ~30 menit pengukuran + pencatatan | Setujui/tolak; perangkat yang dipakai untuk pengukuran |
| G.5 | Uji deployment bx dan forwarder "next": apakah bx masih dapat dipakai (demo konfigurasi bx); amati apakah registrasi baru terus memakai forwarder `0x12B66400…` | bx adalah deployment awal yang tidak dilanjutkan; rotasi forwarder sedang berjalan (atau tidak) | Percobaan demo konfigurasi bx; pengamatan registrasi baru (log `UsernameSet` terbaru) | **Campuran**: pengamatan forwarder = read-only; percobaan demo bx = transaksi (jika demo bx dijalankan) | Demo bx bisa gagal / tidak didukung (itu sendiri adalah hasil); jangan menyimpulkan apa pun tentang bx sebelum ticket Q2 dijawab | Biaya: gas testnet jika demo bx dijalankan (~0.06 RLS). Waktu: ~1 jam (pengamatan + percobaan) | Setujui/tolak; apakah demo bx dijalankan, atau hanya pengamatan forwarder; urutan vs ticket Q2 |
| G.6 | Monitoring kontinu + finality: pencatatan harian jumlah tx per tipe selama seminggu (bukan 2 snapshot saja); eksperimen finality terpisah jika memungkinkan | Pola aktivitas berubah antar hari; waktu finality dapat diukur dari RPC/Explorer | Jumlah tx per tipe per hari (7 hari); waktu hingga tx dianggap final menurut RPC/Explorer | **Read-only** (monitoring + pengukuran finality; tanpa transaksi) — load test TIDAK termasuk (hanya di lingkungan yang sesuai, bukan membanjiri public testnet) | Beban kerja harian selama seminggu; finality mungkin tidak dapat diukur dengan presisi dari data publik | Biaya: $0. Waktu: ~15 menit/hari × 7 hari + ~1 jam analisis akhir | Setujui/tolak; tanggal mulai; apakah finality diukur bersamaan |

## Ringkasan untuk keputusan

- **Read-only saja (tanpa transaksi, tanpa risiko dana):** G.2, G.4, G.6
  (dan pengamatan forwarder di G.5).
- **Perlu transaksi (state berubah, gas testnet):** G.1, G.3 (jika tx
  baru), G.5 (jika demo bx dijalankan).
- **Urutan yang disarankan (bukan keputusan):** ticket dulu (Q1–Q10),
  lalu G.2 + G.4 (read-only, murah, menutup gap F.1 dan proof-time),
  lalu G.1 + G.3 (satu paket transaksi), lalu G.5 (setelah jawaban
  ticket Q2), lalu G.6 (monitoring seminggu, bisa jalan paralel).
- **Yang TIDAK direkomendasikan (audit §G.8):** mencoba menjadi
  auditor; menyimpulkan apa pun tentang Enygma Sovereign dari
  ketiadaan data publik; menyajikan angka "volume" yang mencampur
  token berbeda tanpa caveat desimal.

## Status

- 22 Nov 2026: tabel ini dibuat sebagai bahan keputusan. Belum ada
  eksperimen yang dijalankan. Ticket draft ada di
  `tickets/rayls-team-questions-draft-2026-11-22.md` (DRAFT, belum
  dikirim; dikeluarkan dari batch commit saat ini — draf lokal untuk
  revisi terpisah).
