# Enygma Week 2 — Edit Plan (private payment experiment documentation video)

Sources (do not change):
- Footage: ~/workspace/user/media_library/video/61/610a5cd30d3cdc457ea836e69c74229a6fb42d3530f4227a2269a00f4af311fa.mp4
  1300x720, 30fps, 241.73 s. Native audio SILENT (mean/max -91 dB) -> no audio bed.
- VO: ~/workspace/user/files/ElevenLabs_2026-11-21T13_44_30_Zara_-_The_Warm__Real-World_Conversationalist_pvc_s50_sim75_v4.mp3
  ElevenLabs Zara, 183.56 s, used as-is. Mean -23.2 dB, max -0.9 dB.
- Output: ~/workspace/enygma-week2-video/enygma-week2-private-payment-final.mp4 — 1280x720 HD, H.264 + AAC.

## ON-SCREEN TEXT RULES (Anara's correction, 21 Nov 21:19 WIB)
In ALL on-screen video text (subtitles, highlights/callouts): the token is written **$RLS**, not RLS.
Example: "6 $RLS", "4.42 $RLS", "shielded $RLS". On-screen text only; the VO audio stays as-is.
Subtitles are made from the VO script with RLS -> $RLS replaced in the displayed text.

## VERIFIED FACTS FROM THE FOOTAGE (used as-is)
- Recipient username on screen: **@kittynim** (not @kittymin as in the brief, not "Kittyman" as in the VO transcript). Clearly visible in: the account menu (t=45), Receive page, the To column of the send form (t=85, t=100), the Auditor row "@anara paid @kittynim 6 $RLS". Address 0x680D...0eFC. Subtitles/highlights use @kittynim. (The VO audio pronounces that name ambiguously; the on-screen text is the checkable truth.)
- Sender @anara. Sender shielded $RLS balance 14,324 -> 3,908 (difference 10,416). Recipient shielded $RLS balance 321.4 -> 327.4 (t=45: 321.4; t=170: 327.4).
- Fee on the send page: 3.84 gas + 0.58 Rayls Foundation (15%) = 4.42 $RLS (display). Activity detail: Relayer fee 4.416 $RLS. Both are correct in their context (4.42 = display rounding).
- ZK proof: "256 bytes", "Made in 10 s, in this tab" (success screen t=145).
- Explorer: tx 0x09edab2b...eff525bb, Status Success, method transferV2, Block 24825928, Timestamp Nov 21 2026 16:40:42 (+07:00 UTC). From = relayer @rayls-relayer; To = SharedVault; Value 0 ($USDr); 3 commitments + 3 encrypted notes (activity detail).
- Footage note: Chrome "Page Unresponsive" dialog appears briefly ~t=189-191 and ~t=223 (CUT from the edit — a browser error popup, not part of the experiment).
- $USDr Send detour (t=22-40 and t=70-75) CUT — the VO does not mention $USDr; the token used is $RLS.
- @anara account menu (t=2-11) CUT. "Quantum-private payments" interstitial (t=117-119) CUT.

## SCENE MAP (footage time -> VO beat; VO starts 0.8 s into the final video)
| # | VO (s) | Footage | Visual content |
|---|----------|---------|------------|
| 1 | 0.0-10.0 | 11.0-21.0 | Dashboard @anara ($5.32, shielded 14,324) |
| 2 | 10.0-16.5 | freeze t=21.0 (6.5 s) | Dashboard hold |
| 3 | 16.5-22.5 | 47.0-53.0 | Dashboard @kittynim ($12.42) |
| 4 | 22.5-29.6 | 55.0-62.1 | Receive @kittynim (QR + address) |
| 5 | 29.9-35.0 | 76.0-81.1 | Send $RLS, token $RLS |
| 6 | 35.0-44.0 | 80.0-86.0 + 93.0-96.0 | Type @kittynim; amount 6 |
| 7 | 44.0-57.2 | 96.0-108.0 + freeze 1.2 s | Fee breakdown 4.42 $RLS |
| 8 | 57.2-62.0 | 108.0-112.8 | Passkey dialog |
| 9 | 62.0-70.0 | 120.0-128.0 | Proof steps, grid filling |
| 10 | 70.0-76.0 | 139.0-145.0 | Success: 256 bytes, Made in 10 s |
| 11 | 76.0-83.0 | 145.0-152.0 | Success: Sent 6 $RLS to @kittynim |
| 12 | 83.0-87.1 | 172.0-176.1 | Recipient activity: Received +6 $RLS |
| 13 | 87.1-92.0 | 168.0-171.0 + freeze 1.9 s | Recipient dashboard: shielded 327.4 |
| 14 | 92.0-101.0 | 161.0-165.0 + freeze 5.0 s | Sender dashboard: shielded 3,908 |
| 15 | 101.0-110.0 | 206.0-212.0 + freeze 3.0 s | Detail: Relayer fee 4.416 $RLS |
| 16 | 110.0-117.1 | 196.0-201.0 + freeze 2.1 s | Activity detail open |
| 17 | 117.5-126.0 | 233.0-241.5 | Explorer: transferV2, Block 24825928 |
| 18 | 126.0-131.0 | freeze t=241.5 (5.0 s) | Explorer (From relayer / Value 0) |
| 19 | 131.0-140.0 | 201.0-206.0 + freeze 4.0 s | Detail: Value 0 ($USDr) |
| 20 | 140.0-147.4 | 183.0-187.0 + 212.0-215.4 | Activity + commitments |
| 21 | 147.4-158.0 | 215.4-222.0 + freeze 4.0 s | Encrypted notes |
| 22 | 158.0-177.3 | freeze t=237.0, slow zoom 19.3 s | Explorer hold (closing) |
| 23 | 177.3-183.2 | 176.0-181.9 | Activity list (closing) |

Target video duration: 0.8 (lead-in) + 183.56 (VO) + ~1.0 (tail) = ~185.4 s.
Freeze = tpad (static screen, does not look like a freeze). Slow zoom = zoompan 1.00 -> 1.12.

## SUBTITLES (ASS, Liberation Sans, 22pt, white + dark outline, bottom center, max 2 lines)
- Text from the VO script (audio as the truth), with RLS -> $RLS.
- Keywords colored amber (#FFC53D): @anara, @kittynim, 6 $RLS, 4.42 $RLS, 4.416 $RLS,
  256 byte, 10 seconds, zero-knowledge proof, Block 24,825,928, transferV2, SharedVault,
  Relayer, 0 USDR, 321.4, 327.4, 14,324, 3,908, 10,416.
- Timing from faster-whisper word timestamps (transcript/words_full.json).
