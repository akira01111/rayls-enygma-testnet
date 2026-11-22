# Transaction audit: `0x09edab2b...`

This package records the Week 2 private-payment transaction at block `24825928`. The map below links saved RPC and Explorer responses to decoded records, derived tables, scripts, the manifest, and audit notes.

## Package map

| Evidence layer | Location | Contents |
|---|---|---|
| Raw evidence | [`raw/`](raw/) | Saved RPC and Explorer response envelopes. Treat as immutable inputs. |
| Decoded data | [`decoded/`](decoded/) | ABI-based event and calldata parsing, signature lookups, and the audit summary. The ABI came from the client bundle, not verified deployed source. |
| Derived tables | [`datasets/`](../../../datasets/) | CSVs built from this and other saved inputs; see the [dataset guide](../../../datasets/README.md). |
| Fetch, decode, verify | [`scripts/`](../../../scripts/) | Shared scripts: [fetch](../../../scripts/tx_audit_09edab2b.py), [decode](../../../scripts/decode_tx_09edab2b.py), and [transaction verifier](../../../scripts/verify_tx_audit_09edab2b.py). |
| Manifest | [`manifest.json`](manifest.json) | Package file list, byte counts, and SHA-256 values. The README and review PDF are not manifest payload entries. |
| Reports and interpretation | [TX audit report](TX-AUDIT-REPORT.md), [gaps](gaps.md), [TODO](TODO.md), [addendum](ADDENDUM-2026-11-22.md) | Audit results, unresolved questions, follow-up, and dated correction. Follow the [r3 article audit](../../testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-r3.md) and [F17 addendum](../../testnet-journeys/week2-private-payment/ARTICLE-AUDIT-2026-11-22-addendum-f17.md) for the governing classifications. |

## Verify

From the repository root:

```sh
python3 scripts/verify_tx_audit_09edab2b.py
python3 datasets/verify_datasets.py
```

The transaction verifier v1.0.1 reads from `~/workspace/rayls-enygma-public-testnet-research` rather than resolving the checkout from its own file; the [reproduction guide](../../../REPRODUCE.md) uses that path. The dataset verifier is repository-relative and checks the derived CSVs, their checksums, and the TX and journey manifests. These integrity checks do not prove interpretations. Re-fetching and decoding steps are also in the reproduction guide.

## Data limits

The seven event topics and the transaction selector match signatures in the client-side demo ABI. No verified source is available for the deployed vault implementation, so these matches do not establish its internal behavior. Preserve the distinctions in the governing audit: statement word 8's integer wei value is a verified fact, its RLS unit is an interpretation, and the meaning "total fee" is an inference.
