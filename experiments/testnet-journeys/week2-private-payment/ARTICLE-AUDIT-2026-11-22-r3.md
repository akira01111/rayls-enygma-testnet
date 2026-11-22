> **Translator's note (public version):** This document is a faithful English translation of the frozen Indonesian source (SHA-256 `6a1be437ce51227286f23861615781c01d8e394c5a3b07ea34262ba785c6638f`), prepared for the public repository. It is a translation only — not a revision, update, or new version. All findings, numbers, hashes, addresses, URLs, tables, evidence classifications, limitations, and conclusions are unchanged from the frozen source. The Indonesian source is retained privately in the project archive and is not included in this repository.

# Targeted audit — "What Can the Public Actually See When Two Accounts Make a Private Transfer on Rayls Enygma?"

**Audit date:** 22 Nov 2026, ~13:24–14:10 WIB
**Scope:** the two-account experiment of 21 Nov 2026 carried out
with the @anara account (sender, according to the app) and @kittynim
(receiver, according to the app), 6 RLS (according to the app) + the
experiment video + the TX `0x09edab2b…` evidence package ONLY.
Attributing the on-chain transaction to the two accounts is a
**reconstruction** (app evidence + registry + transaction match) —
not an on-chain fact, because there is no user address inside the
transaction (see correction 1, §6 F15).
**Out of scope:** the overall Rayls audit; the 511-transaction network
inventory; new experiments; new on-chain transactions.
**Method:** the video was watched in full (final 185.5 sec + raw
footage 241.7 sec, local VO transcription + 24 frames read); all
numbers/addresses were re-derived from the raw files (not from
earlier reports); old reports were used only as a comparison, and
every deviation was recorded.
**Status:** audit report + list of candidate commit files. NOT yet
committed, NOT yet pushed. Awaiting Anara's review.

**Revision r3 (22 Nov 2026, ~14:00 WIB):** this file revises
`ARTICLE-AUDIT-2026-11-22-r2.md` (kept as a record) based on Anara's
review of r2 — four corrections:
(1) the §4.1 row and every mention of 4.416 are split into three
layers: the raw integer in the statement, the RLS-unit interpretation,
and the "total fee" interpretation;
(2) claim 4 in §7.5 uses "user-level sender/receiver" to avoid
confusion with the relayer as the public transaction sender;
(3) the size and SHA-256 of r2 were matched to the canonical file
(48,097 bytes, SHA `00e464f2…`) — the figure of 47,530 bytes in §8.5
of r2 was an intermediate measurement taken before §8.4 was restored
(see §8.5);
(4) the exact list of files proposed for the commit was added
(§8.6), together with the full `git status --short` output.

## 1. Video ↔ transaction matching

### 1.1 Activity sequence (final video, verified against the raw footage)

The account labels (@anara / @kittynim) and balance figures in this
table are the **app display** (direct observation). The link between
these activities and the on-chain transaction `0x09edab2b…` is a
**reconstruction** (correction 1): the app shows the same tx in both
accounts' Activity, the registry maps both usernames to addresses,
and the time/block match — but no on-chain field states "this tx is
the payment from @anara to @kittynim".

| # | Video time | Activity | Screen evidence | Matches on-chain |
|---|---|---|---|---|
| 1 | ~0–15 sec | @anara account: $RLS Public 260.1335 / Shielded 14.324 / Total 274.4576; $USDr 0.01 / 4.9775 / 4.9875 | frame f_001 + raw_001 | Balances are the app display (not direct on-chain data) — see 1.3 |
| 2 | ~15–30 sec | @kittynim account: $RLS Public 17.8252 / Shielded 321.4 / Total 339.2252; $USDr 5 / 7 / 12 | frame f_002 + raw_003 | Same — app display |
| 3 | ~30–45 sec | Send $RLS page, Shielded, To @kittynim (0x680D…8eFC), "can receive shielded payments", Shielded: 14.324, Amount 0.00 | frame f_003 + raw_005 | Username→address matches the registry (see 2.3) |
| 4 | ~45–60 sec | Amount 6 $RLS; Fees 4.42 $RLS ("3.84 gas + 0.58 Rayls Foundation (15%)") | frame f_004 | 4.42 = 3.84 + 0.58 (wallet display; see §3) |
| 5 | ~60–75 sec | Passkey confirm → "Approve" ✓ → "Pick your notes and encrypt" ✓ → "Make the zero-knowledge proof" (loading proving key, 4.8 sec) | frame f_005 + raw_006 (passkey prompt) + raw_007 (ZK tooltip) | The passkey prompt + tooltip are only in the raw footage, not in the final |
| 6 | ~75–90 sec | Success: "Sent 6 $RLS to @kittynim, privately", proof 256 bytes, "Made in 10 s, in this tab", fee 4.42 $RLS, tx 0x09edab2b…eff525bb | frame f_006 + raw_008 | Tx matches fully (see §2) |
| 7 | ~90–105 sec | @anara: Shielded 14.324 → 3.908; Total 264.0416; $USDr unchanged | frame f_007 | Difference 10.416 = 6 + 4.416 (arithmetic from the displayed balances) |
| 8 | ~105–120 sec | @kittynim Activity: "Received +6 $RLS, 21 Nov 2026, 16:40", tx 0x09edab2b…; panel "What the explorer shows" | frame f_008 + raw_011 (full panel) | Tx + time match (see 2.1); the panel contains 2 discrepancies (see §4.4, §4.5) |
| 9 | ~120–135 sec | Explorer: Success, transferV2, Block 24825928, 175 confirmations, "Nov 21 2026 16:40:42 (+07:00 UTC)", From 0xa5f0C684…, SharedVault | frame f_009 + f_011 | Matches the raw data fully (see 2.1) |
| 10 | ~135–150 sec | Activity @kittynim: +6 RLS (16:40), +250 RLS Shielded (16:31), +2 USDr (13 Nov) | frame f_010 + raw_010 | +6 matches; +250 and +2 are SEPARATE activities (see 1.2) |
| 11 | ~150–185 sec | Closing narration: the tx is not invisible; what is recorded is the event, the block, and the relayer; not an ordinary public transfer | frame f_011 + f_012 + transcript 147–184 sec | Narration claims assessed in §4 |

### 1.2 What must NOT be mixed into the 6 RLS payment story

- **Shielded +250 $RLS, 21 Nov 2026, 16:31, tx `0xa917fdcc…4104bd38`.**
  @kittynim's own activity (shielding), 9 minutes BEFORE the transfer.
  The "before" balance 321.4 ALREADY includes this +250 (321.4 + 6 = 327.4 exactly).
  Not part of the payment; not verified on-chain in this audit.
- **Received +2 $USDr, 13 Nov 2026, 09:20, tx `0x2be744ca…8b6e1fc9`.**
  Activity from 8 days earlier. Not part of the payment.
- The final video does not explicitly distinguish the three (all appear
  in the Activity list). The article must mention the +250/+2 as other
  activities on the same account, not as part of the transfer.

### 1.3 What could not yet be matched / matching limits

