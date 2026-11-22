# Enygma Week 2 — Video Final QA Report (v2 rebuild, 21 Nov 2026)

## Deliverable
- **File:** `enygma-week2-private-payment-final.mp4`
- **Path:** `~/workspace/enygma-week2-video/enygma-week2-private-payment-final.mp4`
- **Specs:** 1280×720, 30 fps, H.264 + AAC, 185.53 s, 10,686,373 bytes (~10.7 MB), 5,566 frames
- **Subtitles:** `subs.ass` — 44 cues, Liberation Sans 24pt, white + black outline, amber (#FFC53D) highlights; all on-screen token text uses **$RLS** (0 bare "RLS"); receiver is **@kittynim** (3 occurrences, 0 "@kittymin")
- **Audio:** ElevenLabs Zara VO as-is, adelay 800 ms, volume ×2.0 (+6 dB), alimiter 0.89; mean −16.5 dB, max 0.0 dB; silence only 0–0.85 s lead-in + natural VO pauses. Source native audio is effectively silent (−91 dB), so no bed was mixed.

## What v1 got wrong and how v2 fixed it
1. **tpad freezes rendered black** (9 regions, proven by isolated test) → v2 renders every segment as a separate clip; freezes are still-frame `-loop 1` inputs at source times 21.0, 106.0, 171.0, 165.0, 212.0, 201.0, 241.5, 206.0, 222.0, 181.9; zoom reuses the verified `zoom_long.mp4`; concat via the concat demuxer (no filter_complex, no tpad, no label collisions).
2. **$USDr visible in S5** (Send $USDr page + open token dropdown) → S5 now starts at source 81.5 s, after $RLS is selected; S6 re-split (86.6–90.6 + 91.0–96.0).
3. **Unexplained 2.9 s black at 163.2–166.1 in the zoom region** → gone in v2 (demuxer concat, no duplicate [v21] label).
4. **Subtitle covering key data at 2 beats** (found in v2 frame QA) → fee cue (47.84–59.58) and sender-balance cue (96.64–104.50) moved to a top-aligned style; fee box (4.42 $RLS / 3.84 + 0.58) and sender $RLS row (3.908) are now fully visible. Trade-off: top subtitles cover the form's top token row (fee cue) and the "Received +6 $RLS" header (detail page at ~104 s) — neither is key data for those beats.

## QA verified (final v3, `-ss` frame extraction — reliable; select/tile sheets are not trusted)
- blackdetect (pic_th 0.98, pix_th 0.10): **no black regions** on the final file.
- 24 full-res frames read across all beats; per-clip durations all within 0.05 s of target (total drift +0.13 s, imperceptible).
- Sync spot-checked against whisper word times: "The interface reported" 70.28 s → success screen; "The explorer shows" 119.26 s → Explorer; "The receiver can confirm" 176.48 s → activity list; "set the amount to 6 $RLS" → Amount field shows 6.
- Key data visible on screen: @anara dashboard 14.324 → 3.908; @kittynim dashboard 327.4; fee 3.84 + 0.58 = 4.42 $RLS; detail relayer fee 4.416 $RLS; proof 256 bytes, Made in 10 s; Explorer Success / transferV2 / Block 24825928 / From relayer 0xa5f0… / SharedVault; commitments + encrypted notes.

## VO → footage scene map (edit seconds → source seconds)
| Edit | VO beat | Footage |
|---|---|---|
| 0–10 | Intro: what does a private payment leave behind? | @anara dashboard 11–21 + freeze 21.0 |
| 10–16.5 | (freeze) | dashboard hold |
| 16.5–22.5 | Two testnet accounts | @kittynim dashboard 47–53 |
| 22.5–29.6 | Receiver account | Receive page 55–62.1 |
| 29.6–34.7 | Opened send page | Send $RLS form 81.5–86.6 |
| 34.7–44 | Chose RLS, entered @kittynim, amount 6 | typing 86.6–90.6 + amount 91–96 |
| 44–57.2 | Fee breakdown 3.84 + 0.58 = 4.42 | fee screen 96–108 + freeze 106.0 |
| 57.2–62 | Passkey confirm | passkey dialog 108–112.8 |
| 62–70 | Proof: notes, encrypt, ZK proof | proof steps 120–128 |
| 70–76 | 256-byte proof, 10 s | success screen 139–145 |
| 76–83 | Transaction went through, 6 $RLS sent | success screen 145–152 |
| 83–87.1 | Receiver activity: 6 $RLS received | receiver activity 172–176.1 |
| 87.1–92 | Receiver balance 321.4 → 327.4 | receiver dashboard 168–171 + freeze 171.0 |
| 92–101 | Sender balance 14.324 → 3.908 | sender dashboard 161–165 + freeze 165.0 |
| 101–110 | Difference 10.416; 6 + 4.416 fee | activity detail 206–212 + freeze 212.0 |
| 110–117.1 | What the blockchain recorded | detail 196–201 + freeze 201.0 |
| 117.5–126 | Explorer: transferV2, Block 24,825,928 | Explorer 233–241.5 + freeze 241.5 |
| 126–131 | Public sender is the Relayer | detail 201–206 + freeze 206.0 |
| 131–140 | Value field 0 USDR | activity 183–187 |
| 140–147.4 | Receiver activity confirms 6 $RLS | detail 212–215.4 |
| 147.4–158 | Commitments + encrypted notes | detail 215.4–222 + freeze 222.0 |
| 158–177.3 | Transaction isn't invisible; block + Relayer recorded | Explorer slow zoom 19.3 s |
| 177.3–183.2 | Receiver confirms; public record differs | activity 176–181.9 + freeze 181.9 |

## Discrepancies (already established; unchanged)
1. **Receiver username is @kittynim, not @kittymin.** Verified on screen in three places (account menu, To field, send form: "@kittynim 0x680D…0eFC can receive shielded payments"). The brief and VO transcript say @kittymin / "Kittyman"; subtitles/highlights use the on-screen @kittynim. VO audio unchanged.
2. **4.42 vs 4.416 $RLS is rounding, not a discrepancy:** 4.42 is the rounded displayed total (3.84 + 0.58); 4.416 is the exact relayer fee in the detailed activity explanation. Both shown as-is.

## Known minor issues (accepted, not blockers)
- Subtitles occasionally overlap non-key UI text at the bottom of a few frames (e.g. the "Public / Hidden" explainer rows on the send form; the "NFTs / None yet" line on the dashboard; the "Hand it to the relayer" step row during proof). Key numbers/data are never covered.
- The feedback popup ("You just did your first send…") covers the right ~35% of the success screen from ~t=142 s — it is in the source recording and cannot be removed.
- Both "Halaman Tidak Merespons" (Page unresponsive) dialogs and the two $USDr send detours were cut.
