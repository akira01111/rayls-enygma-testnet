# scripts

Audit and reproduction scripts: read-only RPC queries, log parsing, and checks
that let anyone reproduce a number in this repository.

Rules:

- Scripts are read-only. They never send transactions, sign anything, or
  change on-chain state.
- Each script records the tool and client versions it was run with.
- A script that needs a secret or a private key does not belong here.

## Scripts in this repository

- `01_network_identity.py` (v2.0.1) — Module 01: network identity audit.
- `tx_audit_09edab2b.py` (v1.1.0) — Week 2 TX audit: raw fetch via curl.
- `decode_tx_09edab2b.py` (v1.0.0) — Week 2 TX audit: decode + summary
  (no network; reads raw files only).
- `verify_tx_audit_09edab2b.py` (v1.0.1) — Week 2 TX audit: independent
  verification (re-reads evidence, recomputes SHA-256, checks the manifest).
