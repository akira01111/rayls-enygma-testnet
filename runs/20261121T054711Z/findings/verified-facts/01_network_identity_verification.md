# Module 01 - Network Identity Audit: Verification Report

Network: Rayls Enygma Public Testnet
RPC endpoint: https://testnet-rpc.rayls.com
Retrieved at (UTC): 2026-11-21T05:47:11Z
Script: scripts/01_network_identity.py
Python: 3.12.3 (CPython)

## Status: PASS

## Checks

- [PASS] chain_id_matches_expected - expected 7295799 (0x6f5337), observed 7295799 (0x6f5337)
- [PASS] block_number_matches_latest_block - eth_blockNumber=24800203, latest.number=24800204, drift=+1 blocks
- [PASS] latest_block_has_hash - hash=0x7c1ffb4e9dfb5eb64869e071c7a3f2ba0ffb01e894985c93ed9b3e0b90c3dee5
- [PASS] latest_block_timestamp_valid - timestamp=0x6b013062 (2026-11-21T05:47:14Z)
- [PASS] genesis_block_is_zero - genesis.number=0
- [PASS] genesis_block_has_hash - hash=0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545
- [PASS] latest_block_after_genesis - latest=24800204, genesis=0
- [PASS] latest_block_not_before_baseline - latest=24800204, baseline=24793989 at 2026-11-21T04:50:45Z
- [PASS] all_rpc_calls_succeeded - 4/4 calls OK

## Observed values

- Chain ID: 7295799 (0x6f5337); expected 7295799 (0x6f5337)
- Latest block: 24800204 (0x17a6bcc)
- Latest block hash: 0x7c1ffb4e9dfb5eb64869e071c7a3f2ba0ffb01e894985c93ed9b3e0b90c3dee5
- Latest block timestamp (UTC): 2026-11-21T05:47:14Z
- Genesis hash: 0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545
- Genesis timestamp (UTC): 2026-03-12T16:22:30Z

## Comparison with the previous audit

- Previous audit (21 Nov 2026, 04:50:45 UTC): chain ID 7295799, latest block 24793989.
- This run: chain ID 7295799, latest block 24800204 (delta +6215 blocks).
- Chain ID matches the previous audit: yes.

## Files and SHA256

- raw-data/rpc-responses/01_network_identity_raw.json - 2131d69031ca3b8e085004a807e8ebd169780c12c25b68afd1c0f3e8124fb85c
- datasets/01_network_identity_metadata.json - 8d4e60119fce820f605007684ac834c3f50e1e1523d8a470a43405578620208f
- datasets/01_network_identity.csv - 156c0b719499d212f3ba096c38b188c669463f6fd0069cf42b34aaadc4db9282

## Limitations

- Read-only RPC calls only. Nothing here proves anything about the demo, the relayer, or contract behaviour.
- On a live chain, eth_blockNumber and eth_getBlockByNumber(latest) are read seconds apart, so the check allows the latest block to be up to 10 blocks ahead of the blockNumber read, and never behind.
- The RPC connection can drop mid-response through this VM's egress proxy (observed: RemoteDisconnected / IncompleteRead via urllib; the same call succeeds via curl). The script retries each call up to 5 times on a fresh connection and records the attempt count per call in the raw file.
- The genesis block is read from the same RPC endpoint; an independent archive source was not cross-checked.
- Block timestamps are the values reported by the chain, not independently measured wall-clock times.
- A PASS here means network identity is consistent at retrieval time; it does not verify any other module.