- **The app balances (Public/Shielded/Total) are direct observation,
  not verified on-chain data (correction 3).** A shielded balance
  is the result of the app decrypting notes with the user's keys; no
  on-chain field states "shielded balance of @anara = 14.324" or
  "shielded balance of @kittynim = 321.4". What can be said: the app
  displays those balance changes, and the changes are arithmetically
  consistent with 6 + 4.416 (a consistency check on displayed values,
  not on-chain verification). Likewise, the "+6 $RLS" in the receiver's
  Activity is an app display (the app decrypts the note for that
  account), not an on-chain field.
- **The "16:40" time in the Activity is the browser's local time (WIB).**
  It matches the block timestamp 16:40:42 WIB (raw `block.json`).
  The raw-data fetch time (16:13–16:29 UTC) is a different UTC clock —
  do not mix them.
- **"175 confirmations" and "Confirmed within <= 0.545 secs"** are a
  snapshot of the explorer display at recording time, not stable facts.
- **"Made in 10 s"** is an app-display timer, not an independently
  measured duration.

### 1.4 Raw footage vs final video (was anything reordered?)

The substantive order is the SAME. What was cut from the final (only
in the footage):
(1) the Send page initially showing $USDr, then switched to $RLS (raw_002);
(2) the passkey prompt (raw_006); (3) the zero-knowledge proof
explanation tooltip (raw_007 — its text is quoted in §5.2);
(4) the @kittynim Receive page with QR + full address (raw_004);
(5) the "Page Not Responding" dialog (a brief browser freeze, raw_010);
(6) the explorer still loading at the end of the recording (raw_012) —
meaning the explorer segment in the final video was recorded in a
separate take (after the page had loaded), not at the same moment as
the activity recording. There was no reordering of the experiment
sequence; the cuts are editorial. The browser freeze and the separate
take are recorded as recording observations, not as experiment findings.

## 2. Audit of the JSON package and the transaction (re-derived from the raw data)

All values below were read directly from
`experiments/transactions/tx-09edab2b/raw/*.json` on 22 Nov 2026, not
from `TX-AUDIT-REPORT.md` or `decoded/*`.

### 2.1 Main transaction `0x09edab2b…`

| Field | Value (raw) | Matches video |
|---|---|---|
| hash | `0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb` | yes (f_006, f_009, f_011) |
| block | 24825928 (0x17ad048), timestamp 1795254042 = **2026-11-21 16:40:42 WIB** | yes, exactly (f_009: "16:40:42 (+07:00 UTC)") |
| from | `0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8` (relayer) | yes (f_009) — NOT @anara |
| to | `0x9c5ad5e5ea5b5910e7fd1e1cc7b70ce0e4bf06c2` (SharedVaultProxy) | yes ("SharedVault", f_009) |
| value | 0x0 (0) | yes ("Value 0", f_008/raw_011) |
| gas / gasPrice | gasLimit 1,630,484; gasPrice 48,000,000,000 wei (48 Gwei) | — (not in the video) |
| input | 4,804 bytes; selector `0xaacd552c` | "transferV2" (f_009/f_011) |
| receipt | status 0x1 (success); gasUsed 1,316,001; 7 logs; contractAddress null | "Success" (f_009) |
| block | contains only this 1 transaction (block gasUsed = 1,316,001; block gasLimit 500,000,000) | — |

### 2.2 Selector + calldata structure (fresh verification)

- `keccak256("transferV2((((uint256,uint256),(uint256[2],uint256[2]),(uint256,uint256)),uint256[],uint256,uint256),bytes[],bytes[])")`
  first 4 bytes = **`0xaacd552c`** — matching the selector in the calldata.
  (The canonical signature is taken from `decoded/bundle-abi-extract.json`,
  the client-side ABI from the demo bundle — see §5.)
- Proof: 8-word struct = **256 bytes** (calldata bytes 100–356) — matching
  the "256 bytes" display in the video.
- Statement: 10-word array (length 10, bytes 452–804):

