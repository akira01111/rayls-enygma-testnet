# TX Audit Report — Rayls Enygma Week 2 Experiment

**Transaction:** `0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb`
**Network:** Rayls Public Testnet, chain ID 7295799 (`0x6f5337`)
**Block:** 24825928 (2026-11-21 09:40:42 UTC; exactly 1 transaction in the block)
**Audit date:** 21–22 Nov 2026 (retrieved 21 Nov 16:13–16:29 UTC; Anara asleep, overnight job)
**Experiment:** private payment of 6 RLS from @anara to @kittynim, recorded by Anara
on video with ElevenLabs (Zara) voice-over. This audit examines the on-chain
transaction only; the wallet UI / VO / video are treated as experiment context,
not as on-chain evidence.

**Labels used** (same 6-label taxonomy as the initial audit):
verified-fact / official-claim / direct-observation / reconstruction / inference / unknown.
Every claim in `decoded/audit_summary.json` carries one of these labels.

**Scripts (versions recorded; see manifest):**

| script | version | role |
|---|---|---|
| `scripts/tx_audit_09edab2b.py` | 1.1.0 | fetch raw data via curl (v1.0.0 used urllib and FAILED on transport — see §6) |
| `scripts/decode_tx_09edab2b.py` | 1.0.0 | decode + hex search + fee + summary (no network; reads raw files only) |
| `scripts/verify_tx_audit_09edab2b.py` | 1.0.0 | INDEPENDENT verification: re-reads evidence, recomputes SHA-256, checks manifest + cross-consistency |

**Evidence package:** `experiments/transactions/tx-09edab2b/` — raw JSON (immutable,
chmod 444), decoded JSON, this report, `gaps.md`, `TODO.md`, `manifest.json`.
SHA-256 for every file is in `manifest.json`. The combined review PDF is a
derivative copy only (`01_tx_audit_complete_history.pdf`).

---

## 1. What was checked

- RPC (curl, browser UA, up to 5 attempts per call): `eth_chainId`,
  `eth_getTransactionByHash`, `eth_getTransactionReceipt`, `eth_getBlockByNumber`,
  `eth_getLogs` (single-block cross-check), `eth_getCode` + EIP-1967 slot reads
  for the destination/implementation/token/Multicall3/registry.
- Explorer API: `gettxinfo`, `gettxreceiptstatus`, `txlist` for the relayer
  (blocks 24825800–24826200), `getLogs` for UserRegistry `UsernameSet`
  (blocks 23212003–24910000, 200k-block pages).
- Function selector + event topic0s: 4byte.directory (all count 0 — see §6),
  then local pure-Python keccak256 against the demo-bundle IEnygmaDvp ABI
  (`decoded/bundle-abi-extract.json`; bundle SHA-256 `7530bbc2…` matches the
  audit §C.4 — bundle unchanged since 21 Nov).
- Calldata parsed structurally as ABI words; logs decoded per the bundle ABI;
  case-insensitive hex search for sender/receiver/token/relayer/amounts;
  fee computed from receipt values; one related relayer tx fetched and decoded.

## 2. Findings per question

### Q1 — Receipt / status — verified-fact
Status `0x1` (success). Block 24825928, transactionIndex 0, gasUsed 1,316,001
of gasLimit 1,630,484, effectiveGasPrice 48,000,000,000 wei, 7 logs,
contractAddress null. Block 24825928 contains exactly this one transaction.
Explorer agrees on block, from, gas limit/price/used, status, hash.

### Q2 — Calldata / function — verified-fact (with a stated limit)
Function is **transferV2**. Selector `0xaacd552c` equals the first 4 bytes of
keccak256 of the canonical signature
`transferV2((((uint256,uint256),(uint256[2],uint256[2]),(uint256,uint256)),uint256[],uint256,uint256),bytes[],bytes[])`
from the bundle ABI. Calldata (4,804 bytes) parses cleanly with zero trailing
bytes: receipt tuple with an 8-word (256-byte) Groth16 proof — matching the VO
claim of a 256-byte proof — statement of 10 uint256 values, numberOfInputs 1,
numberOfOutputs 3, ciphertextI 3 entries × 1,088 bytes, ciphertextII 3 entries
× 92 bytes.
**Limit:** no verified contract source exists for the deployed vault
implementation, so what transferV2 does internally is NOT proven from source;
the function identity and the calldata structure are proven from the selector
match + the clean structural parse. The ABI used is the demo app's client-side
ABI, not verified on-chain source.

