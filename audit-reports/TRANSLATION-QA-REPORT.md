# Translation QA Report — ENYGMA Testnet Audit Report (ID → EN)

**Date:** 22 November 2026 (23:30–23:45 WIB)
**Branch:** `docs/public-documentation-review` (from `deb3d09`; `main` untouched)
**Scope:** full translation of the initial audit report from Indonesian to
English. No summary, no dropped sections.

## Files

| File | Language | Lines | Bytes | SHA-256 |
|---|---|---|---|---|
| `ENYGMA-TESTNET-AUDIT-REPORT.md` | Indonesian (original, main for now) | 617 | 64,787 | `1d2ab730a6df4abc99af830ac1ef4e3a7d8845b3b78ee51c9a7dcda51c50c711` |
| `ENYGMA-TESTNET-AUDIT-REPORT.en.md` | English (translation, candidate main) | 617 | 65,433 | `13622c8faf80ab4c70077d8976b7d8893b34ebebe41f06f9174e3dd98ce76b10` |
| `ENYGMA-TESTNET-AUDIT-REPORT.id.md` | Indonesian (backup copy of original) | 617 | 64,787 | `1d2ab730a6df4abc99af830ac1ef4e3a7d8845b3b78ee51c9a7dcda51c50c711` |

The original's hash is unchanged (`1d2ab730…` — the same hash recorded in
`audit-reports/README.md` when the report was first copied in). The backup
`.id.md` is byte-identical to the original.

## Method

