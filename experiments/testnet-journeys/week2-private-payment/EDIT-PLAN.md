# Enygma Week 2 — Edit Plan (video dokumentasi eksperimen private payment)

Sumber (jangan diubah):
- Footage: ~/workspace/user/media_library/video/61/610a5cd30d3cdc457ea836e69c74229a6fb42d3530f4227a2269a00f4af311fa.mp4
  1300x720, 30fps, 241.73 dtk. Audio native SILENT (mean/max -91 dB) -> tidak ada bed audio.
- VO: ~/workspace/user/files/ElevenLabs_2026-11-21T13_44_30_Zara_-_The_Warm__Real-World_Conversationalist_pvc_s50_sim75_v4.mp3
  ElevenLabs Zara, 183.56 dtk, dipakai apa adanya. Mean -23.2 dB, max -0.9 dB.
- Output: ~/workspace/enygma-week2-video/enygma-week2-private-payment-final.mp4 — 1280x720 HD, H.264 + AAC.

## ATURAN TEKS TAMPILAN (koreksi Anara, 21 Nov 21:19 WIB)
Di SEMUA teks tampilan video (subtitle, highlight/callout): token ditulis **$RLS**, bukan RLS.
Contoh: "6 $RLS", "4.42 $RLS", "shielded $RLS". Hanya teks di layar; audio VO tetap apa adanya.
Subtitles dibuat dari naskah VO dengan penggantian RLS -> $RLS pada teks tampilannya.

## FAKTA TERVERIFIKASI DARI FOOTAGE (dipakai apa adanya)
- Username penerima di layar: **@kittynim** (bukan @kittymin seperti di brief, bukan "Kittyman" seperti
  transkrip VO). Terlihat jelas di: menu akun (t=45), Receive page, kolom To send form (t=85, t=100),
  baris Auditor "@anara paid @kittynim 6 $RLS". Alamat 0x680D...0eFC. Subtitle/highlight memakai @kittynim.
  (Audio VO mengucapkan nama itu ambigu; teks layar adalah kebenaran yang bisa dicek.)
- Pengirim @anara. Saldo shielded $RLS pengirim 14.324 -> 3.908 (selisih 10.416).
  Saldo shielded $RLS penerima 321.4 -> 327.4 (t=45: 321.4; t=170: 327.4).
- Fee di send page: 3.84 gas + 0.58 Rayls Foundation (15%) = 4.42 $RLS (tampilan).
  Detail activity: Relayer fee 4.416 $RLS. Keduanya benar di konteksnya (4.42 = pembulatan tampilan).
- ZK proof: "256 bytes", "Made in 10 s, in this tab" (layar sukses t=145).
- Explorer: tx 0x09edab2b...eff525bb, Status Success, method transferV2, Block 24825928,
  Timestamp Nov 21 2026 16:40:42 (+07:00 UTC). From = relayer @rayls-relayer; To = SharedVault;
  Value 0 ($USDr); 3 commitments + 3 encrypted notes (detail activity).
- Catatan footage: dialog Chrome "Halaman Tidak Merespons" muncul singkat ~t=189-191 dan ~t=223
  (DIPOTONG dari edit — popup error browser, bukan bagian eksperimen).
- Detour Send $USDr (t=22-40 dan t=70-75) DIPOTONG — VO tidak menyebut $USDr, token yang dipakai $RLS.
- Menu akun @anara (t=2-11) DIPOTONG. Interstitial "Quantum-private payments" (t=117-119) DIPOTONG.

## PETA SCENE (waktu footage -> beat VO; VO mulai 0.8 dtk di video final)
| # | VO (dtk) | Footage | Isi visual |
|---|----------|---------|------------|
| 1 | 0.0-10.0 | 11.0-21.0 | Dashboard @anara ($5.32, shielded 14.324) |
| 2 | 10.0-16.5 | freeze t=21.0 (6.5 dtk) | Dashboard hold |
| 3 | 16.5-22.5 | 47.0-53.0 | Dashboard @kittynim ($12.42) |
| 4 | 22.5-29.6 | 55.0-62.1 | Receive @kittynim (QR + alamat) |
| 5 | 29.9-35.0 | 76.0-81.1 | Send $RLS, token $RLS |
| 6 | 35.0-44.0 | 80.0-86.0 + 93.0-96.0 | Ketik @kittynim; amount 6 |
| 7 | 44.0-57.2 | 96.0-108.0 + freeze 1.2 dtk | Fee breakdown 4.42 $RLS |
| 8 | 57.2-62.0 | 108.0-112.8 | Passkey dialog |
| 9 | 62.0-70.0 | 120.0-128.0 | Proof steps, grid mengisi |
| 10 | 70.0-76.0 | 139.0-145.0 | Sukses: 256 bytes, Made in 10 s |
| 11 | 76.0-83.0 | 145.0-152.0 | Sukses: Sent 6 $RLS to @kittynim |
| 12 | 83.0-87.1 | 172.0-176.1 | Activity penerima: Received +6 $RLS |
| 13 | 87.1-92.0 | 168.0-171.0 + freeze 1.9 dtk | Dashboard penerima: shielded 327.4 |
| 14 | 92.0-101.0 | 161.0-165.0 + freeze 5.0 dtk | Dashboard pengirim: shielded 3.908 |
| 15 | 101.0-110.0 | 206.0-212.0 + freeze 3.0 dtk | Detail: Relayer fee 4.416 $RLS |
| 16 | 110.0-117.1 | 196.0-201.0 + freeze 2.1 dtk | Detail activity terbuka |
| 17 | 117.5-126.0 | 233.0-241.5 | Explorer: transferV2, Block 24825928 |
| 18 | 126.0-131.0 | freeze t=241.5 (5.0 dtk) | Explorer (From relayer / Value 0) |
| 19 | 131.0-140.0 | 201.0-206.0 + freeze 4.0 dtk | Detail: Value 0 ($USDr) |
| 20 | 140.0-147.4 | 183.0-187.0 + 212.0-215.4 | Activity + commitments |
| 21 | 147.4-158.0 | 215.4-222.0 + freeze 4.0 dtk | Encrypted notes |
| 22 | 158.0-177.3 | freeze t=237.0, slow zoom 19.3 dtk | Explorer hold (closing) |
| 23 | 177.3-183.2 | 176.0-181.9 | Activity list (penutup) |

Durasi video target: 0.8 (lead-in) + 183.56 (VO) + ~1.0 (tail) = ~185.4 dtk.
Freeze = tpad (layar statis, tidak terlihat sebagai freeze). Zoom pelan = zoompan 1.00 -> 1.12.

## SUBTITLE (ASS, Liberation Sans, 22pt, putih + outline gelap, bawah tengah, maks 2 baris)
- Teks dari naskah VO (audio sebagai kebenaran), dengan RLS -> $RLS.
- Kata kunci diwarnai amber (#FFC53D): @anara, @kittynim, 6 $RLS, 4.42 $RLS, 4.416 $RLS,
  256 byte, 10 seconds, zero-knowledge proof, Block 24,825,928, transferV2, SharedVault,
  Relayer, 0 USDR, 321.4, 327.4, 14.324, 3.908, 10.416.
- Timing dari word timestamps faster-whisper (transcript/words_full.json).
