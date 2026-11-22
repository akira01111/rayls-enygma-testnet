# Module 01 - Network Identity Audit: Complete File

Network: Rayls Enygma Public Testnet
RPC endpoint: https://testnet-rpc.rayls.com
Run ID: 20261121T054711Z
Retrieved at (UTC): 2026-11-21T05:47:11Z
Script version that produced this run: 1.0.0 (before the no-overwrite fix; the exact code is preserved in runs/20261121T054711Z/scripts/01_network_identity.py)
Status: **PASS (9/9 checks)**

## Note about this file

This file is a **combined copy for reading** — it contains the code, terminal output, raw JSON, metadata, checksums, dataset, and verification report of Module 01 in a single document.
The authoritative evidence remains the **6 separate files** in this run directory (see the list below), because:
- raw data must stand on its own so it cannot be changed undetected — a SHA256 checksum is only meaningful if the raw file is separate and untouched;
- the script must be a `.py` file so it can be re-run as-is;
- if everything were merged into a single editable file, one typo fix in the report section would change the hash of the whole file, and the raw data could no longer be proven unchanged.
So: this file is for reading and review; the 6 separate files remain the official evidence.

Relocation note (21 Nov 2026 ~12:55 WIB): this run's evidence was originally written to the canonical locations (raw-data/, datasets/, findings/) by script v1.0.0, then moved byte-identically to runs/20261121T054711Z/ when the script was fixed to v2.0.0 (no-overwrite layout). All SHA256 values were verified identical before and after the move. The observed content was not changed. The raw JSON and the script copy in this run are read-only (chmod 444). This run's metadata does not yet record run_id/script_version because it was created by script v1.0.0 before those fields existed — the run ID and script version for this run are recorded here and in runs/README.md.

Evidence files (run 20261121T054711Z):
- runs/20261121T054711Z/scripts/01_network_identity.py (v1.0.0, byte-identical copy of the script that ran this run)
- runs/20261121T054711Z/raw-data/rpc-responses/01_network_identity_raw.json
- runs/20261121T054711Z/datasets/01_network_identity.csv
- runs/20261121T054711Z/datasets/01_network_identity_metadata.json
- runs/20261121T054711Z/datasets/01_network_identity_checksums.sha256
- runs/20261121T054711Z/findings/verified-facts/01_network_identity_verification.md

## 1. Summary of results

- Chain ID: 7295799 (0x6f5337) — matches the previous audit.
- Latest block: 24800204 (0x17a6bcc), hash 0x7c1ffb4e9dfb5eb64869e071c7a3f2ba0ffb01e894985c93ed9b3e0b90c3dee5, timestamp 2026-11-21T05:47:14Z — up +6215 blocks from baseline 24793989 (21 Nov 04:50:45 UTC).
- Genesis hash: 0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545, timestamp 2026-03-12T16:22:30Z (new data, not present in the previous audit).
- The latest block fetched is empty (0 transactions).
- Run 1 initially FAILED (eth_chainId connection dropped 3x + block check too strict), fixed (retry 5x + 10-block drift tolerance), run 2 PASS.

## 2. Verification report

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

## 3. Output terminal (run 2)

```
module: 01_network_identity
rpc: https://testnet-rpc.rayls.com
retrieved_at_utc: 2026-11-21T05:47:11Z
chain_id: 7295799 (0x6f5337)
latest_block: 24800204 (0x17a6bcc)
latest_block_hash: 0x7c1ffb4e9dfb5eb64869e071c7a3f2ba0ffb01e894985c93ed9b3e0b90c3dee5
latest_block_timestamp_utc: 2026-11-21T05:47:14Z
genesis_hash: 0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545
genesis_block_timestamp_utc: 2026-03-12T16:22:30Z
status: PASS
check chain_id_matches_expected: PASS (expected 7295799 (0x6f5337), observed 7295799 (0x6f5337))
check block_number_matches_latest_block: PASS (eth_blockNumber=24800203, latest.number=24800204, drift=+1 blocks)
check latest_block_has_hash: PASS (hash=0x7c1ffb4e9dfb5eb64869e071c7a3f2ba0ffb01e894985c93ed9b3e0b90c3dee5)
check latest_block_timestamp_valid: PASS (timestamp=0x6b013062 (2026-11-21T05:47:14Z))
check genesis_block_is_zero: PASS (genesis.number=0)
check genesis_block_has_hash: PASS (hash=0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545)
check latest_block_after_genesis: PASS (latest=24800204, genesis=0)
check latest_block_not_before_baseline: PASS (latest=24800204, baseline=24793989 at 2026-11-21T04:50:45Z)
check all_rpc_calls_succeeded: PASS (4/4 calls OK)
sha256 raw: 2131d69031ca3b8e085004a807e8ebd169780c12c25b68afd1c0f3e8124fb85c
sha256 metadata: 8d4e60119fce820f605007684ac834c3f50e1e1523d8a470a43405578620208f
sha256 dataset: 156c0b719499d212f3ba096c38b188c669463f6fd0069cf42b34aaadc4db9282
EXIT_CODE=0
```

