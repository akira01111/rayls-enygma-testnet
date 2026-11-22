# contracts

Contract ABIs, source code references, and deployment configuration for the
Rayls Enygma Public Testnet.

Rules:

- Every entry records the contract address in full, the chain ID, the source
  link, and whether the source is verified or unverified.
- Proxy, implementation, registry, and vault addresses are recorded
  separately — a proxy address is not an implementation address.
- Deployment files are stored as found; the date and source of each file
  are noted.

## token-flows

(Moved here verbatim from the former `contracts/token-flows/README.md`
during the Phase 1 restructure, 22 Nov 2026; the folder was removed
after the move.)

Documentation of how tokens move through the Enygma system.

A token flow must keep four things separate:

1. **Main transaction** — the transaction that starts the flow.
2. **Destination contract address** — which contract the call was sent to.
3. **Token recipient from the Transfer event** — the actual recipient on record, which may differ from the address that was called.
4. **Balance changes** — before/after balances per address, from observable state only.

These four are never merged into a single number, and the same movement is never counted twice. Shielded amounts that cannot be observed are recorded as unobservable, not estimated.

## interactions

(Moved here verbatim from the former `contracts/interactions/README.md`
during the Phase 1 restructure, 22 Nov 2026; the folder was removed
after the move.)

Records of how the contracts call each other during a flow — which contract a call touches, and in what order.

Based on source code and observed transactions only. A call path that has not been seen in code or in a transaction is not written here.
