# addresses

Contract addresses used by the Enygma Public Testnet deployment: proxy,
implementation, registry, vault, and token contracts.

Each entry records the full address, the chain ID, the contract's role, and
the source where the address was found. No address is written from memory —
only from a source that was actually checked.

## addresses.json

`addresses.json` (this folder) is the machine-readable contract map,
extracted verbatim from the initial audit report
(`audit-reports/ENYGMA-TESTNET-AUDIT-REPORT.md`, §C.2/C.3, 21 Nov 2026):
yx + bx deployments, EIP-1967 implementation slots, auditor/relayer/
Multicall3/forwarder/EnygmaDvp, and the unknown-provenance address
`0xd908…`. Every address in it was checked to appear in the audit report.
The bx live implementations do not match the bundle — see the file's notes.