## 4. Metadata JSON

```json
{
  "module": "01_network_identity",
  "network": "Rayls Enygma Public Testnet",
  "rpc_endpoint": "https://testnet-rpc.rayls.com",
  "chain_id": 7295799,
  "chain_id_hex": "0x6f5337",
  "expected_chain_id": 7295799,
  "latest_block": 24800204,
  "latest_block_hash": "0x7c1ffb4e9dfb5eb64869e071c7a3f2ba0ffb01e894985c93ed9b3e0b90c3dee5",
  "latest_block_timestamp_utc": "2026-11-21T05:47:14Z",
  "genesis_hash": "0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545",
  "genesis_block_timestamp_utc": "2026-03-12T16:22:30Z",
  "baseline_block": 24793989,
  "baseline_block_at_utc": "2026-11-21T04:50:45Z",
  "retrieved_at_utc": "2026-11-21T05:47:11Z",
  "python_version": "3.12.3",
  "python_implementation": "CPython",
  "script": "scripts/01_network_identity.py",
  "status": "PASS"
}
```

## 5. SHA256 checksums

```
2131d69031ca3b8e085004a807e8ebd169780c12c25b68afd1c0f3e8124fb85c  01_network_identity_raw.json
8d4e60119fce820f605007684ac834c3f50e1e1523d8a470a43405578620208f  01_network_identity_metadata.json
156c0b719499d212f3ba096c38b188c669463f6fd0069cf42b34aaadc4db9282  01_network_identity.csv
```

## 6. Dataset CSV

```csv
retrieved_at_utc,rpc_endpoint,chain_id,chain_id_hex,latest_block,latest_block_hash,latest_block_timestamp_utc,genesis_block_hash,genesis_block_timestamp_utc,status
2026-11-21T05:47:11Z,https://testnet-rpc.rayls.com,7295799,0x6f5337,24800204,0x7c1ffb4e9dfb5eb64869e071c7a3f2ba0ffb01e894985c93ed9b3e0b90c3dee5,2026-11-21T05:47:14Z,0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545,2026-03-12T16:22:30Z,PASS
```

## 7. Raw JSON (copy — original file: runs/20261121T054711Z/raw-data/rpc-responses/01_network_identity_raw.json)

