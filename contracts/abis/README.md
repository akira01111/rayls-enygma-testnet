# abis

ABI files for the contracts listed in `../addresses/`.

Each ABI records the contract it belongs to, where it came from (verified
source, official docs, or generated from source code), and the date it was
added.

## Current ABIs

No ABI file is stored in this folder. The only ABI in this repository is the
demo-bundle extract used by the Week 2 TX audit:
`experiments/transactions/tx-09edab2b/decoded/bundle-abi-extract.json`
(IEnygmaDvp entries incl. transferV2, extracted from the demo bundle
`assets/index-Dlv-HYaZ.js`, bundle SHA-256 `7530bbc2…`). It is deliberately
NOT duplicated here — the TX package is its canonical home. Note: this ABI
comes from the demo app's client-side code, not from verified on-chain
source.
