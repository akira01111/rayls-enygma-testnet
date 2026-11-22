# G.1–G.6 — decision table (NOT run; needs Anara's approval per experiment)

Source: initial audit `audit-reports/ENYGMA-TESTNET-AUDIT-REPORT.md` §G
(22 Nov 2026). Nothing here has been executed. Each row states what
the experiment would do, what it needs, whether it is read-only or
changes state, the risks, a rough cost/time estimate, and the decision
still needed. **Estimates are estimates** (based on the Week 2 TX audit:
chain gas ~0.063 RLS per tx; faucet 1×/hour per the pilot blog; testnet
RLS is faucet-funded, not bought). Nothing is a commitment.

## Table

| # | Objective | Hypothesis | Data needed | Read-only / transaction | Risk | Estimated cost / time | Decision needed |
|---|---|---|---|---|---|---|---|
| G.1 | Full flow shield → transfer → unshield on a new testnet wallet, each step in a small and different amount so it can be tracked; match the event pattern against classification D.7 | The three actions really are separate as classified (different event log per action) | New testnet wallet; faucet RLS; tx hash + block + event log per step | **Transaction** (4 tx: registration, shielding, transfer, unshielding) + state change | New wallet + faucet; small amounts but testnet gas cost still applies; risk of a wrong step in the flow (mitigation: small amounts, one step at a time, verify each receipt) | Cost: testnet gas ~0.06 RLS/tx × 4 ≈ 0.25 RLS (faucet, $0). Time: ~1–2 hours of active work + faucet wait 1×/hour | Approve/reject; amount per step; whether to use a new wallet or an existing wallet |
| G.2 | Test whether the shielding amount is publicly visible through ERC-20 token logs (RLS Transfer + USDr) over the same block range as vault yx, matched against the 272 shielding txs | The shielding amount is visible through token logs even though the vault logs do not show it — or it is not visible | RLS `Transfer` log (`0x07e17E17…`) + USDr (`0x0000…0400`) over the vault yx block range; list of 272 shielding txs | **Read-only** (only reading logs via RPC/Explorer; no transaction, no signature) | No funds at risk; risk is only analysis time + large log volume (272 tx × block range) | Cost: $0. Time: ~1–2 hours of analysis (log fetch + matching) | Approve/reject; block range to use |
| G.3 | Measure the actual fee per action (registration, shielding, transfer, unshielding) from receipts; compare against the docs' claims (relayer 15% to the Foundation; USDr +0.25%); investigate the origin of the 0.0001 RLS discrepancy | The fee per action can be measured and explained; the 0.0001 RLS discrepancy has an identified component (not rounding) | Experiment tx receipts per action; wallet vs on-chain fee breakdown; 13 Nov demo data (note: demo tx hashes were not recorded) | **Transaction** (using txs from G.1; no new txs if G.1 has already run) + read-only analysis | Same as G.1 if new txs are needed; if using G.1 txs, no additional risk | Cost: $0 extra if using G.1 txs (if new txs: ~0.06 RLS/tx). Time: ~1 hour of analysis | Approve/reject; whether to combine with G.1 or run standalone |
| G.4 | Measure proving time locally (or note the time from the UI demo); compare against the 4 official figures that disagree with each other (408 ms / ~2.2 s / ~3 s / "under 4 s") | The official figures were measured under different conditions (device, input size, network) | Local proving time + device + input size + network conditions; the 4 official figures + their sources | **Read-only** (local measurement; no transaction, no signature) | No funds at risk; figures without context are meaningless (mitigation: record device + input + network) | Cost: $0. Time: ~30 minutes of measurement + recording | Approve/reject; device to use for measurement |
| G.5 | Test the bx deployment and the "next" forwarder: whether bx can still be used (bx configuration demo); observe whether new registrations keep using forwarder `0x12B66400…` | bx is an early deployment that was not continued; forwarder rotation is in progress (or not) | bx configuration demo attempt; observation of new registrations (latest `UsernameSet` logs) | **Mixed**: forwarder observation = read-only; bx demo attempt = transaction (if the bx demo is run) | The bx demo may fail / be unsupported (that itself is a result); do not conclude anything about bx before ticket Q2 is answered | Cost: testnet gas if the bx demo is run (~0.06 RLS). Time: ~1 hour (observation + attempt) | Approve/reject; whether the bx demo is run, or only forwarder observation; order vs ticket Q2 |
| G.6 | Continuous monitoring + finality: daily recording of tx counts per type for a week (not just 2 snapshots); separate finality experiment if possible | Activity patterns change across days; finality time can be measured from RPC/Explorer | Tx counts per type per day (7 days); time until a tx is considered final per RPC/Explorer | **Read-only** (monitoring + finality measurement; no transactions) — load testing NOT included (only in a suitable environment, not flooding the public testnet) | Daily workload for a week; finality may not be measurable precisely from public data | Cost: $0. Time: ~15 minutes/day × 7 days + ~1 hour of final analysis | Approve/reject; start date; whether finality is measured at the same time |

## Summary for decision

- **Read-only only (no transactions, no funds at risk):** G.2, G.4, G.6
  (and forwarder observation in G.5).
- **Needs transactions (state changes, testnet gas):** G.1, G.3 (if new
  txs), G.5 (if the bx demo is run).
- **Suggested order (not a decision):** ticket first (Q1–Q10),
  then G.2 + G.4 (read-only, cheap, closing gaps F.1 and proof time),
  then G.1 + G.3 (one transaction package), then G.5 (after the
  ticket Q2 answer), then G.6 (a week of monitoring, can run in parallel).
- **NOT recommended (audit §G.8):** trying to become an
  auditor; concluding anything about Enygma Sovereign from
  the absence of public data; presenting "volume" figures that mix
  different tokens without a decimals caveat.

## Status

- 22 Nov 2026: this table was made as decision material. No
  experiment has been run. The ticket draft is at
  `tickets/rayls-team-questions-draft-2026-11-22.md` (DRAFT, not
  sent; excluded from the current commit batch — a local draft for
  separate revision).