| Position | Value | Status |
|---|---|---|
| [0] | 0 | not yet identified |
| [1] | 0 | not yet identified |
| [2] | `0x0d6edc87…` (hash) | not yet identified (a Merkle/binding reading = inference) |
| [3] | `0x0c0f23a6…` | **nullifier** — same as topic[3] of log[0] |
| [4] | `0x094b233a…` | **commitment 1** — same as topic[2] of log[1] |
| [5] | `0x2304db2e…` | **commitment 2** — same as topic[2] of log[2] |
| [6] | `0x206ed94a…` | **commitment 3** — same as topic[2] of log[3] |
| [7] | `0x9c5ad5e5…` (vault address) | verified |
| [8] | **4,416 × 10¹⁸** (integer) | verified (the integer's appearance); the RLS unit and the "total fee" meaning are interpretation (see §3.2) |
| [9] | `0x0f58ff41…` (hash) | not yet identified (a binding reading = inference) |

- Two other uint256s in the struct (byte 388 = **1**, byte 420 = **3**):
  consistent with "1 note in, 3 notes out" (1 nullifier + 3
  commitments), but that label is an **inference**, not a verified field
  name (no statement layout has been published).
- Ciphertext: from each EncryptedNote log, ciphertextI (1,088 bytes) and
  ciphertextII (92 bytes) **are present verbatim inside the calldata**
  (checked by substring + fresh SHA-256 for all three). The 1,312-byte
  log data is not a raw copy of the calldata — it is an ABI wrapper
  (offset + length) around the same two ciphertexts.

### 2.3 Event logs (7 logs, all from the vault proxy)

| Log | Event (topic0 verified by fresh keccak) | Contents |
|---|---|---|
| [0] | Nullifier `0x437885c0…` | vaultId=2, treeNumber=0, nullifier `0x0c0f23a6…` |
| [1–3] | Commitment `0x28ec6d3c…` (×3) | vaultId=2, commitment (same as statement[4–6]) |
| [4–6] | EncryptedNote `0x3703497a…` (×3) | vaultId=2, commitment, ciphertextI 1,088 B + ciphertextII 92 B |

The topic0 of all three events was verified fresh with keccak256 over
the signatures from the bundle ABI (Commitment, EncryptedNote,
Nullifier — all three match). An independent `eth_getLogs` also
returned the same 7 logs. There is no PaidOut / CoinLocked /
PartialWithdrawal event on this tx.

### 2.4 Registry username → address (fresh verification)

- Registry `0xA473291FFb33e2276F364fAE169f03c4406719e9`, 195 UsernameSet
  logs (chunks [28, 26, 9, 0, 25, 46, 33, 28, 0] = 195).
- `@anara`: 1 log, block 23353951, address topic
  `0x0c5b369ad7d0c4e051a2887575f7fc85e0ccd0b5` — matches the EVM in the video
  (0x0C5B…D0B5).
- `@kittynim`: 1 log, block 23575688, address topic
  `0x680d90983da58bcb7d127e3421193274e84e0efc` — matches the EVM in the video
  (0x680D…8eFC) and the full address on the Receive page in the footage (raw_004).
- **The identities @anara → 0x0c5b… and @kittynim → 0x680d… are on-chain
  facts from the registry** (not merely video claims). The link from
  the tx → @anara remains a reconstruction: there is no user address
  inside the tx (see §4.3).

### 2.5 Separate transaction from the same relayer `0xacc7d175…` (correction 5)

This transaction is written up as a **separate transaction**, not as
part of the main transaction. What is verified from the raw data:

- From `0xa5f0c684…` (the SAME address as the main tx sender),
  to `0x07e17e17…` (the RLS token), block 24825932 (4 blocks after the main
  tx), 09:40:45 UTC — **3 seconds after the main tx** (block timestamp
  difference; verified fact).
- Input `0xa9059cbb…` = ERC-20 `transfer(address,uint256)` with the
  address argument `0x71af09966cbed4434cca97c40fa38b8083548b95` and the amount
  **exactly 0.576 RLS** (576,000,000,000,000,000 wei, read from the input,
  not from a report). The address and amount as **call arguments**
  are verified fact; neither is a conclusion about who the recipient
  is or what the transfer is for.
- Receipt successful, gasUsed 41,806, 1 log (ERC-20 Transfer event).
- The relayer txlist (2 independent explorer calls) returned exactly
  2 txs in the block window: the main tx + this one. There is no other
  relayer tx in that window.

What is NOT concluded (without evidence):

- **Who `0x71af…` is.** The previous audit map calls it
  "Auditor EOA" — that is a reconstruction, not a proven on-chain link.
  Whether this address belongs to the Rayls Foundation, an auditor,
  or another party: **unknown**.
- **What this transfer is for.** The exact arithmetic match 3.84 × 15% = 0.576
  and the wallet display "15% Rayls Foundation fee" are
  **a consistent clue** for the suspicion that this transfer relates
  to the fee — but a numerical match is not proof of purpose.
  Purpose of the payment: **unknown**. The article must not write
  this transfer as a "fee payment to the Foundation" or a "fee
  settlement" as a fact; the correct wording is: "a separate transaction
  from the same relayer, three seconds later, calling transfer() with
  the arguments (0x71af…, 0.576 RLS)".

### 2.6 What is NOT in the tx (checked fresh)

- The addresses `0x0c5b…` (@anara) and `0x680d…` (@kittynim): **absent** from
  the calldata, from every log's data, and from every topic.
- The value 6 RLS (6 × 10¹⁸ as a 32-byte word): **absent** from the calldata.
- The words "anara" / "kittynim": absent from the tx.

## 3. Fee audit

### 3.1 Three components — separated

| Component | Value | Source | Classification |
|---|---|---|---|
| Chain gas | 1,316,001 gas × 48 Gwei = **0.063168048 native gas units** | receipt + tx (raw) | **Verified fact** for the number; **Unknown** for the token name (see 3.3) |
| Integer 4,416 × 10¹⁸ in statement[8] | **4,416 × 10¹⁸** as a word in statement[8] | calldata (raw) | **Verified fact** — only the integer's appearance; the RLS unit = **interpretation** (app display + the token's 18 decimals); the "total fee" meaning = **inference** (see §3.2) |
| Interpretation "4.416 = total fee" | the number in statement[8] IS the payment's total fee | app display + arithmetic (see §3.2) | **Inference** (strong, corroborated — not an on-chain fact) |
| Separate 0.576 RLS transaction | transfer() with the arguments (`0x71af…`, 0.576 RLS), a separate tx from the same relayer, 3 seconds later | related-tx input + receipt (raw) | **Verified fact** — arguments + timing; the recipient (who) and purpose: **Unknown** (see §2.5) |
| Arithmetic remainder | **3.84 RLS** = 4.416 − 0.576 | arithmetic | **Reconstruction** (never appears as a word of its own in the on-chain data) |
| Wallet display | "3.84 gas + 0.58 Rayls Foundation (15%)" = 4.42 | Video UI (f_004/f_006) | **Direct observation** (UI claim) |
| 15% | 3.84 × 15% = 0.576 (exactly) | arithmetic | **Verified fact** (the calculation); that 15% is the Foundation rate = **Official claim** (UI + docs); that the 0.576 RLS transfer is the payment of that rate = **Unknown** |

### 3.2 The 4.416 = 3.84 + 0.576 pattern — facts and interpretation separated (correction 2)

