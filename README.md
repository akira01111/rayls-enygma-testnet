# Rayls Enygma public testnet research

The research examines Rayls Enygma Public Testnet deployment details, public on-chain activity, and testnet experiments. Findings are labeled as verified facts, official claims, direct observations, reconstructions, inferences, or unknowns.

## Research question

What can the public actually see when two accounts make a private transfer on Rayls Enygma?

## Start here

- [Index](INDEX.md): browse the evidence, datasets, audit packages, open questions, and file history.
- [Reproduction guide](REPRODUCE.md): verify the saved packages or repeat the read-only checks.
- [Research trail](RESEARCH-TRAIL.md): chronological account of the work and unresolved questions.

## Network

- Chain: Rayls Enygma Public Testnet
- Chain ID: `7295799` (`0x6f5337`)
- RPC: https://testnet-rpc.rayls.com
- Explorer: https://testnet-explorer.rayls.com

## Current findings

The latest interpretation of the Week 2 private-payment experiment is in the [r3 article audit](experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r3.md) and [F17 addendum](experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-addendum-f17.md). Those documents govern when earlier classifications differ.

| Finding | Evidence-based summary |
|---|---|
| Transaction | `0x09edab2b...25bb`, block `24825928`; one transaction in the block. |
| Sender and destination | The transaction was sent by relayer `0xa5f0c684...0ac8` to SharedVaultProxy `0x9c5ad5e5...06c2`. The implementation source is not verified. |
| Logs | Seven logs came from the vault proxy: one Nullifier, three Commitment, and three EncryptedNote topics. These names are signature matches, not verified source declarations. |
| Statement word 8 | Integer `4,416,000,000,000,000,000` wei = verified fact; the RLS unit = interpretation; the meaning "total fee" = inference. |
| Chain gas | `0.063168048` native units, derived from gas used and the effective gas price. The token identity is unresolved (RLS or USDr). |
| Related transfer | A separate `0.576 RLS` transfer appears four blocks later. Its recipient identity and purpose are unknown. |
| Account association | The link between this transaction, `@anara`, and `@kittynim` is a reconstruction from experiment context; the chain does not establish that link. |

## Research method

On-chain observations came from read-only JSON-RPC and Explorer queries. Fetch scripts save request and response structures as provenance records, not byte-for-byte HTTP captures. The transaction decoder reads those saved files and the client-side demo ABI, then matches the function selector and event topics. These signature matches do not verify the deployed contracts' internal logic.

The [r3 audit](experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r3.md) and [F17 addendum](experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-addendum-f17.md) govern finding classifications.

## Primary sources

- [Rayls testnet JSON-RPC](https://testnet-rpc.rayls.com) and [Rayls testnet Explorer](https://testnet-explorer.rayls.com/) are the on-chain data endpoints used by the fetch scripts.
- [Enygma Public testnet app](https://enygma-testnet.rayls.com/) is the source of the client-side ABI extraction stored at `experiments/transactions/tx-09edab2b/decoded/bundle-abi-extract.json`. It is not verified contract source.
- [Try Enygma Public on testnet](https://docs.rayls.com/docs/try-enygma-public-on-testnet) and [How Enygma Public works](https://docs.rayls.com/docs/how-enygma-public-works) are official documentation (accessed 22 Nov 2026) and describe Rayls' claims. They do not establish what the examined transaction did beyond what the on-chain evidence shows.

## Verify the saved evidence

Run from the repository root:

```sh
python3 datasets/verify_datasets.py  # dataset verifier
python3 scripts/verify_tx_audit_09edab2b.py  # transaction verifier
```

The [dataset verifier](datasets/verify_datasets.py) independently derives the CSVs, checks fields in `audit_report.json` against the sources, and checks the manifests and checksums. The separate [transaction verifier](scripts/verify_tx_audit_09edab2b.py) checks the raw and decoded transaction package. The recorded results are 9/9 and 23/23 checks, respectively; these confirm integrity and internal consistency, not interpretations. Verifier v1.0.1 expects the checkout at `~/workspace/rayls-enygma-public-testnet-research`; the dataset verifier resolves the repository relative to its own file. See the [reproduction guide](REPRODUCE.md) for the procedure and limits.

## Repository map

- [Index](INDEX.md) - complete file guide, provenance, status, and path history.
- [Research trail](RESEARCH-TRAIL.md) - chronological work log and open questions.
- [Reproduction guide](REPRODUCE.md) - commands and reproduction limits.
- [Audit reports](audit-reports/) - initial audit report and provenance note.
- [Transaction package guide](experiments/transactions/tx-09edab2b/README.md) - map of the raw responses, decoded data, derived datasets, scripts, manifest, and reports.
- [Week 2 journey](experiments/testnet-journeys/week2-private-payment/) - public video files and the governing article audit.
- [Datasets](datasets/) - derived CSVs, build and verification scripts, and checksums.
- [Runs](runs/) - Network Identity Audit evidence and run notes.
- [Contracts](contracts/) - addresses, ABIs, and verified-source status.
- [Raw data](raw-data/) - captured screenshots and public video assets.
- [Scripts](scripts/) - audit and reproduction scripts.
- [Findings](findings/) - classification rules.

## Scope and limitations

This repository does not establish the identity of `0x71af...`, the purpose of the related `0.576 RLS` transfer, the meaning of statement words `[0]`, `[1]`, `[2]`, and `[9]`, the contents of encrypted notes, or the deployed vault implementation's source code. It also does not establish whether the relayer's displayed "0.58 Rayls Foundation (15%)" fee corresponds to that transfer. Selective auditing on this deployment could not be independently verified in the initial audit. See the [governing interpretation](experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r3.md), the [F17 addendum](experiments/testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-addendum-f17.md), and [open questions](RESEARCH-TRAIL.md) for detail.

## Public snapshot

The public `main` branch points to `deb3d09` ("Restructure repo presentation (Phase 1)", 22 Nov 2026).