### Q3 — Destination contract / SharedVault — verified-fact
Destination is the SharedVaultProxy (yx)
`0x9C5Ad5e5Ea5b5910E7fD1E1CC7b70ce0e4bF06c2`, called **directly** (NOT via
Multicall3 — unlike the audit's sampled shielded-transfer tx `0x7f72…`).
Its EIP-1967 implementation slot reads
`0xAd9667049f14D1757D147F652c41Dc241C57091C`, matching the live vault-yx
implementation recorded in the audit (§C.3). The Explorer's displayed method
name (transferV2) is a cross-check only; the proof is the selector match (Q2).

### Q4 — Event logs — verified-fact
7 logs, all from the vault proxy: **1× Nullifier** (vaultId 2, treeNumber 0,
nullifier `0x0c0f23a6…`), **3× Commitment** (vaultId 2, commitments
`0x094b233a…`, `0x2304db2e…`, `0x206ed94a…`), **3× EncryptedNote** (same 3
commitments, each with 1,312 bytes of ciphertext data = two byte arrays:
ciphertextI 1,088 bytes + ciphertextII 92 bytes). No ERC20 Transfer log, no
PaidOut, no PartialWithdrawal, no log from any other address. This matches the
audit's shielded-transfer classification (Commitment + EncryptedNote +
Nullifier, no payout). The 3 calldata ciphertexts are byte-identical
(SHA-256) to the 3 log ciphertexts.

### Q5 — Commitment / encrypted-note observability — direct-observation
Commitment hashes are public (3 hashes in topics and in the calldata
statement). EncryptedNote ciphertexts are public as opaque bytes (1,312 bytes
each; lengths + SHA-256 fingerprints recorded). The note VALUES (amounts,
sender, receiver, token) are NOT visible in the ciphertext. One input note was
spent (1 nullifier) and 3 output notes were created (3 commitments).

### Q6 — Hidden vs visible — direct-observation
NOT visible anywhere in the raw transaction input, receipt, or logs
(case-insensitive hex search, bare address and 32-byte-word forms): receiver
EVM `0x680d…0efc`, sender EVM `0x0c5b…0b5`, RLS token proxy `0x07e1…7ea`,
amount 6 RLS as 6e18, fee values 3.84 / 0.58 / 4.42 RLS as 18-decimal words.
FOUND in the on-chain data: the fee TOTAL **4.416 RLS as a 32-byte word in the
calldata** (statement[8] = 4,416,000,000,000,000,000 wei); the relayer address
as tx.from; the vault proxy address (also as statement[7]); the spent
nullifier hash and the 3 commitment hashes (in the calldata statement and in
log topics).
The 6 RLS figure, the two usernames, and the token type come only from the
wallet UI / VO / video (direct observation of the experiment), NOT from
on-chain data. "Not visible in this data" is NOT proof that the information is
unknowable in principle: parties holding the relevant keys (receiver view key,
sender keys, auditor keys) could decrypt the notes; this audit does not test
that.

Statement layout (10 values): [0]=0, [1]=0, [2]=`0x0d6edc87…` (unidentified
hash — position before the nullifier is consistent with a Merkle root, not
proven), [3]=nullifier (verified vs log 0), [4–6]=the 3 commitments (verified
vs logs 1–3), [7]=vault address (verified vs to-address — the proof is bound
to this vault), [8]=4.416 RLS fee (verified), [9]=`0x0f58ff41…` (unidentified
hash — position after the fee is consistent with a binding/ciphertext hash,
not proven).

### Q7 — Relayer role / sender link — reconstruction
tx.from is the relayer `0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8`
(verified-fact). The registry shows that address holds the username
`rayls-relayer` (verified-fact from UsernameSet logs; first registration in
the set). The docs claim the relayer submits user transactions and the public
sender shown is the relayer (official-claim). Whether THIS tx was submitted on
behalf of @anara (`0x0c5b…0b5`) is a **reconstruction, not an on-chain fact**:
the on-chain data contains no link to @anara (no sender address, no username,
no key). The link rests on experiment context: the same block/time/method/vault
as the success screen in the recorded experiment, the matching
nullifier/commitment pattern, and the shielded-balance decrease shown in the
wallet UI. from=relayer alone is NOT proof that the relayer is the sender, and
the absence of the sender address is NOT proof of absolute unlinkability.
Registry resolutions (verified-fact): @anara →
`0x0c5b369ad7d0c4e051a2887575f7fc85e0ccd0b5` (block 0x1645a5f);
@kittynim → `0x680d90983da58bcb7d127e3421193274e84e0efc` (block 0x167bc88,
matches the address shown in the video). 195 usernames observed
(audit §D.6 recorded 194 at 21 Nov; +1 since).