**Fact (verified fact):** the integer 4,416 × 10¹⁸ appears as a word
in statement[8] of the calldata; the integer 0.576 × 10¹⁸ appears as
the amount argument in the separate transaction `0xacc7d175…`; the
difference between the two is 3.84 × 10¹⁸. **Three layers that must
be distinguished:** (a) the raw integer — fact; (b) the RLS unit —
**interpretation**, and its source differs per term: the RLS unit for
0.576 is anchored by the RLS token contract (`transfer()` was called
on the RLS token contract `0x07e17e17…`, so the amount is expressed in
that token's units), whereas the RLS unit for 4.416 comes from the app
display (the wallet + detailed activity state the fee in RLS) — the
calldata carries no unit label; 3.84 inherits its unit from the app
display; (c) the "total fee" meaning — **inference** (see below). The
equation 4.416 = 3.84 + 0.576 closes on the numbers; the RLS label on
each term comes from different sources and must not be read as one and
the same on-chain fact.

**Interpretation (inference, corroborated but not an on-chain fact):**
that the word in statement[8] is the "total fee", that 3.84 is the
fee portion retained by the relayer, and that 0.576 is the portion
forwarded as the Foundation fee. Corroboration for this interpretation:
(i) the wallet display shows a total fee of 4.42 (3.84 + 0.58) and
the detailed-activity explanation shows 4.416 as the fee according to
the app; (ii) the balance arithmetic closes: 6 + 4.416 = 10.416 equals
the displayed shielded-balance decrease; (iii) 3.84 × 15% = 0.576 exactly.

**Verification limit of this interpretation:** no statement layout has
been published and there is no verified source for the vault contract —
so the semantic meaning of the statement[8] word cannot be proven from
a verified on-chain schema; it is established through value matching +
the app display + the client-side ABI from the demo bundle (reference
code, not a verified source). In other words: **the integer 4,416 × 10¹⁸
in statement[8] is a fact; the RLS label for that integer and the
"total fee" meaning are a strong interpretation but still an
interpretation.** The article must write the three separately: "the integer
4,416 × 10¹⁸ appears in the transaction's statement; the app presents
it as 4.416 RLS and as the total fee" — not "the on-chain fee is
4.416 RLS" without qualification.

- The integer 4,416 × 10¹⁸ (statement) and 0.576 RLS (ERC-20 transfer
  on the RLS token contract) were both independently verified from the
  raw data — with the note that the RLS unit for each comes from a
  different source (see above).
- 3.84 appears only as a difference. Its exact nature (relayer service
  fee vs gas reimbursement) is **unknown** — the wallet calls it "gas",
  the earlier TX report calls it "relayer service fee, not chain gas"
  (TX-AUDIT-REPORT.md:206), but no on-chain word proves either one.
- Note: 3.84 RLS ≠ chain gas 0.063168048. The two differ by ~60×.
  The article must keep the two separate.

### 3.3 NEW FINDING — gas token: RLS or USDr? (unanswered)

Two official app texts contradict each other:

- **For RLS:** the wallet asset list labels it "$RLS — Pays gas"
  (direct observation, f_001); the Rayls pilot blog (12 Nov, cited in
  the initial audit:193) states "all fees in $RLS" (official claim);
  a contract named `RlsGasForwarder` (0x753cc3…); the TX report
  labels the chain gas "0.063168048 RLS".
- **For USDr:** the "What the explorer shows" panel states the relayer
  "pays the gas in $USDr" and "Value counts only the chain's own coin,
  $USDr" (raw_011). The USDr token address `0x0000…0400` is a
  precompile-style address (0x400), consistent with a protocol-level
  token — but that is not proof of the gas token's name.

The raw tx cannot settle this: gasPrice/gasUsed are stated in native
units with no token name. **The label "0.063168048 RLS" in
TX-AUDIT-REPORT.md:144 is an assumption (written as "(18 decimals assumed)"
for the decimals, but the token identity was never checked).**
For the article, the safe wording is: "chain gas 1,316,001 × 48 Gwei =
0.063168048 native gas units" + a note that the app's own texts
disagree about the token. Do not state RLS or USDr as an established
fact. (Ticket-question candidate — see §7.4.)

## 4. Public-data visibility audit

### 4.1 What an ordinary public observer can see (from the tx + explorer)

| Data | Publicly visible? | Evidence |
|---|---|---|
| That a transfer happened | yes | successful tx, transferV2 method |
| Block + time | yes | block 24825928, 16:40:42 WIB |
| Sending relayer | yes | from `0xa5f0c684…` |
| Contract called | yes | SharedVaultProxy `0x9c5ad5e5…` |
| Value field | yes — **0** | tx value 0x0 |
| Gas used + gas price | yes | 1,316,001 × 48 Gwei |
| 1 nullifier (hash) | yes | log[0] topic[3] `0x0c0f23a6…` |
| 3 commitments (hashes) | yes | log[1–3] topic[2] |
| 3 encrypted notes / ciphertexts | yes (as bytes) | log[4–6] data; same bytes as in the calldata |
| Integer 4,416 × 10¹⁸ in statement[8] | yes — as a calldata word | statement[8] (raw). The RLS unit for this integer is interpretation (app display), and its meaning as "total fee" is inference (see §3.2) — neither is an on-chain fact |
| Separate 0.576 RLS transaction | yes — as a transfer() call | tx `0xacc7d175…` (public ERC-20 transfer); transfer purpose: unknown (see §2.5) |
| Address argument `0x71af…` in that transfer | yes — as a call argument | ERC-20 transfer input; who owns that address: unknown |

### 4.2 What an ordinary public observer CANNOT read from this tx

| Data | Status |
|---|---|
| Payment amount (6 RLS) | absent as plaintext in the tx (checked fresh, §2.6) |
| Who the sender is (@anara) | address absent from the tx (checked fresh, §2.6) |
| Who the receiver is (@kittynim) | address absent from the tx (checked fresh, §2.6) |
| Which token (RLS) | no token marker in the main tx (the token is only known from the app context + balances) |
| Value of each note / mapping of the 3 notes → (payment / change / fee) | reconstruction from the balances, not an on-chain fact |
| Ciphertext contents (amounts, note owners) | encrypted; cannot be read without keys |

### 4.3 Key holders / auditor — what is different

- **Key holders (sender/receiver):** can decrypt their own notes
  and see their shielded balance in the app. That is why the receiver's
  Activity shows "+6 $RLS" for the same tx — the receiver's app
  decrypts the note for that account. This capability is a design
  claim (docs + UI), not something proven by the tx.
- **Auditor:** the app panel claims "Auditor sees it" for the
  sender, receiver, and amount. **This claim is not verified
  on-chain in this audit.** What is verified: there is an auditor
  role in the registry (7 AuditorAdded, 4 AuditorKeyGiven — from the
  initial audit), and the separate transaction `0xacc7d175…` calls
  transfer() with the address argument `0x71af…` (called "Auditor EOA"
  in the audit map — the link between that address and the auditor role
  is a reconstruction, not a proven on-chain link). The article must
  present "the auditor can see it" as an app claim, not as a
  verified fact.
- **Authorities:** there is no evidence in this package about authority
  access. Do not conclude anything in that direction.
- The principle used here (per the instructions): do not conclude
  "impossible to know" merely because something does not appear as
  plaintext. The ciphertext is on the chain; whether someone can
  decrypt it depends on the keys — and that is beyond the evidence
  in this package.

### 4.4 NEW FINDING — relayer address in the panel ≠ on-chain relayer address

The "What the explorer shows" panel (raw_011, also f_008) writes:
"From — The relayer, @rayls-relayer **0x25f8…8ac5**, not you."
But the on-chain tx sender is **`0xa5f0c684…`**, and that same address
is recorded as the relayer in `contracts/addresses/addresses.json`
(`other_addresses[1]`) and in the explorer txlist endpoint.
Searching for `25f8` across the whole repo does not find that address
in any file (the only matches are hex fragments inside ciphertext
blobs — false positives). The full `0x25f8…` address is not visible
in the video (shown truncated), so it cannot be searched further from
this evidence. **Possibilities:** (a) the panel shows a relayer service
address different from the tx-signing address; (b) a stale/cached
address; (c) the panel is wrong. Nothing can be decided from this
evidence. **The article must use the on-chain address `0xa5f0c684…` and
mention this discrepancy as an open question** (ticket candidate — see
§7.4). Do not quote `0x25f8…` as the relayer.

### 4.5 NEW FINDING — "Hidden" in the panel does not mean "not on the chain"

The panel marks "Amount: 3 commitments: 0x094b233a…, 0x2304db2e…,
0x206ed94a…" as **Hidden / Auditor sees it** — yet those three
commitment values ARE public topics in log[1–3] (verified fresh,
§2.3). That means: "Hidden" in the panel's language means "cannot be
interpreted as amounts by an ordinary observer", NOT "absent from the
blockchain". The article must write this precisely: the commitments
and ciphertexts **exist and are public as bytes**; what is hidden is
**what they mean** (the amounts, the owners). Do not write "the
commitments are not visible" or "the notes are not on the chain".

### 4.6 Notes on the video narration claims

- "The public transaction sender is the relayer, not @anara" — **true**
  (from = relayer).
- "The value field shows 0" — **true** (value 0x0). (The Whisper
  transcript writes "0 U.S.D.R." — that is a transcription artifact,
  not a video error; the subtitle in frame f_008 writes "Value — 0,
  the value field is empty".)
- "The explorer shows commitments and encrypted notes, rather than a
  conventional public transfer" — **true** (logs + calldata).
- "The transaction itself isn't invisible. The blockchain still records
  that it happened, which block included it, and which relayer submitted
  it." — **true, and it is the right thesis for the article**.
- "The receiver can confirm the payment, while the public transaction
  record shows a different picture" — **true** (receiver's Activity
  vs the explorer display).

## 5. Documentation and implementation

### 5.1 Three layers that must be distinguished

| Layer | Example | Status for this tx |
|---|---|---|
| **Official claims** (docs, blog, app UI) | docs.rayls.com: a shielded send only shows the event, the relayer, the gas fee; relayer fee 15% to the Foundation; pilot blog: "all fees in $RLS"; UI: "Quantum-private", "Auditor sees it", explorer panel | Cited as claims, not as on-chain evidence |
| **Reference code** (client-side demo bundle) | `bundle-abi-extract.json` (IEnygmaDvp, bundle SHA `7530bbc2…`, taken 21 Nov 16:17 UTC); event signatures + transferV2 | Selector/topic match on-chain (fresh verification §2.2–2.3); the contract's internal logic is NOT proven by the bundle |
| **Deployed implementation** | SharedVaultProxy `0x9c5ad5e5…`, implementation from the EIP-1967 slot `0xAd966704…` (read fresh from `contracts.json`), yx registry `0xA473291F…` | Address + bytecode + slot verified; **no verified source** for the vault implementation (from the initial audit, not re-verified in this round — see 5.3) |

### 5.2 Relevant app text (direct observation from the footage)

- ZK proof tooltip (raw_007): "A zero-knowledge proof shows something
  is true without showing why. Here it shows the vault that you may
  spend these notes and that nothing is created, without saying which
  notes, whose they are, or how much. This tab computes it from your
  keys and notes. Onchain go the proof, the new notes, encrypted, and
  a nullifier per note spent." — Official claim (UI copy). Consistent
  with what was observed on-chain (1 proof of 256 bytes, 3 new encrypted
  notes, 1 nullifier) — but "shows the vault that you may spend" is a
  statement about the proof, not something that can be checked from the tx.
- The Public/Hidden/Auditor rows on the Send page (f_003/f_004): "That
  payment happened" (Public) / "Who paid whom, and how much —
  Quantum-private" (Hidden) / "@anara paid @kittynim 6 $RLS" (Auditor).
  These are **UI labels**, not on-chain classifications.

### 5.3 Limitations carried over from the previous audit (not re-verified)

- No verified source for the vault implementation `0xAd966704…`
  (initial audit; `contracts/verified-source/README.md`). This round did
  not re-check the explorer verification status (outside the article's
  scope; requires a separate live check).
- bx vs yx implementations: this tx uses the active yx deployment
  (vault proxy `0x9c5ad5e5…`); the bx mismatch is not relevant
  to this article.
- 4byte.directory has no entry for this selector/event (from the
  previous audit) — resolution relies on the bundle ABI + local keccak
  (verified fresh in this round).

## 6. Classification of findings

| # | Finding | Label | Source + reason |
|---|---|---|---|
| F1 | Successful tx, transferV2, block 24825928, 16:40:42 WIB | Verified fact | `transaction.json` + `receipt.json` + `block.json` + explorer frame |
| F2 | Public sender = relayer `0xa5f0c684…`, not @anara | Verified fact | tx `from` (raw) + explorer frame |
| F3 | Value field = 0 | Verified fact | tx `value` 0x0 (raw) |
| F4 | 1 nullifier + 3 commitments + 3 encrypted notes | Verified fact | receipt 7 logs + fresh topic0 keccak |
| F5 | Log ciphertexts = bytes in the calldata | Verified fact | substring + fresh SHA-256 (§2.2) |
| F6a | Integer 4,416 × 10¹⁸ appears in statement[8] | Verified fact | word in the calldata (raw) — only the integer's appearance; the RLS unit = interpretation (app display); the "total fee" meaning = inference (F6b) |
| F6b | That number IS the payment's total fee | Inference | app display + balance arithmetic + 3.84 × 15% = 0.576; the word's semantic meaning is not proven by a verified on-chain schema (§3.2) |
| F7 | Separate transaction from the same relayer, 3 seconds later, calling transfer() with the arguments (`0x71af…`, 0.576 RLS) | Verified fact (arguments + timing) | related-tx input + receipt + block timestamp (raw); who `0x71af…` is and what the transfer is for: Unknown (F31, F32) |
| F8 | 3.84 = 4.416 − 0.576 | Reconstruction | arithmetic on the numbers; no on-chain word of its own; the RLS unit of each term comes from a different source (see §3.2) |
| F9 | 3.84 is "gas" / the relayer service fee | Unknown | the wallet calls it "gas"; its exact nature is not proven on-chain |
| F10 | Chain gas 0.063168048 native units | Verified fact (number) | gasUsed × gasPrice (raw) |
| F11 | Chain gas = 0.063168048 **RLS** | Unknown | TX report label; app texts contradict each other (§3.3) |
| F12 | The 6 RLS amount is absent from the tx as plaintext | Verified fact | fresh search in calldata/logs/topics (§2.6) |
| F13 | @anara/@kittynim addresses absent from the tx | Verified fact | fresh search (§2.6) |
| F14 | @anara = `0x0c5b…`, @kittynim = `0x680d…` | Verified fact | registry UsernameSet (raw), decoded fresh |
| F15 | Tx `0x09edab2b…` is a payment from @anara → @kittynim of 6 RLS | Reconstruction | three pillars: (1) the app shows the same tx in both accounts' Activity; (2) the registry maps @anara → `0x0c5b…` and @kittynim → `0x680d…`; (3) time/block match. NOT an on-chain fact: no user address or amount is inside the tx (F12, F13) |
| F16 | 3 outgoing notes = (6 payment / 3.908 change / 4.416 [statement[8] value]) | Reconstruction | balances + note count; not an on-chain fact; the RLS unit and the "fee" meaning for 4.416 are interpretation (see §3.2) |
| F17 | Statement[3–8] = nullifier, 3 commitments, vault address, fee | Verified fact | fresh value matching (§2.2) |
| F18 | Statement[0,1,2,9] = (0, 0, hash, hash) | Verified fact (its values); Unknown (their meaning) | values read fresh; no published layout |
| F19 | Struct (1, 3) = 1 incoming note, 3 outgoing notes | Inference | consistent with 1 nullifier + 3 commitments; the label is not verified |
| F20 | Proof is 256 bytes | Verified fact | calldata structure: the proof is a static 8-word tuple (bytes 100–356) according to the bundle ABI schema; the UI display "256 bytes" corroborates. Note: identifying it as the "proof" depends on the client-side ABI schema (reference code, not verified source) |
| F21 | Proof generated in 10 seconds in the browser | Direct observation | ONLY the app's timer display ("Made in 10 s, in this tab"). Not an independently measured duration; this audit did not measure proving time with any instrument |
| F22 | Shielded balances 14.324 → 3.908 and 321.4 → 327.4 | Direct observation | app display (video); arithmetically consistent with 6 + 4.416 — but NOT verified on-chain data; no on-chain field states a shielded balance |
| F23 | Relayer panel `0x25f8…8ac5` ≠ on-chain relayer `0xa5f0c684…` | Verified fact (the discrepancy); Unknown (its cause) | panel video vs raw tx; `0x25f8` is not in the repo |
| F24 | "Auditor sees it" (sender/receiver/amount) | Official claim | app UI copy; not verified on-chain |
| F25 | Commitments "Hidden" in the panel despite being public topics | Verified fact (the discrepancy) | panel vs raw logs (§4.5) |
| F26 | "All fees in $RLS" (pilot blog) | Official claim | cited in the initial audit:193 |
| F27 | Panel: relayer "pays the gas in $USDr" | Official claim | UI copy (raw_011); contradicts F26 |
| F28 | No verified source for the vault implementation | Official claim (carried) | initial audit; not re-verified this round |
| F29 | +250 RLS (16:31) and +2 USDr (13 Nov) are not part of the payment | Verified fact | video Activity list; +250 already included in the "before" balance |
| F30 | Block 24825928 contains only this tx | Verified fact | `block.json` (1 transaction) |
| F31 | The match 3.84 × 15% = 0.576 indicates the transfer `0xacc7d175…` relates to the fee | Inference | exact numerical match + wallet display "15%"; a numerical match is not proof of the transfer's purpose |
| F32 | `0x71af…` is the Rayls Foundation / Auditor fee address | Unknown | no on-chain link; the "Auditor EOA" label in the audit map is a reconstruction |

## 7. Audit findings report

### 7.1 Findings that are already strong (usable in the article — with classification)

- The transaction happened and is recorded publicly: a successful
  transferV2, block 24825928, 16:40:42 WIB, public sender relayer
  `0xa5f0c684…`, vault `0x9c5ad5e5…`, value 0. (**Verified fact.**)
- What is publicly visible: 1 nullifier, 3 commitments, 3 encrypted
  notes, and the integer 4,416 × 10¹⁸ in statement[8]. (**Verified fact**
  for the integer's appearance; the RLS label and the "total fee"
  meaning are **inference** — see §3.2.)
- What cannot be read publicly from the tx: the 6 RLS amount, the
  sender, the receiver, the token — none of them appear as plaintext
  (checked fresh). (**Verified fact** — the result of searching the
  calldata/logs/topics.)
- The link between this tx and the @anara → @kittynim payment of 6 RLS
  is a **reconstruction** (app + registry + tx match), not an on-chain
  fact (correction 1).
- The app shows "+6 $RLS" in the receiver's Activity for the same tx,
  and the displayed shielded balances move 321.4 → 327.4 (receiver) and
  14.324 → 3.908 (sender); the difference 10.416 = 6 + 4.416
  arithmetically. (**Direct observation** from the app, not verified
  on-chain data — correction 3.)
- The proof is 256 bytes according to the calldata structure; the app
  reports a 10-second generation time. (**Verified fact** for the size,
  from the calldata; **direct observation** for the time — correction 4.)
- The username→address identities are verified from the on-chain
  registry (@anara → `0x0c5b…`, @kittynim → `0x680d…`). (**Verified fact.**)
- A separate transaction from the same relayer, three seconds later,
  calls transfer() with the arguments (`0x71af…`, 0.576 RLS).
  (**Verified fact** for the arguments + timing; who `0x71af…` is and
  what the transfer is for: **unknown** — correction 5.)
- Rayls' own docs description (a shielded send shows the event, the
  relayer, and the gas fee) matches what was observed. (**Official claim**
  consistent with the evidence.)

