# TODO — Week 2 TX audit (0x09edab2b…)

Unfinished work, blocked items, and next steps for the morning review.
Nothing here is a commitment to do it — items need Anara's decision where noted.

## Done in this package
- [x] Raw fetch (PASS 18/18, curl transport; v1.0.0 urllib failure documented)
- [x] Decode: selector + 3 event topic0s resolved (keccak vs bundle ABI)
- [x] Calldata structural parse (0 trailing bytes; ciphertexts SHA-256-matched to logs)
- [x] Hidden-vs-visible hex search (sender/receiver/token/6 RLS not in tx data; fee total 4.416 RLS IS in the statement)
- [x] Fee computation + related fee-settlement tx (0.576 RLS, block 24825932)
- [x] Registry lookup: @anara and @kittynim addresses resolved (195 usernames)
- [x] Explorer cross-check (gettxinfo, gettxreceiptstatus, relayer txlist)
- [x] Report (TX-AUDIT-REPORT.md), gaps.md, this TODO.md
- [x] Independent verify script (scripts/verify_tx_audit_09edab2b.py) — see manifest
- [x] Manifest (all files, SHA-256) + combined review PDF (01_tx_audit_complete_history.pdf)

## Not done / needs a decision
- [ ] **Open the ticket(s) to the Rayls team** (needs Anara's decision): bx
  proxy-vs-bundle mismatch; auditor scope conflict; 0.0001 RLS fee origin;
  RLS token slot anomaly; statement layout positions 0/1/2/9; whether
  0x71af… is the foundation fee address; confirm the "15% of the relayer
  fee" reading; confirm the wallet "gas" label meaning. Ticket-first before
  any public conclusion (mod guidance).
- [ ] **Approve / reject experiments G.1–G.6** (needs Anara's decision):
  shielding ERC-20 visibility, fee experiments, relayer `from` sweep across
  the 511 vault txs, proof-time measurement.
- [x] **Re-fetch verification**: re-run the fetch script once and diff against
  the saved raw files; any difference must be documented, not forced to match.
  (Historical RPC data should be identical. **DONE 22 Nov 2026 11:02 WIB**:
  re-fetch run + identity check; comparator v2.1.1 **CERTIFIED 12:33 WIB**
  — stable historical payload 9/9 PASS, 6 dynamic fields recorded
  separately, 4 post-snapshot registry events above tip 24,869,295
  listed separately. Comparator v1's exit 1 on the same pair was solely
  the live `eth_blockNumber` read. Stage 1 CLOSED 22 Nov 2026. This
  closes stage 1 (re-fetch verification) only — not the whole audit.)
- [ ] **Article writing**: NOT started. Only after the ticket + experiments
  decisions. The previous article's conclusion (selective auditing not
  independently verifiable) STANDS unless new evidence appears.
- [ ] **Fee-settlement pattern check**: does the separate ERC20 fee transfer
  a few blocks after the payment hold for other shielded transfers? Needs a
  sample across the 511 vault txs (not done).
- [ ] **Module 02**: NOT started — blocked until Module 01 is published
  (Anara's rule). This TX audit is a separate evidence job, not Module 02.
- [ ] **Commit / push**: NOT done and NOT to be done without Anara's explicit
  approval. The repo state is unchanged (HEAD 1676829 + untracked Module 01
  and TX-audit files). pdf/ stays local, never in a commit.

## Blocked / failed lookups (recorded, not hidden)
- 4byte.directory: selector 0xaacd552c + all three event topic0s return
  count 0 (not in the database). Resolved instead via bundle ABI + keccak.
- RPC eth_getLogs over >100,000 blocks rejected (code −32602); registry
  lookup used Explorer API pagination instead.
- Fetch v1.0.0 (urllib) failed on transport for 3 calls (IncompleteRead);
  v1.1.0 (curl) succeeded. No data was lost; the failure is documented in
  the report §6.
- No verified contract source for the deployed vault implementation exists
  (bundle ABI used instead) — a standing limitation, not a failure of this run.