### Q8 — Fee vs wallet — verified-fact (fee total), reconstruction (split)
- On-chain gas for the target tx: 1,316,001 × 48,000,000,000 wei =
  63,168,048,000,000,000 wei = **0.063168048 RLS** (18 decimals assumed).
  This does NOT equal the wallet-displayed "gas" fee of 3.84 RLS. The wallet's
  "gas" label is the relayer service fee, not the chain gas cost.
- The TOTAL fee IS public on-chain: calldata statement[8] = **4.416 RLS**
  exactly, matching the wallet detail-activity fee 4.416 RLS.
- The 0.58 foundation fee has an on-chain counterpart: 4 blocks later (block
  24825932) the relayer transferred **0.576 RLS** of the RLS token to
  `0x71af09966cbed4434cca97c40fa38b8083548b95` (tx
  `0xacc7d175…`, verified-fact; 0.576 rounds to 0.58 at 2 decimals). That
  address is recorded in the audit map as the Auditor EOA; whether it is the
  Rayls Foundation fee address is UNKNOWN.
- The split closes exactly: **4.416 = 3.84 + 0.576**, and **3.84 × 15% =
  0.576 exactly**. So the docs' "relayer fee 15% to Rayls Foundation" reads
  as 15% OF THE RELAYER FEE (not of the payment): the foundation portion
  (0.576) is verified on-chain, the relayer-retained portion (3.84) is
  determined arithmetically from two verified on-chain numbers, though it
  never appears as its own word in the data.
- Reconstruction (not verified): 1 input note spent, 3 output notes created;
  the sender shielded balance fell by 10.416 RLS = 6 payment + 4.416 fee, so
  the 4.416 fee plausibly sits inside the shielded notes (one output note to
  the relayer, of which 0.576 went on to the foundation address and 3.84 stayed
  with the relayer). Note values are encrypted, so this mapping cannot be
  verified from the chain.

## 3. Comparison vs wallet display / Explorer / video

| item | wallet / video | on-chain (this audit) | verdict |
|---|---|---|---|
| method | transferV2 | transferV2 (selector match) | agrees |
| block | 24825928 | 24825928 | agrees |
| public sender | Relayer | tx.from = relayer | agrees |
| value field | 0 USDR | tx.value = 0 | agrees |
| ZK proof | 256 bytes, 10 s in-browser | proof struct = 256 bytes; 10 s is VO only, not measurable on-chain | size agrees; time unverified |
| sender balance | 14.324 → 3.908 (−10.416) | 1 nullifier spent, 3 notes created; values encrypted | consistent, values not visible |
| receiver balance | 321.4 → 327.4 (+6) | 6 RLS not visible anywhere on-chain | amount from wallet only |
| fee gas | 3.84 RLS | chain gas 0.063168048 RLS; statement fee 4.416 RLS; 3.84 = 4.416 − 0.576 | label differs; total agrees |
| fee foundation | 0.58 RLS | 0.576 RLS to 0x71af… (block 24825932) | agrees within rounding |
| fee total | 4.42 / 4.416 RLS | statement[8] = 4.416 RLS exactly | agrees (4.42 = rounded display) |
| receiver | @kittynim | address not in tx data; registry resolves @kittynim → 0x680d…0efc | identity from registry + video, not from tx |

## 4. Relation to the prior archives

**Strengthens:**
- Audit §D.7 shielded-transfer classification (Commitment + EncryptedNote +
  Nullifier, no payout) — this tx is a clean instance: 1/3/3.
- Audit §F privacy limits — sender, receiver, amount, token type are absent
  from the tx data, as the docs claim; the audit's "shielded transfers reveal
  no who/how much/which token" holds for this tx.
- Audit §C.3 vault-yx implementation (`0xAd966704…`) — re-confirmed live via
  the EIP-1967 slot.
- Bundle hash `7530bbc2…` unchanged since the 21 Nov audit; the bundle ABI
  resolves the function and all three event topic0s on-chain.

**Adds (new evidence):**
- The fee TOTAL (4.416 RLS) is a public statement value, not hidden — the
  docs' "a shielded send shows only that a send happened, the relayer, and
  its gas fee" is imprecise: this tx publicly commits to the fee amount and
  to the vault address in the statement.