### 7.2 Findings that need correction (before use in the article)

- **K1. Relayer address:** do not quote `0x25f8…8ac5` from the panel as
  the relayer. The on-chain address is `0xa5f0c684…`. The panel
  discrepancy must be mentioned as an open question, not ignored.
- **K2. Chain gas unit:** do not write "chain gas 0.063168048 RLS"
  as a fact. Write "1,316,001 gas × 48 Gwei = 0.063168048 native gas
  units" and note that the app texts disagree (RLS vs USDr).
  The RLS label in TX-AUDIT-REPORT.md:144 is an assumption whose token
  identity was never checked.
- **K3. "Hidden" ≠ "not on the chain":** do not write that the
  commitments/encrypted notes are "not visible" or "invisible". Write:
  their bytes are public; what cannot be read is their meaning (the
  amounts, the owners).
- **K4. Mapping of the 3 notes:** do not assert "note 1 = the 6 RLS
  payment, note 2 = the 3.908 change, note 3 = the 4.416 fee" as fact.
  That is a reconstruction. Write it as "consistent with" or do not
  map them.
- **K5. "3.84 gas":** do not write 3.84 as chain gas or as an
  on-chain-verified fee. Write: the arithmetic difference
  4.416 − 0.576; the wallet calls it "gas"; its exact nature is not
  yet known.