```json
{
  "module": "01_network_identity",
  "network": "Rayls Enygma Public Testnet",
  "rpc_endpoint": "https://testnet-rpc.rayls.com",
  "retrieved_at_utc": "2026-11-21T05:47:11Z",
  "calls": [
    {
      "method": "eth_chainId",
      "params": [],
      "request": {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_chainId",
        "params": []
      },
      "retrieved_at_utc": "2026-11-21T05:47:11Z",
      "http_status": 200,
      "response": {
        "jsonrpc": "2.0",
        "id": 1,
        "result": "0x6f5337"
      },
      "error": null,
      "attempts": 1
    },
    {
      "method": "eth_blockNumber",
      "params": [],
      "request": {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "eth_blockNumber",
        "params": []
      },
      "retrieved_at_utc": "2026-11-21T05:47:12Z",
      "http_status": 200,
      "response": {
        "jsonrpc": "2.0",
        "id": 2,
        "result": "0x17a6bcb"
      },
      "error": null,
      "attempts": 1
    },
    {
      "method": "eth_getBlockByNumber",
      "params": [
        "latest",
        false
      ],
      "request": {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "eth_getBlockByNumber",
        "params": [
          "latest",
          false
        ]
      },
      "retrieved_at_utc": "2026-11-21T05:47:13Z",
      "http_status": 200,
      "response": {
        "jsonrpc": "2.0",
        "id": 3,
        "result": {
          "hash": "0x7c1ffb4e9dfb5eb64869e071c7a3f2ba0ffb01e894985c93ed9b3e0b90c3dee5",
          "parentHash": "0xfc5e203d287767b5dd96f1a51e55f5e9dc262311643fe33147d8acde16b7ca94",
          "sha3Uncles": "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
          "miner": "0xcf25e900fdb7523e4c81466d9c453cfdddb4a0ee",
          "stateRoot": "0x8ec032638838b139b87a5ae32c6b778d7bd102abeb14521c09e3b4b5ac429053",
          "transactionsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
          "receiptsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
          "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
          "difficulty": "0x0",
          "number": "0x17a6bcc",
          "gasLimit": "0x1dcd6500",
          "gasUsed": "0x0",
          "timestamp": "0x6b013062",
          "extraData": "0x",
          "mixHash": "0x9df252cadf2e30c59f774b35a94d73d6e37a4781d343f81d4955bb4272698579",
          "nonce": "0x000000fc0003fe8e",
          "baseFeePerGas": "0xb2d05e000",
          "withdrawalsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
          "blobGasUsed": "0x0",
          "excessBlobGas": "0x0",
          "parentBeaconBlockRoot": "0x9df252cadf2e30c59f774b35a94d73d6e37a4781d343f81d4955bb4272698579",
          "requestsHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
          "size": "0x26d",
          "uncles": [],
          "transactions": [],
          "withdrawals": []
        }
      },
      "error": null,
      "attempts": 1
    },
    {
      "method": "eth_getBlockByNumber",
      "params": [
        "0x0",
        false
      ],
      "request": {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "eth_getBlockByNumber",
        "params": [
          "0x0",
          false
        ]
      },
      "retrieved_at_utc": "2026-11-21T05:47:14Z",
      "http_status": 200,
      "response": {
        "jsonrpc": "2.0",
        "id": 4,
        "result": {
          "hash": "0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545",
          "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
          "sha3Uncles": "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347",
          "miner": "0x0000000000000000000000000000000000000000",
          "stateRoot": "0x8f1fea565bb21693c4ad99a892c2720cdc7f7f0cbab7380d0313c6696ac47f6d",
          "transactionsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
          "receiptsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
          "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
          "difficulty": "0x0",
          "number": "0x0",
          "gasLimit": "0x1c9c380",
          "gasUsed": "0x0",
          "timestamp": "0x69b2e846",
          "extraData": "0x",
          "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
          "nonce": "0x0000000000000000",
          "baseFeePerGas": "0x7",
          "withdrawalsRoot": "0x56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421",
          "blobGasUsed": "0x0",
          "excessBlobGas": "0x0",
          "parentBeaconBlockRoot": "0x0000000000000000000000000000000000000000000000000000000000000000",
          "requestsHash": "0xe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "size": "0x264",
          "uncles": [],
          "transactions": [],
          "withdrawals": []
        }
      },
      "error": null,
      "attempts": 2
    }
  ]
}
```

## 8. Complete Python code (copy — original file: runs/20261121T054711Z/scripts/01_network_identity.py, v1.0.0)

