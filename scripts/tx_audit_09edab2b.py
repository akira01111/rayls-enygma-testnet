#!/usr/bin/env python3
"""TX audit fetch — Rayls Enygma Week 2 experiment transaction (read-only).

Fetches, via plain JSON-RPC, the transaction, receipt, block, logs and
destination-contract data for one tx hash and stores each response as
received in the evidence package. Nothing is modified after capture:
every raw file is written once in exclusive mode and then chmod 444.

Target:
  TX 0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb
  Chain 7295799 (0x6f5337), RPC https://testnet-rpc.rayls.com
  Expected block 24825928 (from the experiment video / Explorer).

Method notes (from Module 01 experience on this VM):
  - urllib POSTs to this RPC intermittently die with RemoteDisconnected /
    IncompleteRead through the egress proxy while curl succeeds, so this
    script transports every call with the curl binary (subprocess), with
    up to 5 attempts per call and 1 s sleep between attempts. The attempt
    count is recorded per call in the raw file.
  - A browser-like User-Agent header is sent (plain urllib once got
    HTTP 403 error 1010 from Cloudflare on another endpoint).
  - First run of this script (2026-11-21T16:13:53Z) used urllib and
    FAILED on transport: eth_getTransactionByHash (IncompleteRead, 0
    bytes, 5/5 attempts), eth_getTransactionReceipt (IncompleteRead,
    9961 bytes read, 5/5), eth_getLogs (IncompleteRead, 0 bytes, 5/5).
    No valid data was captured; the partial raw/ directory was removed
    and the run was redone with curl. The failure is recorded here and
    in the report, not hidden.
  - Captured response data is serialized once and never modified after
    capture. A raw file here stores the request object, the parsed JSON
    response and transport metadata; it is a captured-and-serialized
    response structure, NOT a byte-level HTTP capture.

Exit codes: 0 = all core calls succeeded and all checks pass;
1 = a core call failed or a check failed (outputs still written);
2 = refusal (evidence already exists) or unexpected error.
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

SCRIPT_VERSION = "1.1.0"
TX_HASH = "0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb"
EXPECTED_BLOCK = 24825928
EXPECTED_CHAIN_ID = 7295799
RPC_URL = "https://testnet-rpc.rayls.com"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
EIP1967_IMPL_SLOT = (
    "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
)
# Contract addresses from the initial audit (C.2) — used only as read
# targets for eth_getCode context, never as an assumption about the tx.
RLS_TOKEN_PROXY = "0x07e17E17e17E17e17e17e17E17E17E17E17e17EA"
MULTICALL3 = "0xca11bde05977b3631167028862be2a173976ca11"
USER_REGISTRY_PROXY = "0xA473291FFb33e2276F364fAE169f03c4406719e9"

MAX_ATTEMPTS = 5
RETRY_SLEEP_S = 1.0


def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_hex_int(value):
    """Parse a 0x-hex string to int; None when not a valid hex int."""
    if not isinstance(value, str):
        return None
    try:
        return int(value, 16)
    except (TypeError, ValueError):
        return None


def rpc_call(method, params, req_id):
    """One JSON-RPC call via curl, with retries. Returns a call record."""
    payload = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}
    data = json.dumps(payload).encode("utf-8")
    attempts = 0
    last_problem = None
    while attempts < MAX_ATTEMPTS:
        attempts += 1
        try:
            proc = subprocess.run(
                ["curl", "-s", "-S", "--max-time", "60", "-X", "POST",
                 "-H", "Content-Type: application/json",
                 "-H", "User-Agent: " + USER_AGENT,
                 "-d", data.decode("utf-8"),
                 "-w", "\nHTTPSTATUS:%{http_code}",
                 RPC_URL],
                capture_output=True, timeout=90)
            out = proc.stdout.decode("utf-8", errors="replace")
            if proc.returncode != 0:
                last_problem = "curl exit %d: %s" % (
                    proc.returncode,
                    proc.stderr.decode("utf-8", errors="replace")[:300])
                if attempts < MAX_ATTEMPTS:
                    time.sleep(RETRY_SLEEP_S)
                continue
            if "\nHTTPSTATUS:" not in out:
                last_problem = "curl output missing HTTP status trailer"
                if attempts < MAX_ATTEMPTS:
                    time.sleep(RETRY_SLEEP_S)
                continue
            body, _, status = out.rpartition("\nHTTPSTATUS:")
            if status.strip() != "200":
                last_problem = "HTTP status %s" % status.strip()
                if attempts < MAX_ATTEMPTS:
                    time.sleep(RETRY_SLEEP_S)
                continue
            parsed = json.loads(body)
            validation = validate_response(parsed, req_id)
            return {
                "method": method,
                "params": params,
                "attempts": attempts,
                "validation": validation,
                "request": payload,
                "response": parsed,
            }
        except (subprocess.TimeoutExpired, json.JSONDecodeError,
                OSError) as exc:
            last_problem = "%s: %s" % (type(exc).__name__, exc)
            if attempts < MAX_ATTEMPTS:
                time.sleep(RETRY_SLEEP_S)
    return {
        "method": method,
        "params": params,
        "attempts": attempts,
        "validation": {"ok": False, "problems": [last_problem or "unknown error"]},
        "request": payload,
        "response": None,
    }


def validate_response(resp, req_id):
    """Check a JSON-RPC response envelope. Returns {ok, problems}."""
    problems = []
    if not isinstance(resp, dict):
        return {"ok": False, "problems": ["response is not a JSON object"]}
    if resp.get("jsonrpc") != "2.0":
        problems.append("jsonrpc is not '2.0': %r" % (resp.get("jsonrpc"),))
    if resp.get("id") != req_id:
        problems.append("id mismatch: expected %r, got %r" % (req_id, resp.get("id")))
    if "error" in resp and resp["error"] is not None:
        problems.append("RPC error object present: %r" % (resp["error"],))
    if "result" not in resp:
        problems.append("missing 'result' field")
    return {"ok": not problems, "problems": problems}


def result_of(call):
    """The 'result' of a call record, or None when invalid."""
    resp = call.get("response")
    if not isinstance(resp, dict):
        return None
    return resp.get("result")


def write_json_exclusive(path, obj):
    """Write JSON once in exclusive mode, then chmod 444. Refuses overwrite."""
    text = json.dumps(obj, indent=2, sort_keys=True) + "\n"
    with open(path, "x", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(path, 0o444)


def main():
    script_path = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(script_path))
    pkg_dir = os.path.join(
        repo_root, "experiments", "transactions", "tx-09edab2b"
    )
    raw_dir = os.path.join(pkg_dir, "raw")
    try:
        os.makedirs(raw_dir, exist_ok=False)
    except FileExistsError:
        print("REFUSAL: raw directory already exists: %s" % raw_dir)
        print("Refusing to overwrite existing evidence. Aborting.")
        return 2

    retrieved_at = utc_now_iso()
    base_meta = {
        "script": os.path.relpath(script_path, repo_root),
        "script_version": SCRIPT_VERSION,
        "tx_hash": TX_HASH,
        "chain_id_expected": EXPECTED_CHAIN_ID,
        "expected_block": EXPECTED_BLOCK,
        "rpc_url": RPC_URL,
        "retrieved_at_utc": retrieved_at,
    }
    req_id = 0

    def call(method, params):
        nonlocal req_id
        req_id += 1
        return rpc_call(method, params, req_id)

    checks = []

    def check(name, passed, detail):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    # ---- 1. chain identity + current block (context) + the transaction ----
    c_chain = call("eth_chainId", [])
    c_blocknum = call("eth_blockNumber", [])
    c_tx = call("eth_getTransactionByHash", [TX_HASH])
    tx = result_of(c_tx)
    chain_id = parse_hex_int(result_of(c_chain)) if c_chain["validation"]["ok"] else None
    check("chain_id_is_7295799", chain_id == EXPECTED_CHAIN_ID,
          "eth_chainId -> %r (parsed %r)" % (result_of(c_chain), chain_id))
    check("transaction_found", isinstance(tx, dict) and tx.get("hash") is not None,
          "eth_getTransactionByHash returned %s"
          % ("a tx object" if isinstance(tx, dict) else "null/invalid"))
    tx_hash_ok = isinstance(tx, dict) and (tx.get("hash") or "").lower() == TX_HASH.lower()
    check("transaction_hash_matches_target", tx_hash_ok,
          "tx.hash -> %r" % (tx.get("hash") if isinstance(tx, dict) else None))
    tx_block = parse_hex_int(tx.get("blockNumber")) if isinstance(tx, dict) else None
    check("transaction_block_is_24825928", tx_block == EXPECTED_BLOCK,
          "tx.blockNumber -> %r (parsed %r)" % (
              tx.get("blockNumber") if isinstance(tx, dict) else None, tx_block))
    tx_to = tx.get("to") if isinstance(tx, dict) else None
    rec_tx = dict(base_meta)
    rec_tx["calls"] = [c_chain, c_blocknum, c_tx]
    rec_tx["checks"] = checks
    write_json_exclusive(os.path.join(raw_dir, "transaction.json"), rec_tx)

    # ---- 2. receipt ----
    c_receipt = call("eth_getTransactionReceipt", [TX_HASH])
    receipt = result_of(c_receipt)
    rec_ok = isinstance(receipt, dict)
    check("receipt_found", rec_ok,
          "eth_getTransactionReceipt returned %s"
          % ("a receipt object" if rec_ok else "null/invalid"))
    status = receipt.get("status") if rec_ok else None
    check("receipt_status_success", status in ("0x1", 1),
          "receipt.status -> %r" % (status,))
    r_block = parse_hex_int(receipt.get("blockNumber")) if rec_ok else None
    check("receipt_block_is_24825928", r_block == EXPECTED_BLOCK,
          "receipt.blockNumber -> %r (parsed %r)" % (
              receipt.get("blockNumber") if rec_ok else None, r_block))
    check("receipt_block_matches_tx_block", rec_ok and r_block == tx_block,
          "receipt block %r vs tx block %r" % (r_block, tx_block))
    r_to = receipt.get("to") if rec_ok else None
    check("receipt_to_matches_tx_to",
          rec_ok and isinstance(r_to, str) and isinstance(tx_to, str)
          and r_to.lower() == tx_to.lower(),
          "receipt.to %r vs tx.to %r" % (r_to, tx_to))
    r_hash = receipt.get("transactionHash") if rec_ok else None
    check("receipt_txhash_matches_target",
          isinstance(r_hash, str) and r_hash.lower() == TX_HASH.lower(),
          "receipt.transactionHash -> %r" % (r_hash,))
    r_logs = receipt.get("logs") if rec_ok else None
    check("receipt_logs_present", isinstance(r_logs, list),
          "receipt.logs is a list of %d entries"
          % (len(r_logs) if isinstance(r_logs, list) else -1))
    rec_receipt = dict(base_meta)
    rec_receipt["calls"] = [c_receipt]
    rec_receipt["checks"] = checks
    write_json_exclusive(os.path.join(raw_dir, "receipt.json"), rec_receipt)

    # ---- 3. block + block logs (completeness cross-check) ----
    block_hex = receipt.get("blockNumber") if rec_ok else None
    if not isinstance(block_hex, str):
        block_hex = "0x%x" % EXPECTED_BLOCK
    c_block = call("eth_getBlockByNumber", [block_hex, False])
    block = result_of(c_block)
    b_number = parse_hex_int(block.get("number")) if isinstance(block, dict) else None
    check("block_number_matches_receipt", b_number == EXPECTED_BLOCK,
          "block.number -> %r (parsed %r)" % (
              block.get("number") if isinstance(block, dict) else None, b_number))
    b_hash = block.get("hash") if isinstance(block, dict) else None
    r_bhash = receipt.get("blockHash") if rec_ok else None
    check("block_hash_matches_receipt",
          isinstance(b_hash, str) and isinstance(r_bhash, str)
          and b_hash.lower() == r_bhash.lower(),
          "block.hash %r vs receipt.blockHash %r" % (b_hash, r_bhash))
    rec_block = dict(base_meta)
    rec_block["calls"] = [c_block]
    rec_block["checks"] = checks
    write_json_exclusive(os.path.join(raw_dir, "block.json"), rec_block)

    # Block-level logs filtered to the three known log emitters from the
    # initial audit (C.2): the vault proxy, the RLS token proxy and
    # Multicall3. The receipt is authoritative for this tx; this call is
    # only a completeness cross-check, and its address filter is a stated
    # limitation (a log from an unexpected address would not appear here).
    c_logs = call("eth_getLogs", [{
        "fromBlock": block_hex, "toBlock": block_hex,
        "address": [RLS_TOKEN_PROXY, MULTICALL3,
                    "0x9C5Ad5e5Ea5b5910E7fD1E1CC7b70ce0e4bF06c2"],
    }])
    block_logs = result_of(c_logs)
    if isinstance(block_logs, list) and isinstance(r_logs, list):
        tx_logs_in_block = [lg for lg in block_logs
                            if isinstance(lg, dict)
                            and (lg.get("transactionHash") or "").lower() == TX_HASH.lower()]
        check("block_logs_contain_receipt_logs",
              len(tx_logs_in_block) == len(r_logs),
              "eth_getLogs for the block returned %d logs for this tx; "
              "receipt has %d logs" % (len(tx_logs_in_block), len(r_logs)))
        # every receipt log must appear identically in the block-level set
        r_set = {json.dumps(lg, sort_keys=True) for lg in r_logs
                 if isinstance(lg, dict)}
        b_set = {json.dumps(lg, sort_keys=True) for lg in tx_logs_in_block}
        check("receipt_logs_identical_to_block_logs", r_set == b_set,
              "receipt log set == block-level log set for this tx: %s"
              % (r_set == b_set))
    else:
        check("block_logs_contain_receipt_logs", False,
              "eth_getLogs result is not a list or receipt logs missing")
        check("receipt_logs_identical_to_block_logs", False,
              "cannot compare: one side is not a list")
    rec_logs = dict(base_meta)
    rec_logs["calls"] = [c_logs]
    rec_logs["receipt_logs_copy"] = r_logs
    rec_logs["checks"] = checks
    write_json_exclusive(os.path.join(raw_dir, "logs.json"), rec_logs)

    # ---- 4. destination contract: code + EIP-1967 implementation slot ----
    c_calls = []
    dest = tx_to if isinstance(tx_to, str) else None
    impl_addr = None
    if dest:
        c_code = call("eth_getCode", [dest, "latest"])
        c_calls.append(c_code)
        code = result_of(c_code)
        check("destination_code_nonempty",
              isinstance(code, str) and len(code) > 2,
              "eth_getCode(%s) returned %d hex chars"
              % (dest, len(code) if isinstance(code, str) else -1))
        c_slot = call("eth_getStorageAt", [dest, EIP1967_IMPL_SLOT, "latest"])
        c_calls.append(c_slot)
        slot = result_of(c_slot)
        if isinstance(slot, str) and len(slot) == 66:
            impl_addr = "0x" + slot[-40:]
            check("implementation_slot_readable", True,
                  "EIP-1967 slot -> %s (implementation %s)" % (slot, impl_addr))
        else:
            check("implementation_slot_readable", False,
                  "EIP-1967 slot -> %r" % (slot,))
        if impl_addr and impl_addr != "0x0000000000000000000000000000000000000000":
            c_impl_code = call("eth_getCode", [impl_addr, "latest"])
            c_calls.append(c_impl_code)
            icode = result_of(c_impl_code)
            check("implementation_code_nonempty",
                  isinstance(icode, str) and len(icode) > 2,
                  "eth_getCode(%s) returned %d hex chars"
                  % (impl_addr, len(icode) if isinstance(icode, str) else -1))
    else:
        check("destination_code_nonempty", False, "tx.to is missing; no code read")
        check("implementation_slot_readable", False, "tx.to is missing")
    # context reads (audit C.2 addresses, for contracts.json comparison)
    for label, addr in (("rls_token_proxy", RLS_TOKEN_PROXY),
                        ("multicall3", MULTICALL3),
                        ("user_registry_proxy", USER_REGISTRY_PROXY)):
        c_ctx = call("eth_getCode", [addr, "latest"])
        c_ctx["label"] = label
        c_calls.append(c_ctx)
    rec_contracts = dict(base_meta)
    rec_contracts["destination"] = dest
    rec_contracts["implementation_from_slot"] = impl_addr
    rec_contracts["calls"] = c_calls
    rec_contracts["checks"] = checks
    write_json_exclusive(os.path.join(raw_dir, "contracts.json"), rec_contracts)

    # ---- summary ----
    core_failed = [c for c in checks if not c["passed"]]
    status = "PASS" if not core_failed else "FAIL"
    print("retrieved_at_utc: %s" % retrieved_at)
    print("tx: %s" % TX_HASH)
    print("to: %s" % dest)
    print("implementation from slot: %s" % impl_addr)
    print("receipt logs: %s"
          % (len(r_logs) if isinstance(r_logs, list) else "n/a"))
    print("checks: %d/%d passed" % (len(checks) - len(core_failed), len(checks)))
    for c in core_failed:
        print("  FAILED: %s — %s" % (c["name"], c["detail"]))
    print("status: %s" % status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