- **K6. "Auditor sees it":** present it as an app claim, not as a
  verified capability. Do not write that the auditor "can see it" as
  a fact of this audit.
- **K7. Other activities:** do not present the +250 RLS (16:31) or the
  +2 USDr (13 Nov) as part of the 6 RLS payment.
- **K8. @anara → @kittynim attribution (correction 1):** do not write
  "this on-chain transaction is the payment from @anara to @kittynim"
  as a fact. Write: transaction `0x09edab2b…` is recorded on-chain;
  its link to the two accounts is a reconstruction from the app
  evidence + registry + transaction match.
- **K9. The 0.576 RLS transfer (correction 5):** do not write "0.576 RLS
  was sent to the Auditor/Foundation as a fee" as a fact. Write: a
  separate transaction from the same relayer, three seconds later,
  calls transfer() with the arguments (`0x71af…`, 0.576 RLS);
  who `0x71af…` is and what the transfer is for are not yet known.
  The match 3.84 × 15% = 0.576 may be mentioned as an arithmetic clue,
  not as proof of purpose.

### 7.3 Evidence that is not yet sufficient

- The gas token's identity (RLS vs USDr) — the app texts contradict
  each other; the tx gives no token name.
- The meaning of statement[0,1,2,9] and the struct fields (1, 3) — no
  layout has been published.
- Whether `0x71af…` is the Rayls Foundation fee address — no on-chain
  link; only the audit map calls it "Auditor EOA".
- The purpose of the separate transfer `0xacc7d175…` (0.576 RLS with
  the address argument `0x71af…`) — the match 3.84 × 15% = 0.576 is
  only an arithmetic clue, not proof of purpose.
- The semantic meaning of the statement[8] word as "total fee" — the
  integer is verified, its interpretation is inference (see §3.2).
- The RLS unit for the statement[8] integer — it comes from the app
  display, not from the calldata; the calldata carries no unit label.
- The nature of the 3.84 component (service fee vs gas reimbursement).
- The auditor's actual capability (decryption/identification) — only
  a UI claim.
- Re-verification of the "no verified source" status of the vault
  implementation (carried over from the initial audit; not re-verified
  here).

### 7.4 Unanswered questions (ticket / article candidates)

Two open questions retained (per the review):

- **Q-A:** Why does the "What the explorer shows" panel name the
  relayer `0x25f8…8ac5`, while the tx sender is `0xa5f0c684…`?
  Are there two relayer addresses, or does the panel show a different
  address?
- **Q-B:** Which token pays the chain gas — RLS or USDr?
  The wallet + pilot blog say RLS; the explorer panel says USDr.

Other questions still open:

- **Q-C:** What do statement[0,1,2,9] and the struct fields (1, 3) mean?
- **Q-D:** Is `0x71af09966cbed4434cca97c40fa38b8083548b95` the Rayls
  Foundation fee address?
- **Q-E:** What exactly is the 3.84 RLS component (relayer service fee
  vs gas reimbursement)?
- **Q-F:** What is the separate transaction `0xacc7d175…` for (a 0.576
  RLS transfer with the address argument `0x71af…`)? The match
  3.84 × 15% = 0.576 is an arithmetic clue, not proof of purpose.

### 7.5 List of claims safe to use in the article (corrected, with classification)

1. "On 21 Nov 2026, transaction `0x09edab2b…` was recorded on-chain
   in block 24825928 (16:40:42 WIB) as a successful transferV2 call."
   — **Verified fact.** "The experiment links this transaction to a
   shielded payment of 6 RLS from @anara to @kittynim." —
   **Reconstruction** (app + registry + tx match; not an on-chain fact).