```python
#!/usr/bin/env python3
"""Module 01 - Network Identity Audit: Rayls Enygma Public Testnet.

Read-only JSON-RPC checks using the Python standard library only.
No private key, no wallet, no API secret, no third-party library.

Calls made:
  - eth_chainId
  - eth_blockNumber
  - eth_getBlockByNumber (latest, full transactions = false)
  - eth_getBlockByNumber (genesis, block 0x0, full transactions = false)

Outputs, all relative to the repository root (the parent of scripts/):
  - raw-data/rpc-responses/01_network_identity_raw.json
  - datasets/01_network_identity.csv
  - datasets/01_network_identity_metadata.json
  - datasets/01_network_identity_checksums.sha256
  - findings/verified-facts/01_network_identity_verification.md

Exit code: 0 when every check passes (PASS), 1 otherwise (FAIL).
Raw data is written exactly as received and is never modified afterwards.
"""

import csv
import hashlib
import http.client
import json
import platform
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RPC_URL = "https://testnet-rpc.rayls.com"
EXPECTED_CHAIN_ID = 7295799
EXPECTED_CHAIN_ID_HEX = "0x6f5337"
# Latest block observed in the previous audit (21 Nov 2026, 04:50:45 UTC).
# Used only as a sanity floor: the chain must not go backwards.
BASELINE_BLOCK = 24793989
BASELINE_BLOCK_AT_UTC = "2026-11-21T04:50:45Z"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
TIMEOUT_SECONDS = 30

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = REPO_ROOT / "raw-data" / "rpc-responses" / "01_network_identity_raw.json"
DATASET_PATH = REPO_ROOT / "datasets" / "01_network_identity.csv"
METADATA_PATH = REPO_ROOT / "datasets" / "01_network_identity_metadata.json"
CHECKSUMS_PATH = REPO_ROOT / "datasets" / "01_network_identity_checksums.sha256"
REPORT_PATH = REPO_ROOT / "findings" / "verified-facts" / "01_network_identity_verification.md"


def utc_now_iso():
    """Current UTC time as ISO 8601 with a Z suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def block_timestamp_iso(hex_timestamp):
    """Convert a hex block timestamp to UTC ISO 8601."""
    return datetime.fromtimestamp(int(hex_timestamp, 16), tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def rpc_call(method, params, call_id):
    """One read-only JSON-RPC call, retried on a fresh connection.

    The RPC endpoint can cut a chunked response mid-body
    (http.client.IncompleteRead). Each attempt opens a new connection.
    Returns (record, error_or_None).
    """
    request = {"jsonrpc": "2.0", "id": call_id, "method": method, "params": params}
    body = json.dumps(request).encode("utf-8")
    record = {
        "method": method,
        "params": params,
        "request": request,
        "retrieved_at_utc": utc_now_iso(),
        "http_status": None,
        "response": None,
        "error": None,
        "attempts": 0,
    }
    last_error = None
    for attempt in range(1, 6):
        record["attempts"] = attempt
        if attempt > 1:
            time.sleep(1)
        http_request = urllib.request.Request(
            RPC_URL,
            data=body,
            headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
            method="POST",
        )
        try:
            with urllib.request.urlopen(http_request, timeout=TIMEOUT_SECONDS) as resp:
                record["http_status"] = resp.status
                record["response"] = json.loads(resp.read().decode("utf-8"))
            return record, None
        except urllib.error.HTTPError as exc:
            last_error = "HTTPError: %s" % exc
            record["http_status"] = exc.code
        except (
            urllib.error.URLError,
            http.client.HTTPException,
            ValueError,
            UnicodeDecodeError,
            TimeoutError,
            OSError,
        ) as exc:
            last_error = "%s: %s" % (type(exc).__name__, exc)
    record["error"] = "failed after %d attempts: %s" % (record["attempts"], last_error)
    return record, record["error"]


def result_of(record):
    """Extract the 'result' field of a call, or None when the call failed."""
    if record["error"] is not None:
        return None
    response = record["response"] or {}
    if "error" in response:
        return None
    return response.get("result")


def sha256_hex(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=False)
        handle.write("\n")


def main():
    retrieved_at_utc = utc_now_iso()
    calls = []
    errors = []

    for call_id, (method, params) in enumerate(
        [
            ("eth_chainId", []),
            ("eth_blockNumber", []),
            ("eth_getBlockByNumber", ["latest", False]),
            ("eth_getBlockByNumber", ["0x0", False]),
        ],
        start=1,
    ):
        record, error = rpc_call(method, params, call_id)
        calls.append(record)
        if error is not None:
            errors.append("%s: %s" % (method, error))
        elif "error" in (record["response"] or {}):
            errors.append("%s: RPC error %s" % (method, record["response"]["error"]))

    # Raw request/response pairs, exactly as sent and received.
    raw = {
        "module": "01_network_identity",
        "network": "Rayls Enygma Public Testnet",
        "rpc_endpoint": RPC_URL,
        "retrieved_at_utc": retrieved_at_utc,
        "calls": calls,
    }
    write_json(RAW_PATH, raw)

    chain_id_hex = result_of(calls[0])
    block_number_hex = result_of(calls[1])
    latest_block = result_of(calls[2])
    genesis_block = result_of(calls[3])

    checks = []
    values = {}

    # 1. Chain ID matches the expected value from the previous audit.
    chain_id = int(chain_id_hex, 16) if chain_id_hex else None
    values["chain_id"] = chain_id
    values["chain_id_hex"] = chain_id_hex
    checks.append(
        (
            "chain_id_matches_expected",
            chain_id == EXPECTED_CHAIN_ID and chain_id_hex == EXPECTED_CHAIN_ID_HEX,
            "expected %d (%s), observed %s (%s)"
            % (EXPECTED_CHAIN_ID, EXPECTED_CHAIN_ID_HEX, chain_id, chain_id_hex),
        )
    )

    # 2. eth_blockNumber agrees with the latest block's own number.
    # The chain is live: the two reads happen seconds apart, so the latest
    # block may have advanced between them. The check allows the latest
    # block to be ahead by up to 10 blocks, and never behind.
    block_number = int(block_number_hex, 16) if block_number_hex else None
    latest_number = (
        int(latest_block["number"], 16) if latest_block and latest_block.get("number") else None
    )
    values["latest_block"] = latest_number
    values["latest_block_hex"] = latest_block.get("number") if latest_block else None
    drift = (
        (latest_number - block_number)
        if (latest_number is not None and block_number is not None)
        else None
    )
    checks.append(
        (
            "block_number_matches_latest_block",
            drift is not None and 0 <= drift <= 10,
            "eth_blockNumber=%s, latest.number=%s, drift=+%s blocks"
            % (block_number, latest_number, drift),
        )
    )

    # 3. Latest block carries a well-formed hash.
    latest_hash = latest_block.get("hash") if latest_block else None
    values["latest_block_hash"] = latest_hash
    checks.append(
        (
            "latest_block_has_hash",
            isinstance(latest_hash, str)
            and latest_hash.startswith("0x")
            and len(latest_hash) == 66,
            "hash=%s" % latest_hash,
        )
    )

    # 4. Latest block timestamp is a valid, positive Unix time.
    latest_ts_hex = latest_block.get("timestamp") if latest_block else None
    latest_ts_iso = block_timestamp_iso(latest_ts_hex) if latest_ts_hex else None
    values["latest_block_timestamp_utc"] = latest_ts_iso
    checks.append(
        (
            "latest_block_timestamp_valid",
            latest_ts_iso is not None and int(latest_ts_hex, 16) > 0,
            "timestamp=%s (%s)" % (latest_ts_hex, latest_ts_iso),
        )
    )

    # 5. Genesis block is block 0 and carries a well-formed hash.
    genesis_number = (
        int(genesis_block["number"], 16) if genesis_block and genesis_block.get("number") else None
    )
    genesis_hash = genesis_block.get("hash") if genesis_block else None
    genesis_ts_hex = genesis_block.get("timestamp") if genesis_block else None
    genesis_ts_iso = block_timestamp_iso(genesis_ts_hex) if genesis_ts_hex else None
    values["genesis_block"] = genesis_number
    values["genesis_hash"] = genesis_hash
    values["genesis_block_timestamp_utc"] = genesis_ts_iso
    checks.append(
        (
            "genesis_block_is_zero",
            genesis_number == 0,
            "genesis.number=%s" % genesis_number,
        )
    )
    checks.append(
        (
            "genesis_block_has_hash",
            isinstance(genesis_hash, str)
            and genesis_hash.startswith("0x")
            and len(genesis_hash) == 66,
            "hash=%s" % genesis_hash,
        )
    )

    # 6. Latest block is ahead of genesis.
    checks.append(
        (
            "latest_block_after_genesis",
            latest_number is not None and genesis_number == 0 and latest_number > 0,
            "latest=%s, genesis=%s" % (latest_number, genesis_number),
        )
    )

    # 7. Chain has not gone backwards versus the previous audit's observation.
    checks.append(
        (
            "latest_block_not_before_baseline",
            latest_number is not None and latest_number >= BASELINE_BLOCK,
            "latest=%s, baseline=%d at %s" % (latest_number, BASELINE_BLOCK, BASELINE_BLOCK_AT_UTC),
        )
    )

    # 8. No call failed.
    checks.append(
        ("all_rpc_calls_succeeded", not errors, "; ".join(errors) if errors else "4/4 calls OK")
    )

    passed = all(ok for _, ok, _ in checks)
    status = "PASS" if passed else "FAIL"

    # Processed dataset: one row with the key values (CSV, mainnet-repo pattern).
    dataset_row = {
        "retrieved_at_utc": retrieved_at_utc,
        "rpc_endpoint": RPC_URL,
        "chain_id": chain_id if chain_id is not None else "",
        "chain_id_hex": chain_id_hex or "",
        "latest_block": latest_number if latest_number is not None else "",
        "latest_block_hash": latest_hash or "",
        "latest_block_timestamp_utc": latest_ts_iso or "",
        "genesis_block_hash": genesis_hash or "",
        "genesis_block_timestamp_utc": genesis_ts_iso or "",
        "status": status,
    }
    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATASET_PATH, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(dataset_row.keys()))
        writer.writeheader()
        writer.writerow(dataset_row)

    # Metadata.
    metadata = {
        "module": "01_network_identity",
        "network": "Rayls Enygma Public Testnet",
        "rpc_endpoint": RPC_URL,
        "chain_id": chain_id,
        "chain_id_hex": chain_id_hex,
        "expected_chain_id": EXPECTED_CHAIN_ID,
        "latest_block": latest_number,
        "latest_block_hash": latest_hash,
        "latest_block_timestamp_utc": latest_ts_iso,
        "genesis_hash": genesis_hash,
        "genesis_block_timestamp_utc": genesis_ts_iso,
        "baseline_block": BASELINE_BLOCK,
        "baseline_block_at_utc": BASELINE_BLOCK_AT_UTC,
        "retrieved_at_utc": retrieved_at_utc,
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "script": "scripts/01_network_identity.py",
        "status": status,
    }
    write_json(METADATA_PATH, metadata)

    # SHA256 checksums for raw data and metadata (+ dataset).
    raw_sha = sha256_hex(RAW_PATH)
    metadata_sha = sha256_hex(METADATA_PATH)
    dataset_sha = sha256_hex(DATASET_PATH)
    CHECKSUMS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CHECKSUMS_PATH, "w", encoding="utf-8") as handle:
        handle.write("%s  %s\n" % (raw_sha, RAW_PATH.name))
        handle.write("%s  %s\n" % (metadata_sha, METADATA_PATH.name))
        handle.write("%s  %s\n" % (dataset_sha, DATASET_PATH.name))

    # Verification report.
    lines = []
    lines.append("# Module 01 - Network Identity Audit: Verification Report")
    lines.append("")
    lines.append("Network: Rayls Enygma Public Testnet")
    lines.append("RPC endpoint: %s" % RPC_URL)
    lines.append("Retrieved at (UTC): %s" % retrieved_at_utc)
    lines.append("Script: scripts/01_network_identity.py")
    lines.append("Python: %s (%s)" % (platform.python_version(), platform.python_implementation()))
    lines.append("")
    lines.append("## Status: %s" % status)
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for name, ok, detail in checks:
        lines.append("- [%s] %s - %s" % ("PASS" if ok else "FAIL", name, detail))
    lines.append("")
    lines.append("## Observed values")
    lines.append("")
    lines.append("- Chain ID: %s (%s); expected %d (%s)" % (chain_id, chain_id_hex, EXPECTED_CHAIN_ID, EXPECTED_CHAIN_ID_HEX))
    lines.append("- Latest block: %s (%s)" % (latest_number, values["latest_block_hex"]))
    lines.append("- Latest block hash: %s" % latest_hash)
    lines.append("- Latest block timestamp (UTC): %s" % latest_ts_iso)
    lines.append("- Genesis hash: %s" % genesis_hash)
    lines.append("- Genesis timestamp (UTC): %s" % genesis_ts_iso)
    lines.append("")
    lines.append("## Comparison with the previous audit")
    lines.append("")
    lines.append("- Previous audit (21 Nov 2026, 04:50:45 UTC): chain ID 7295799, latest block 24793989.")
    if latest_number is not None:
        lines.append(
            "- This run: chain ID %s, latest block %s (delta %+d blocks)."
            % (chain_id, latest_number, latest_number - BASELINE_BLOCK)
        )
    else:
        lines.append("- This run: latest block could not be read; no comparison possible.")
    lines.append("- Chain ID matches the previous audit: %s." % ("yes" if chain_id == EXPECTED_CHAIN_ID else "NO - see checks above"))
    lines.append("")
    lines.append("## Files and SHA256")
    lines.append("")
    lines.append("- raw-data/rpc-responses/01_network_identity_raw.json - %s" % raw_sha)
    lines.append("- datasets/01_network_identity_metadata.json - %s" % metadata_sha)
    lines.append("- datasets/01_network_identity.csv - %s" % dataset_sha)
    lines.append("")
    lines.append("## Limitations")
    lines.append("")
    lines.append("- Read-only RPC calls only. Nothing here proves anything about the demo, the relayer, or contract behaviour.")
    lines.append("- On a live chain, eth_blockNumber and eth_getBlockByNumber(latest) are read seconds apart, so the check allows the latest block to be up to 10 blocks ahead of the blockNumber read, and never behind.")
    lines.append("- The RPC connection can drop mid-response through this VM's egress proxy (observed: RemoteDisconnected / IncompleteRead via urllib; the same call succeeds via curl). The script retries each call up to 5 times on a fresh connection and records the attempt count per call in the raw file.")
    lines.append("- The genesis block is read from the same RPC endpoint; an independent archive source was not cross-checked.")
    lines.append("- Block timestamps are the values reported by the chain, not independently measured wall-clock times.")
    lines.append("- A PASS here means network identity is consistent at retrieval time; it does not verify any other module.")
    lines.append("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    print("module: 01_network_identity")
    print("rpc: %s" % RPC_URL)
    print("retrieved_at_utc: %s" % retrieved_at_utc)
    print("chain_id: %s (%s)" % (chain_id, chain_id_hex))
    print("latest_block: %s (%s)" % (latest_number, values["latest_block_hex"]))
    print("latest_block_hash: %s" % latest_hash)
    print("latest_block_timestamp_utc: %s" % latest_ts_iso)
    print("genesis_hash: %s" % genesis_hash)
    print("genesis_block_timestamp_utc: %s" % genesis_ts_iso)
    print("status: %s" % status)
    for name, ok, detail in checks:
        print("check %s: %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    print("sha256 raw: %s" % raw_sha)
    print("sha256 metadata: %s" % metadata_sha)
    print("sha256 dataset: %s" % dataset_sha)
    print("raw: %s" % RAW_PATH)
    print("dataset: %s" % DATASET_PATH)
    print("metadata: %s" % METADATA_PATH)
    print("checksums: %s" % CHECKSUMS_PATH)
    print("report: %s" % REPORT_PATH)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
```

## 9. Limitations of this check

- Read-only RPC only. It proves nothing about the demo, the relayer, or contract behaviour.
- On a live chain, eth_blockNumber and eth_getBlockByNumber(latest) are read seconds apart, so the check allows the latest block to be up to 10 blocks ahead of the blockNumber read, and never behind.
- The RPC connection can drop mid-response through this VM's egress proxy (observed: RemoteDisconnected / IncompleteRead via urllib; the same call succeeds via curl). The script retries each call up to 5 times on a fresh connection and records the attempt count per call in the raw file.
- The genesis block is read from the same RPC endpoint; it was not cross-checked against an independent archive source.
- Block timestamps are the values reported by the chain, not independently measured wall-clock times.
- A PASS here means network identity is consistent at retrieval time; it does not verify any other module.
