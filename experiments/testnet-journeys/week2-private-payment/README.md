# Week 2 private payment — testnet journey (21 Nov 2026)

Anara's own hands-on Enygma Public Testnet experiment, recorded on video:
a private payment of **6 $RLS from @anara to @kittynim**, with the ElevenLabs
(Zara) voice-over narrating what the on-chain data does and does not show.
The video is experiment documentation, not a promo.

## What happened (verified facts from the footage + the TX audit)

- Sender: @anara (`0x0c5b369ad7d0c4e051a2887575f7fc85e0ccd0b5`).
  Receiver: **@kittynim** (`0x680d90983da58bcb7d127e3421193274e84e0efc`) —
  confirmed on screen in three places and by the account owner (22 Nov 2026).
- Amount: 6 $RLS. Sender shielded balance 14.324 → 3.908; receiver shielded
  balance 321.4 → 327.4.
- Fee shown in the wallet: 3.84 gas + 0.58 Rayls Foundation = 4.42 $RLS
  (rounded display). The transaction's statement array contains the
  integer 4.416 × 10¹⁸, which the app presents as 4.416 RLS total fee —
  see the article audit (`ARTICLE-AUDIT-2026-11-22-r3.md` §3.2): the
  integer is a verified fact, the RLS unit is an interpretation, and
  the "total fee" meaning is an inference.
- ZK proof: 256 bytes, generated in-browser in ~10 s (per the success screen).
- On-chain transaction: `0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb`,
  block 24825928, transferV2 to SharedVault, public sender = Relayer,
  value field 0 USDR. Audited in full in
  `experiments/transactions/tx-09edab2b/` (independent verifier 23/23 PASS).

## Files in this folder

| file | role |
|---|---|
| `enygma-week2-private-payment-final-720p-public.mp4` | Final video, 720p (1280×720, 30 fps, 185.53 s). **Public sanitized version** (22 Nov 2026): truncated Enygma Spend/View key fragments blurred at t 20–24, 82–88, 109–115, 138–144, 176–185.533 s; otherwise the same content as the original. This is the version committed to the public repository. |
| `enygma-week2-private-payment-final-1080p-public.mp4` | Final video, 1080p upscale (lanczos from the 720p master — bigger/smoother on large screens, no new detail). **Public sanitized version** (22 Nov 2026), same blur ranges as the 720p public version. This is the version committed to the public repository. |
| `ARTICLE-AUDIT-2026-11-22-r3.md` | Article audit, revision 3 (current). "What Can the Public Actually See When Two Accounts Make a Private Transfer on Rayls Enygma?" — evidence-classified audit of this experiment for the article. |
| `ARTICLE-AUDIT-2026-11-22-addendum-f17.md` | Addendum to r3: §6 F17 classification split (F17a/F17b) + pre-commit content and publication-suitability checks. |
| `enygma-week2-private-payment-final.mp4`, `enygma-week2-private-payment-final-1080p.mp4` | Original final videos (720p / 1080p). **LOCAL-ONLY — excluded from the public repository by `.gitignore`** (22 Nov 2026): they still show truncated Enygma Spend/View key fragments. Hashes kept in `manifest.json` for provenance; the public sanitized versions above are the committed files. |
| `ARTICLE-AUDIT-2026-11-22.md` (r1), `ARTICLE-AUDIT-2026-11-22-r2.md` (r2) | Superseded revisions — local record only, NOT committed. |
| `subs.ass` | Subtitles, 44 cues (Liberation Sans, amber highlights). All on-screen token text uses **$RLS**. |
| `build_subs.py` | Generates `subs.ass` from the VO script (source of truth for subtitle text). |
| `build_video_v2.py` | Builds the video-only track from the source footage segments. |
| `EDIT-PLAN.md` | Edit plan: verified facts from the footage, scene map, subtitle rules. |
| `QA-REPORT-V2.md` | QA report for the v2 rebuild (defects found and fixed, verification). |
| `manifest.json` | Bytes + SHA-256 + source path for every file copied here and in `raw-data/`. |
| `README.md` | This file. |

## Inputs (stored under `raw-data/`, not here)

- `raw-data/videos/week2-source-footage-610a5cd30d3cdc457ea836e69c74229a6fb42d3530f4227a2269a00f4af311fa.mp4`
  — Anara's activity recording, 1300×720, 30 fps, 241.728 s. The filename is
  its content SHA-256. Renamed on copy only to record that it is the Week 2
  source footage; content byte-identical. **LOCAL-ONLY — excluded from the
  public repository by `.gitignore` (22 Nov 2026); hash kept in
  `manifest.json` for provenance.**
- `raw-data/videos/ElevenLabs_2026-11-21T13_44_30_Zara_-_The_Warm__Real-World_Conversationalist_pvc_s50_sim75_v4.mp3`
  — voice-over, 183.562 s, used as-is (never regenerated). **LOCAL-ONLY —
  excluded from the public repository by `.gitignore` (22 Nov 2026); hash
  kept in `manifest.json` for provenance.**
- `raw-data/screenshots/chk-21-public.jpg`, `chk-22-public.jpg`,
  `chk-23.jpg` — frames at seconds 21/22/23 of the final 1080p video,
  extracted to verify the "Enygma" spelling after the revision (all three
  read "Enygma"). chk-21/22 are the **public sanitized versions** (22 Nov
  2026): the Enygma Spend/View key line is blurred. The originals
  (`chk-21.jpg`, `chk-22.jpg`) still show the truncated key fragments and
  are **LOCAL-ONLY — excluded from the public repository by `.gitignore`**;
  hashes kept in `manifest.json` for provenance. chk-23 is unchanged.

## Spelling fix + filename lesson (21 Nov 2026)

- The subtitles first rendered "Enigma" in 2 cues. Fixed in `build_subs.py`,
  subtitles regenerated, both finals re-rendered (22:25 WIB). The app's own
  text inside the recorded footage ("Rayls Enigma" feedback popup) cannot be
  changed via subtitles and is unchanged.
- The revised 1080p was first sent under the SAME filename as the old version,
  so Anara's phone opened the old download. It was re-sent as
  `...-1080p-v2.mp4`, byte-identical to the 1080p file in this folder (same
  SHA-256) — it is NOT a second video and is NOT copied here. Lesson recorded:
  a revised file always gets a new, distinct filename.

## What is NOT in this repo (superseded / working files, retained outside)

- `enygma-week2-private-payment-final-v720-backup.mp4` and
  `enygma-week2-private-payment-final-1080p-v720-backup.mp4` — superseded
  old-spelling versions (pre-"Enygma" fix). Kept in
  `~/workspace/enygma-week2-video/`, not copied here.
- `subs-v2-backup.ass` — pre-fix subtitle backup. Same location, not copied.
- `enygma-week2-private-payment-final-1080p-v2.mp4` — byte-identical duplicate
  of the 1080p file (see filename lesson above). Not copied.
- Intermediate working files (`video_only.mp4`, `video_only_v2.mp4`,
  `segments_v2/`, `frames/`, `qa/`, `transcript/`, `zoom_long.mp4`, etc.) —
  retained in `~/workspace/enygma-week2-video/`, not copied. The reproducible
  path is: `build_subs.py` → `subs.ass`; `build_video_v2.py` → video-only
  track; mux per the recipe in `QA-REPORT-V2.md`.
