# Module 01 - Network Identity Audit: Verification Report

Network: Rayls Enygma Public Testnet
RPC endpoint: https://testnet-rpc.rayls.com
Run ID: 20261121T063327Z
Run directory: runs/20261121T063327Z
Retrieved at (UTC): 2026-11-21T06:33:27Z
Script: scripts/01_network_identity.py (version 2.0.1)
Script copy in this run: runs/20261121T063327Z/scripts/01_network_identity.py
Python: 3.12.3 (CPython)

## Status: PASS (13/13 checks)

## Checks

- [PASS] response_valid_eth_chainId - valid
- [PASS] response_valid_eth_blockNumber - valid
- [PASS] response_valid_eth_getBlockByNumber_latest - valid
- [PASS] response_valid_eth_getBlockByNumber_genesis - valid
- [PASS] chain_id_matches_expected - expected 7295799 (0x6f5337), observed 7295799 (0x6f5337)
- [PASS] block_number_within_drift_of_latest_block - eth_blockNumber=24805299, latest.number=24805303, drift=+4 blocks (allowed 0..+10, never behind)
- [PASS] latest_block_has_hash - hash=0x48879b00f91a76d111150506f736d3e424c43aa4d3b901b2d744efa52ff1c149
- [PASS] latest_block_timestamp_valid - timestamp=0x6b013b3e (2026-11-21T06:33:34Z)
- [PASS] genesis_block_is_zero - genesis.number=0
- [PASS] genesis_block_has_hash - hash=0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545
- [PASS] latest_block_after_genesis - latest=24805303, genesis=0
- [PASS] latest_block_not_before_baseline - latest=24805303, baseline=24793989 at 2026-11-21T04:50:45Z
- [PASS] all_rpc_calls_succeeded - 4/4 calls OK

## Observed values

- Chain ID: 7295799 (0x6f5337); expected 7295799 (0x6f5337)
- Latest block: 24805303 (0x17a7fb7)
- Latest block hash: 0x48879b00f91a76d111150506f736d3e424c43aa4d3b901b2d744efa52ff1c149
- Latest block timestamp (UTC): 2026-11-21T06:33:34Z
- Genesis hash: 0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545
- Genesis timestamp (UTC): 2026-03-12T16:22:30Z

## Comparison with the previous audit

- Previous audit (21 Nov 2026, 04:50:45 UTC): chain ID 7295799, latest block 24793989.
- This run: chain ID 7295799, latest block 24805303 (delta +11314 blocks).
- Chain ID matches the previous audit: yes.

## Files and SHA256

- raw-data/rpc-responses/01_network_identity_raw.json - 05609b3cd546a248f9079ce24e3bdec281b60712a7eefa4d7dc610cec72dcc3a
- datasets/01_network_identity_metadata.json - e0c3f06cb508484d5290656e4484c638c34ec772f657d8c83a3241053611f9e4
- datasets/01_network_identity.csv - 9350c65a7f0523d4e91dc3c1d3187e056c94d35ecbdcb6dcb88c509125142ef4
- scripts/01_network_identity.py (copy of the script that ran) - 5ff78700346b2ebd0c1a1e14c2f615b3fd4d422bb7cbbec489b3d48743260ae0

The checksum manifest datasets/01_network_identity_checksums.sha256 also covers this report itself.

## Limitations

- Read-only RPC calls only. Nothing here proves anything about the demo, the relayer, or contract behaviour.
- Response validation: every RPC response is checked for JSON-RPC version 2.0, a response id matching the request id, no RPC error object, and a well-formed result (hex string for eth_chainId / eth_blockNumber; block object with number, hash, and timestamp for eth_getBlockByNumber). A response that fails any of these makes its response_valid_* check FAIL with the exact problem recorded; it never crashes the run.
- The raw JSON file is a captured-and-serialized response structure (request object + parsed JSON response + transport metadata), not a byte-level HTTP capture: no raw HTTP bytes, headers, or TLS data are stored.
- On a live chain, eth_blockNumber and eth_getBlockByNumber(latest) are read seconds apart, so the check block_number_within_drift_of_latest_block allows the latest block to be up to 10 blocks ahead of the blockNumber read, and never behind. The two numbers are not required to be exactly equal.
- The RPC connection can drop mid-response through this VM's egress proxy (observed: RemoteDisconnected / IncompleteRead via urllib; the same call succeeds via curl). The script retries each call up to 5 times on a fresh connection and records the attempt count per call in the raw file.
- The genesis block is read from the same RPC endpoint; an independent archive source was not cross-checked.
- Block timestamps are the values reported by the chain, not independently measured wall-clock times.
- A PASS here means network identity is consistent at retrieval time; it does not verify any other module.
- This run's outputs live in runs/20261121T063327Z/ and are never overwritten: the script refuses to reuse an existing run directory and creates every file in exclusive mode.
