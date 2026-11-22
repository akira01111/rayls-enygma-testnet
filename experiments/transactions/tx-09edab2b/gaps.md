# Remaining gaps — after the Week 2 TX audit (0x09edab2b…)

For each gap from the initial audit (ENYGMA-TESTNET-AUDIT-REPORT.md §H/§I and
the experiment plan §G): what this TX audit resolves vs what stays unknown.
Nothing here is forced to an answer.

## 1. Deployment identity unknowns — STAYS UNKNOWN
- **bx proxies do not match the bundle** (live registry/vault bx implementations
  are not in the bundle; the bx ownerCalls upgrade was never executed).
  This TX audit touches only the yx vault; the bx mismatch is untouched.
- **EnygmaDvp contract** (`0x7ec57a8f…`) and **forwarder rotation** (new
  forwarder `0x12B66400…` already used by the latest registration): untouched.
- **RLS token proxy EIP-1967 slot anomaly** (slot contains its own address):
  untouched.
- New sub-question from this audit: is `0x71af09966cbed4434cca97c40fa38b8083548b95`
  (Auditor EOA per the audit map) the Rayls Foundation fee address? The
  0.576 RLS settlement went there, but no source links the two roles.

## 2. Selective auditing — UNVERIFIED (unchanged)
- Still 7 AuditorAdded / 4 AuditorKeyGiven / 1 AuditorPersonalKeySet (10 Nov);
  this TX audit adds no auditor evidence. The auditor-access scope conflict
  (AMA/blog: scoped; docs/reference repo: network-wide) is still unresolved.
- New observation, NOT verification: the Auditor EOA received the 0.576 RLS
  foundation-fee settlement. Receiving a fee does not prove auditor access to
  shielded data, and must not be cited as such.
- Ticket-first before any public conclusion (mod guidance).

## 3. Shielded-transfer observability limits — PARTIALLY RESOLVED
- **Resolved for one transfer:** this tx proves the pattern end-to-end —
  1 nullifier spent, 3 commitments + 3 encrypted notes created, statement
  with vault binding + public fee total (4.416 RLS), no plaintext sender /
  receiver / amount / token in the tx data. The docs' "shows only that a send
  happened, the relayer, and its gas fee" is imprecise for this tx (the fee
  total and the vault address are also public in the statement; the "gas fee"
  shown is the relayer fee, not chain gas).
- **Stays unknown:** whether shielding amounts are visible via ERC-20
  Transfer logs (audit §G.2) — this tx is a shielded transfer and has NO
  Transfer log, but the shielding path itself was not tested here. The
  relayer-`from` check across all 511 vault txs (audit §I) was not done —
  only this tx + the related fee tx were checked.
- **New gap:** transferV2 statement positions 0, 1, 2, 9 are unidentified
  (two zeros, two hashes). Positions 3–8 are verified by value matching;
  the Merkle-root / binding-hash readings for 2 and 9 are inferences only.

## 4. Docs / contracts unproven — PARTIALLY RESOLVED
- **Resolved:** the bundle ABI's transferV2 signature is confirmed on-chain
  (selector `0xaacd552c` = keccak256 of the canonical signature); the three
  event signatures are confirmed on-chain (topic0 matches); the bundle hash
  is unchanged since 21 Nov.
- **Stays unproven:** no verified contract source for the deployed vault
  implementation — transferV2's internal logic (proof verification, note
  handling, fee accounting) is not proven from source. The "relayer fee 15%
  to Rayls Foundation" claim is now consistent with 15% OF THE RELAYER FEE
  (3.84 × 15% = 0.576 exactly), but the docs do not state the base explicitly
  — confirm with the team before publishing that reading.

## 5. Fee discrepancies — PARTIALLY RESOLVED
- **Resolved for this experiment:** 4.42 vs 4.416 = display rounding
  (statement[8] = 4.416 RLS exactly); the wallet's 3.84 "gas" is the relayer
  service fee (4.416 − 0.576 = 3.84), not chain gas (0.063168048 RLS);
  the 0.58 foundation fee = 0.576 RLS on-chain (rounds to 0.58).
- **Stays UNRESOLVED:** the 0.0001 RLS fee discrepancy from the earlier demo
  (a different experiment) — never call it rounding; untouched by this audit.
- **Stays unknown:** why the relayer fee is 3.84 RLS for this payment
  (flat fee? computed from what?); whether the fee-settlement pattern
  (a separate ERC20 transfer a few blocks later) holds for other shielded
  transfers.

## 6. Proof time — UNVERIFIED (unchanged)
- The VO's "256-byte proof, generated in 10 seconds" — the 256-byte size is
  confirmed on-chain (proof struct = 8 words = 256 bytes); the 10-second
  generation time is not measurable on-chain and was not re-measured here.
  Proof-time figures still differ across sources (408 ms vs ~2.2 s vs ~3 s
  vs "under 4 s").

## 7. Other audit §I items — NOT DONE (still open)
- Experiments G.1–G.6 (need Anara's approval): shielding ERC-20 visibility,
  fee experiments, relayer `from` sweep, proof-time measurement.
- Implementation source verification vs the public repo.
- Continuous monitoring + separate finality experiment; load test only in an
  appropriate environment.
- Read IACR ePrint 2025/1638 + 2025/1639; re-check demo persistence; verify
  EnygmaDvp; check USDr precompile nature.