- The foundation fee has a concrete on-chain settlement: 0.576 RLS to
  `0x71af…` (Auditor EOA per the audit map) 4 blocks after the payment.
- "Relayer fee 15% to Rayls Foundation" is consistent with 15% OF THE
  RELAYER FEE (3.84 × 15% = 0.576), not 15% of the payment (6 × 15% = 0.9).
- The wallet's "3.84 gas" is a relayer service fee, not chain gas (chain gas
  is 0.063 RLS). The 4.42 vs 4.416 difference is display rounding (4.416
  rounds to 4.42), not a discrepancy.
- Registry resolutions for both experiment accounts (@anara, @kittynim).
- Statement layout for transferV2 (positions 3–8 verified by value matching;
  positions 0, 1, 2, 9 unidentified — a new gap).

**Contradicts nothing** in the prior archives. No prior finding was overturned.
The 0.0001 RLS fee discrepancy from the earlier demo is a different item and
stays UNRESOLVED (not addressed here).

## 5. Limitations

1. No verified contract source for the deployed vault implementation; ABIs
   come from the demo-bundle client code.
2. 4byte.directory has no entry for the selector or the three event topic0s.
3. Note values are encrypted; the 3-output-note mapping (6 / 3.908 / 4.416)
   is a reconstruction, not a verified fact.
4. The 3.84 component never appears as its own word; determined
   arithmetically (4.416 − 0.576).
5. Whether `0x71af…` (Auditor EOA) is the Rayls Foundation fee address is
   unknown.
6. Statement positions 0, 1, 2, 9 are unidentified (no published layout).
7. One transaction + one related tx only; nothing is proven about other
   shielded transfers.

## 6. Method notes (honest record)

- **Fetch v1.0.0 failed on transport** (urllib): `eth_getTransactionByHash`,
  `eth_getTransactionReceipt`, `eth_getLogs` died with IncompleteRead /
  RemoteDisconnected (5/5 attempts each); small responses succeeded. No valid
  data was captured; the partial raw directory was removed. v1.1.0 switched
  the transport to curl and passed 18/18.
- **RPC `eth_getLogs` range limit:** the node rejects ranges over 100,000
  blocks (`query exceeds max block range 100000`, code −32602). The registry
  lookup fell back to Explorer API pagination (200k-block pages).
- **Decode bugs found and fixed during development:** (a) the first parse read
  ABI head offsets from the wrong base (input start instead of after the
  4-byte selector), giving numberOfInputs/Outputs 0; (b) the `bytes[]` parse
  treated element offsets as lengths. Both were fixed, the derived outputs
  were deleted and regenerated from scratch; the final script (v1.0.0 on disk)
  parses the calldata with zero trailing bytes and SHA-256-matched
  ciphertexts. The raw files were never touched.
- The related tx (`0xacc7d175…`) was found by listing the relayer's txs in
  blocks 24825800–24826200 (exactly 2 txs: the target and the fee settlement).
  It is saved as `raw/related-tx-0xacc7d175.json` and labelled as a related tx,
  not part of the target tx.

## 7. Files in this package

Paths are repo-relative under
`experiments/transactions/tx-09edab2b/`. Byte sizes are listed here; SHA-256
for every file is in `manifest.json`.

- `raw/transaction.json` — eth_getTransactionByHash (+ chainId/blockNumber sanity)
- `raw/receipt.json` — eth_getTransactionReceipt
- `raw/logs.json` — receipt logs copy + block-level eth_getLogs cross-check
- `raw/block.json` — eth_getBlockByNumber 24825928
- `raw/contracts.json` — eth_getCode + EIP-1967 slot reads
- `raw/explorer.json` — Explorer gettxinfo + gettxreceiptstatus
- `raw/explorer-relayer-txlist.json` — relayer txlist, blocks 24825800–24826200
- `raw/registry-usernames.json` — 195 UsernameSet logs (23212003–24910000)
- `raw/related-tx-0xacc7d175.json` — fee-settlement tx (block 24825932)
- `decoded/decoded_events.json` — per-log decode, calldata parse, hex search, fee
- `decoded/audit_summary.json` — answers to the 8 questions, with labels
- `decoded/bundle-abi-extract.json` — bundle ABI entries + provenance
- `decoded/lookups-4byte.json` — 4byte responses (all count 0)
- `TX-AUDIT-REPORT.md` — this report
- `gaps.md` — remaining gaps
- `TODO.md` — unfinished work
- `manifest.json` — every file: path, bytes, SHA-256, source, retrieved_at_utc