2. "The public sender of that transaction is not @anara. It is the
   relayer, `0xa5f0c684…`, calling the SharedVault contract
   (`0x9c5ad5e5…`) with a value of 0." — **Verified fact** (the tx `from`
   is the relayer; the @anara address is not in the tx).
3. "What the chain records is one nullifier, three commitments and
   three encrypted notes — and the integer 4,416 × 10¹⁸ appears in
   the transaction's statement. The app presents that integer as
   4.416 RLS and as the total fee." — **Verified fact** for the on-chain
   record and the integer's appearance; **inference** for the RLS label
   and the "total fee" meaning.
4. "The amount (6 RLS), the user-level sender and the user-level
   receiver do not appear in the transaction in plaintext. (The public
   transaction sender — the relayer — does appear; see claim 2.)" —
   **Verified fact** (checked fresh in the calldata, logs, and topics).
   The term "user-level" is used here to avoid confusion with the
   relayer as the public transaction sender.
5. "A separate transaction by the same relayer, three seconds later,
   called transfer() on the RLS token contract with the arguments
   (`0x71af…`, 0.576 RLS)." — **Verified fact** for the call and its
   timing; who `0x71af…` is and what the transfer is for: **unknown**.
6. "The receiver's app shows +6 RLS for the same transaction, and the
   app shows the shielded balances moving 321.4 → 327.4 (receiver)
   and 14.324 → 3.908 (sender)." — **Direct observation** (app display,
   not verified on-chain data).
7. "The proof is 256 bytes, according to the transaction's calldata
   structure. The app reported it was generated in 10 seconds in the
   browser." — **Verified fact** (size, calldata source) and
   **direct observation** (time, app display source).
8. "The usernames map to addresses on-chain in the public registry
   (@anara → `0x0c5b…`, @kittynim → `0x680d…`)." — **Verified fact**
   (registry UsernameSet).
9. "Rayls' own documentation describes a shielded send as showing
   only that a transfer happened, the relayer, and the gas fee." —
   **Official claim** (docs.rayls.com, cited in the initial audit).
10. "The commitments and ciphertexts are public as bytes; what is
    hidden is what they mean — the amounts and the owners." —
    **Verified fact** for the existence of the public bytes; **inference**
    for "what they mean is hidden" (based on the encrypted nature of
    the ciphertext, not on an inspection of its contents).

## 8. List of candidate commit files (for the article; NOT yet committed)

Integrity verification (22 Nov 2026, this round):
- Journey manifest: **12/12 entries OK** (SHA-256 + size match).
- TX manifest: **20/20 entries OK**.
- TX verifier: **23/23 PASS, exit 0**.
- Comparator v2.1.1: untouched (hash `bfef1f66…` — not re-verified
  in this round because it was not used; the comparator remains
  certified and unchanged).
- Raw evidence: unchanged (all manifest hashes match).

### 8.1 New files (this audit)

| File | Reason | Verification status |
|---|---|---|
| `experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r3.md` (this file) | Targeted audit report, revision r3, for the article; contains the four review corrections on r2 + the claim list + questions + the exact commit list (§8.6) | Written 22 Nov 2026; all numbers/addresses are the same as in r2 (no new re-derivation — this revision only fixes classifications and wording); the final size is checked in §8.5 |
| `experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r2.md` | Revision r2 (22 Nov 2026); kept as a revision record | **Superseded by r3**; unchanged since written (48,097 bytes, SHA-256 `00e464f29a3615e6…` — verified, see §8.5); **not proposed for the commit** (see §8.6) |
| `experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22.md` (r1) | First version of the audit (22 Nov 2026); kept as a revision record | **Superseded by r2/r3**; unchanged since written (35,269 bytes, SHA-256 `bd54c362c0418e10…`); **not proposed for the commit** (see §8.6) |

### 8.2 Existing files relevant to the article

| File | Reason | Verification status |
|---|---|---|
| `experiments/testnet-journeys/week2-private-payment/enygma-week2-private-payment-final.mp4` (720p) + `…-final-1080p.mp4` | The audited experiment video (main visual evidence) | Journey manifest 12/12 OK; the final video was watched in full in round r1 (12 frames + transcript) |
| `experiments/testnet-journeys/week2-private-payment/subs.ass` | Video subtitles | Manifest 12/12 OK; regeneration proven byte-identical (previous audit) |
| `experiments/testnet-journeys/week2-private-payment/manifest.json` | Manifest + SHA of the video/manifest (12 entries) | **12/12 OK** (re-checked in round r1) |
| `experiments/testnet-journeys/week2-private-payment/README.md` | Journey documentation + findings + limitations | Contents checked in round r1 (relayer panel + balances match the frames) |
| `experiments/testnet-journeys/week2-private-payment/EDIT-PLAN.md`, `QA-REPORT-V2.md` | Edit plan + video QA | Manifest 12/12 OK |
| `experiments/testnet-journeys/week2-private-payment/build-*.sh` | Video build scripts (reproducibility) | Manifest 12/12 OK |
| `experiments/transactions/tx-09edab2b/raw/*.json` (9 files) | Raw tx evidence (unchanged) | TX manifest **20/20 OK**; all key values were re-derived from these files in round r1 |
| `experiments/transactions/tx-09edab2b/decoded/*.json` (4 files) | Decoding + ABI bundle + lookup | Manifest 20/20 OK; selector/topic verified fresh via keccak in round r1 |
| `experiments/transactions/tx-09edab2b/TX-AUDIT-REPORT.md`, `gaps.md`, `TODO.md`, `ADDENDUM-2026-11-22.md`, `manifest.json` | Report + limitations + TX manifest (20 entries) | Manifest 20/20 OK; TODO updated 22 Nov (stage-1 close) + manifest updated; note: the "0.063168048 RLS" label in TX-AUDIT-REPORT.md:144 is a token-identity assumption (see §3.3) |
| `scripts/tx_audit_09edab2b.py`, `scripts/decode_tx_09edab2b.py`, `scripts/verify_tx_audit_09edab2b.py` | Fetch + decode + verifier scripts | Manifest 20/20 OK; verifier **23/23 PASS** (re-run in round r1) |
| `contracts/addresses/addresses.json` | Address map (relayer, vault, registry, RLS token) | INDEX hash matches (9,202 B / `f78f0128…` — re-checked in §8.5); relayer `0xa5f0c684…` matches the tx |
| `contracts/verified-source/README.md` | Status of "no verified source" for the vault implementation | Contents checked (initial audit); not re-verified this round (see §5.3) |
| `audit-reports/ENYGMA-TESTNET-AUDIT-REPORT.md` | Initial audit (docs, pilot blog, registry) — context | Byte-identical to the copy outside the repo (cmp, initial audit); unchanged this round |
| `tickets/rayls-team-questions-draft-2026-11-22.md` | Ticket draft (Q-A/Q-B from §7.4 are additional candidates) | Written 22 Nov; **not yet sent** |
| `INDEX.md`, `RESEARCH-TRAIL.md`, `REPRODUCE.md`, `README.md` | Index/trail/repro entries for the new audit file | **Updated at commit time, after review** (not now) |

### 8.3 What does NOT go into the commit (stays local-only)

