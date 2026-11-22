# Module 01 - Network Identity Audit: Verification Report

Network: Rayls Enygma Public Testnet
RPC endpoint: https://testnet-rpc.rayls.com
Run ID: 20261121T063234Z
Run directory: runs/20261121T063234Z
Retrieved at (UTC): 2026-11-21T06:32:34Z
Script: scripts/01_network_identity.py (version 2.0.1)
Script copy in this run: runs/20261121T063234Z/scripts/01_network_identity.py
Python: 3.12.3 (CPython)

## Status: PASS (13/13 checks)

## Checks

- [PASS] response_valid_eth_chainId - valid
- [PASS] response_valid_eth_blockNumber - valid
- [PASS] response_valid_latest - valid
- [PASS] response_valid_genesis - valid
- [PASS] chain_id_matches_expected - expected 7295799 (0x6f5337), observed 7295799 (0x6f5337)
- [PASS] block_number_within_drift_of_latest_block - eth_blockNumber=24805202, latest.number=24805207, drift=+5 blocks (allowed 0..+10, never behind)
- [PASS] latest_block_has_hash - hash=0x59329e11eb786abbfaf52c7107e4f8f9051910b9c0c046a117c25db8237da8fe
- [PASS] latest_block_timestamp_valid - timestamp=0x6b013b0a (2026-11-21T06:32:42Z)
- [PASS] genesis_block_is_zero - genesis.number=0
- [PASS] genesis_block_has_hash - hash=0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545
- [PASS] latest_block_after_genesis - latest=24805207, genesis=0
- [PASS] latest_block_not_before_baseline - latest=24805207, baseline=24793989 at 2026-11-21T04:50:45Z
- [PASS] all_rpc_calls_succeeded - 4/4 calls OK

## Observed values

- Chain ID: 7295799 (0x6f5337); expected 7295799 (0x6f5337)
- Latest block: 24805207 (0x17a7f57)
- Latest block hash: 0x59329e11eb786abbfaf52c7107e4f8f9051910b9c0c046a117c25db8237da8fe
- Latest block timestamp (UTC): 2026-11-21T06:32:42Z
- Genesis hash: 0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545
- Genesis timestamp (UTC): 2026-03-12T16:22:30Z

## Comparison with the previous audit

- Previous audit (21 Nov 2026, 04:50:45 UTC): chain ID 7295799, latest block 24793989.
- This run: chain ID 7295799, latest block 24805207 (delta +11218 blocks).
- Chain ID matches the previous audit: yes.

## Files and SHA256

- raw-data/rpc-responses/01_network_identity_raw.json - 6ac45acd0c4557b3cc44c493412b00ea3ad9a88416deb693a9f6e73e59df39f9
- datasets/01_network_identity_metadata.json - 0ad82212446486a2f87a35767af1c18f668fdfc9a007f8f969668eb83a77a047
- datasets/01_network_identity.csv - 458684c3d612271ea4259b7b55b3c955ed661d2f22d4c3e6063f170061181078
- scripts/01_network_identity.py (copy of the script that ran) - c09d88eb835ba69d9a6bf4ee8d976584a709b97d140fd379b39385f5050701e0

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
- This run's outputs live in runs/20261121T063234Z/ and are never overwritten: the script refuses to reuse an existing run directory and creates every file in exclusive mode.