The English text was produced as a complete translation, then checked by an
independent script (not by the translator's own word): both files were split
into 13 blocks (preamble + 12 level-2 sections) and, per block, the sets of
0x-hex strings, bare hex strings (commits/SHAs), URLs, and numbers
(separators stripped) were compared with multiplicities. Heading structure,
table rows, code fences, evidence labels, and critical warnings were checked
separately. Every count difference found was traced to its exact line and is
explained in § "Explained differences" below — none was left as an
unexplained mismatch.

## Section-by-section completeness

All 13 blocks: line counts identical, and every extracted set matches
(hex / URLs / numbers / bare hex, including multiplicities).

| Block | Lines ID / EN | 0x-hex | URLs | Numbers | Verdict |
|---|---|---|---|---|---|
| (preamble: title + header fields) | 8 / 8 | 0 / 0 | 0 / 0 | 16 / 16 | OK |
| Taksonomi bukti (evidence taxonomy) | 12 / 12 | 0 / 0 | 0 / 0 | 0 / 0 | OK |
| Ringkasan temuan (summary of findings) | 15 / 15 | 2 / 2 | 1 / 1 | 70 / 70 | OK |
| A. Ringkasan kondisi workspace | 36 / 36 | 0 / 0 | 3 / 3 | 76 / 76 | OK |
| B. Repository GitHub dan dokumentasi | 36 / 36 | 1 / 1 | 0 / 0 | 47 / 47 | OK |
| C. Arsitektur dan konfigurasi | 115 / 115 | 44 / 44 | 6 / 6 | 488 / 488 | OK |
| D. Aktivitas on-chain yang teramati | 116 / 116 | 47 / 47 | 1 / 1 | 597 / 597 | OK |
| E. Kelayakan pengukuran volume | 57 / 57 | 2 / 2 | 2 / 2 | 56 / 56 | OK |
| F. Keterbatasan data aktivitas | 31 / 31 | 1 / 1 | 0 / 0 | 12 / 12 | OK |
| G. Peluang eksperimen berbasis data | 48 / 48 | 3 / 3 | 0 / 0 | 39 / 39 | OK |
| H. Rekomendasi struktur repository | 45 / 45 | 0 / 0 | 0 / 0 | 12 / 12 | OK |
| I. Daftar sumber, commit, dan hash | 101 / 101 | 49 / 49 | 5 / 5 | 505 / 505 | OK |
| Penutup — status audit (closing) | 10 / 10 | 0 / 0 | 0 / 0 | 1 / 1 | OK |

Totals (whole file): 0x-hex 149 occurrences / 67 distinct — match; URLs
18 / 12 distinct — match; numbers 1,919 occurrences (separators stripped) —
match; bare hex 22 / 9 distinct — match.

## Structure and formatting

- Headings: 62 in both files (1 × H1, 12 × H2, 49 × H3), identical level
  sequence and order. No heading added, removed, or reordered.
- Table rows (`|` lines): 85 in both files.
- Code fences: 2 in both files (one block, section H).
- Markdown links `[text](target)`: 0 in the English file — the report uses
  bare URLs and file paths only, so there are no relative links to resolve.
  All 18 URLs are identical to the source.
- Bold/backtick markers: no line has an odd count in either file (the two
  lines flagged by a naive backtick count are the ``` fence lines
  themselves, identical in both files).
- Line endings: LF-only in all three files; all end with a newline.

## Evidence classifications and certainty

Label occurrences (whole file):

| Label | ID | EN |
|---|---|---|
| verified fact | 26 | 26 |
| official claim | 8 | 8 |
| direct observation | 9 | 9 |
| reconstruction | 11 | 11 |
| inference | 5* | 6* |
| unknown | 22* | 23* |

\* See "Explained differences" — both are wording artifacts of the same
lines, not added claims. No inference was upgraded to a verified fact and no
certainty level was changed anywhere.

Critical warnings preserved at full strength (English file): "UNRESOLVED"
3×, "never call it rounding" 1×, "STILL STANDS" 2×, "Never write '7
auditors received keys'" 1×, "needs team context via ticket" 2×.
Contradictions between sources, research limits, open questions, and
repetitive passages are all present in the translation — nothing was removed
as repetitive.

## Explained differences

1. **"inference" 5 → 6 (line 89).** The Indonesian line reads "**koreksi
   terhadap inferensi yang salah:** …" — the word "inferensi" is the same
   term; a raw count of the English word "inference" in the Indonesian file
   naturally finds 0 on that line. The translation is correct, not an
   added label.
2. **"unknown" 22 → 23 (line 87).** The Indonesian table row already
   contains the English phrase "**provenance unknown**"; the English text
   additionally renders "asal/tujuannya tidak diketahui" as "its
   origin/purpose is unknown". Correct translation of the same cell.
3. **shield / shielding / unshielding (lines 193, 291, 366).** Line 193:
   Indonesian "shield/unshield bersifat publik" → "shielding/unshielding
   are public" (abbreviated source terms expanded to their full forms).
   Lines 291, 366: Indonesian "unshielding" used as a count noun → English
   plural "unshieldings". Word-boundary counts: "shielded" 26 = 26;
   "shielding" 24 → 25 and "unshielding" 24 → 23 are fully explained by
   these three lines. No term was dropped or invented.
4. **Number formatting.** Indonesian thousand separator "." → English ","
   (e.g. `7.295.799` → `7,295,799`); Indonesian decimal comma → English "."
   (e.g. `0,0001` → `0.0001`, `752,58` → `752.58`, `196,6795808` →
   `196.6795808`). Values are identical after separator normalization.
5. **Units/time.** "dtk" → "s" (`~2,2 dtk` → `~2.2 s`), "1×/jam" →
   "1×/hour". "tutup Minggu 22 November 2026" → "closes Sunday 22 November
   2026" — verified with `date -d 2026-11-22`: it is indeed a Sunday.

## Terminology decisions

Terms kept in their original form (no translation attempted): contract and
event names (`AuditorAdded`, `AuditorKeyGiven`, `Commitment`,
`EncryptedNote`, `Nullifier`, `PartialWithdrawal`, `PaidOut`,
`SharedVault`), file and repo names (`enygma_payments`,
`enygma_retail_payments`, `auditor.go`, `UserRegistry.sol`, `mlKemAuditCt`,
`aesAuditCt`, `CiphertextHash.sol`), English source quotes from Rayls
docs/blog (kept verbatim), and the six evidence labels (already English in
the source). Fixed renderings used consistently: "selisih fee" → "the fee
discrepancy"; "perlu konteks tim via ticket" → "needs team context via
ticket"; "TETAP BERLAKU" → "STILL STANDS"; "temuan yang tampak janggal" →
"findings that look odd" (deliberately plain, not strengthened to
"suspicious"); "di-build ulang" → "was rebuilt".

## Unresolved items

None for content. The only open item is the decision itself: promoting
`.en.md` to the main version (`ENYGMA-TESTNET-AUDIT-REPORT.md`) awaits
Anara's approval. Until then the Indonesian original stays the main file
and `.id.md` stays as its backup.

## Recommendation

**The translation is fit to be promoted to the main version.** Every
section is fully represented (617/617 lines), every hash, URL, address, and
number matches the original, the structure is identical, classifications
and certainty levels are unchanged, and no Indonesian text remains. The
only change a promotion requires is replacing the main file's contents with
`.en.md` and removing the temporary `.id.md` backup (the original remains
recoverable from `~/workspace/rayls-enygma-audit/`).

## Promotion (22 Nov 2026 ~23:52 WIB)

Anara approved the recommendation above. The English translation was
promoted to the main version: `ENYGMA-TESTNET-AUDIT-REPORT.md` now holds the
English text (SHA-256
`13622c8faf80ab4c70077d8976b7d8893b34ebebe41f06f9174e3dd98ce76b10`, verified
byte-identical to the checked `.en.md` file with `cmp`, after which
`.en.md` was removed as a duplicate). The Indonesian original is preserved
as `ENYGMA-TESTNET-AUDIT-REPORT.id.md` (SHA-256
`1d2ab730a6df4abc99af830ac1ef4e3a7d8845b3b78ee51c9a7dcda51c50c711`,
unchanged). The verification record above describes the state at check
time and is left intact.