- Raw footage `raw-data/videos/week2-source-footage-….mp4`
  (24,777,960 B) and the VO mp3 `raw-data/videos/ElevenLabs_….mp3`
  (2,953,936 B) — already in `.gitignore` (exact-path); unchanged,
  not moved, not compressed.
- Working files for this audit (`~/workspace/rayls-article-audit-2026-11-22/`:
  frame JPGs, Whisper transcript, `derive.py`) — working notes outside
  the repo; the frames are derivatives of the gitignored footage.

### 8.4 Commit notes

- No file was staged/committed/pushed in this round or in this
  revision round.
- At commit time (after Anara's review): include the new files in §8.1
  (r3 as the current audit report; r1/r2 do not go in) + the files
  proposed in §8.6; update INDEX/TRAIL/REPRODUCE for the new audit file
  (r3) — that update has NOT been done in this round (outside the
  limit: "do not change other files"); run the 23/23 verifier once
  more before committing.
- The open questions in §7.4 (Q-A, Q-B) may be added to the ticket
  draft after Anara approves — not now.

### 8.5 Verification of revision round r3 (22 Nov 2026)

**Explanation of the r2 size difference (correction 4).** §8.5 of r2
states 47,530 bytes, while the canonical r2 file is **48,097 bytes**
(SHA-256 `00e464f29a3615e6cd2fdef0b1b8bd2cc930917486fc00d26ae3a6711c36cd9d`,
re-measured this round). The cause: the number 47,530 was measured on
an intermediate state of r2 — after the first draft of §8.5 was written,
but BEFORE §8.4 was restored into the file. Restoring §8.4 added 567
bytes (48,097 − 47,530), so the size and SHA changed, but the §8.5 text
was not updated after that restoration. The number 47,530 is a stale
intermediate measurement, not the final size. The r2 file itself was
never changed afterwards (verified: still 48,097 bytes /
`00e464f2…`). The r1 file also did not change: 35,269 bytes, SHA-256
`bd54c362c0418e10…`.

**Size and SHA of r3.** Final size of r3: **59,742 bytes** (measured after
the last edit; this number was filled in by replacing digits of the
same length so the size did not change). The SHA-256 of r3 is
deliberately not written inside this file: a file cannot contain its
own hash without becoming stale, because writing the hash changes the
file's contents and therefore changes its hash. The final SHA-256 of r3
is stated in the delivery message for this report (measured after the
last edit) and can be verified independently with:
`sha256sum experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r3.md`.

**Integrity (re-checked this round, read-only):**
- Raw footage: 24,777,960 bytes, SHA-256
  `610a5cd30d3cdc457ea836e69c74229a6fb42d3530f4227a2269a00f4af311fa`
  — **unchanged**.
- VO mp3: 2,953,936 bytes, SHA-256
  `ebb2fdda3d84ea99fece015ca075cd7b74f3f96a6630c13182b5eb6f2b5c6a7c`
  — **unchanged**.
- Raw TX evidence: manifest **20/20 OK** (SHA + size match);
  journey manifest **12/12 OK**.
- Comparator v2.1.1: SHA-256
  `bfef1f667408b227cac5b33e27c9352b5ad721ca0b78ed91899d8befdcac08a3`
  — **unchanged** (certified, untouched).
- TX verifier: **23/23 PASS, exit 0** (re-run).
- `contracts/addresses/addresses.json`: 9,202 bytes /
  `f78f012886035836` — matches INDEX.
- Git: 28 status lines (9 modified + 19 untracked), **0 staged**,
  no commit/push (see §8.6).
- Editorial sweep of r3: no factual statement that the 0.576 RLS
  transfer is a fee payment or is addressed to an already-concluded
  recipient; every mention of "4.416"/"4,416" is in the three-layer
  context (§3.2) or as arithmetic on app-display values / as an example
  of prohibited wording (K4, §3.2).

### 8.6 Exact list of files proposed for the commit

Measured: 22 Nov 2026 ~14:10 WIB. No staging, commit, or push in
this round.

#### 8.6.1 Full `git status --short` output (28 lines)

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

#### 8.6.2 Tracked changes: 9 files (97 insertions, 2 deletions)

| File | Changes |
|---|---|
| README.md | +24/−2 (status + finalization links) |
| contracts/abis/README.md | +11 (ABI documentation) |
| contracts/addresses/README.md | +10 (address-map documentation) |
| contracts/verified-source/README.md | +14 (verified-source status) |
| experiments/README.md | +4 |
| experiments/transactions/README.md | +8 |
| findings/README.md | +8 |
| raw-data/videos/README.md | +11 (local-only footage + VO markers) |
| scripts/README.md | +9 |

#### 8.6.3 Untracked files: 73 files (expanded, after r3)

73 = 72 (before r3) + r3. The details are in §8.6.4 (71 proposed)
and §8.6.5 (2 not proposed: r1, r2).

#### 8.6.4 Proposed for the commit: 80 files

9 tracked-modified (§8.6.2) + the following 71 untracked files:

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

(9 tracked from §8.6.2 + 71 above = **80 files**.)

#### 8.6.5 What is NOT proposed for the commit

| File | Reason |
|---|---|
| `experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22.md` (r1) | Superseded by r2/r3; local revision record |
| `experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r2.md` | Superseded by r3; local revision record |
| `raw-data/videos/week2-source-footage-610a5cd30d3cdc457ea836e69c74229a6fb42d3530f4227a2269a00f4af311fa.mp4` (24,777,960 bytes) | Local-only, excluded by `.gitignore` (exact-path); hash `610a5cd3…` unchanged |
| `raw-data/videos/ElevenLabs_2026-11-21T13_44_30_Zara_-_The_Warm__Real-World_Conversationalist_pvc_s50_sim75_v4.mp3` (2,953,936 bytes) | Local-only, excluded by `.gitignore` (exact-path); hash `ebb2fdda…` unchanged |

There is no other file in the working tree outside the lists in §8.6.4 and §8.6.5.

#### 8.6.6 Notes before the commit (not yet done)

- `INDEX.md`, `REPRODUCE.md`, `RESEARCH-TRAIL.md` (included in
  §8.6.4) need updating to reference the r3 audit file — that update
  has NOT been done in this round, per the limit "do not change other
  files". Do that update before the commit, after this review.
- `experiments/transactions/tx-09edab2b/.src/index.html` contains the
  old text "(the check has not been run yet)" — deliberately kept as
  the source of the 21 Nov PDF build (see the 22 Nov finalization); do
  not edit it without a decision to rebuild the PDF.
- `tickets/rayls-team-questions-draft-2026-11-22.md` is included as a
  draft — the ticket has NOT been sent.
- Run the 23/23 verifier once more immediately before the commit.

## Appendix — working evidence for this round (outside the repo)

- `~/workspace/rayls-article-audit-2026-11-22/frames/` — 12 final-video
  frames + 12 raw-footage frames (JPG, 960 px).
- `~/workspace/rayls-article-audit-2026-11-22/transcript/` — complete
  VO transcript, 183.56 sec (faster-whisper-small, 4 chunks).
- `~/workspace/rayls-article-audit-2026-11-22/derive.py` — re-derivation
  script from the raw data (selector, statement, ciphertext, fee,
  registry, logs).
