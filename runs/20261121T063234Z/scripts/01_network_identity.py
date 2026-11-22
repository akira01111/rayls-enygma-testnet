#!/usr/bin/env python3
"""Module 01 - Network Identity Audit: Rayls Enygma Public Testnet.

Version 2.0.1 - response validation and safe parsing (patch over 2.0.0).

Read-only JSON-RPC checks using the Python standard library only.
No private key, no wallet, no API secret, no third-party library.

Calls made:
  - eth_chainId
  - eth_blockNumber
  - eth_getBlockByNumber (latest, full transactions = false)
  - eth_getBlockByNumber (genesis, block 0x0, full transactions = false)

Every execution writes to its own run directory:
  runs/<run_id>/
    raw-data/rpc-responses/01_network_identity_raw.json
    datasets/01_network_identity.csv
    datasets/01_network_identity_metadata.json
    datasets/01_network_identity_checksums.sha256
    findings/verified-facts/01_network_identity_verification.md
    scripts/01_network_identity.py   (byte copy of the script that ran)

run_id is the UTC timestamp of the run start (YYYYMMDDTHHMMSSZ).
If a directory with that name already exists, a -2 / -3 suffix is added
so the new run never touches the old one.

What the raw JSON is (and is not):
  The raw JSON file is a captured-and-serialized response structure:
  for each call it stores the request object, the parsed JSON response,
  and transport metadata (HTTP status, attempt count, any error, and
  the validation verdict). It is NOT a byte-level HTTP capture: no raw
  HTTP bytes, headers, or TLS data are stored.

Response validation (new in 2.0.1):
  Every captured response is validated before any value is used:
  JSON-RPC version must be "2.0", the response id must match the
  request id, there must be no RPC error object, a "result" field
  must exist, and the result must have the expected shape (a hex
  string for eth_chainId / eth_blockNumber; a block object with
  number, hash, and timestamp for eth_getBlockByNumber). Hashes must
  be full 64-hex-digit values (0x + 64 hex chars). A response that
  fails any of these makes its response_valid_* check FAIL with the
  exact problem recorded in the check detail and in the raw file's
  validation field. It never crashes the run.

Safe parsing (new in 2.0.1):
  All values are parsed through helpers that return None on invalid
  input instead of raising (parse_hex_int, is_full_hash,
  block_timestamp_iso). A malformed or mistyped value therefore
  produces a FAIL check with a clear detail, never a traceback, and
  the run still writes every output file with status FAIL.

Check names (13 checks in 2.0.1):
  response_valid_eth_chainId, response_valid_eth_blockNumber,
  response_valid_eth_getBlockByNumber_latest,
  response_valid_eth_getBlockByNumber_genesis,
  chain_id_matches_expected,
  block_number_within_drift_of_latest_block (renamed in 2.0.1: the
  old name block_number_matches_latest_block wrongly suggested the
  two numbers must be exactly equal; the check allows the latest
  block to be up to 10 blocks ahead, never behind),
  latest_block_has_hash, latest_block_timestamp_valid,
  genesis_block_is_zero, genesis_block_has_hash,
  latest_block_after_genesis, latest_block_not_before_baseline,
  all_rpc_calls_succeeded.

Repository root (new in 2.0.1):
  The repository root is found by walking up from the script file
  until a directory containing both a scripts/ and a runs/
  directory is found. An archived copy run from
  runs/<run_id>/scripts/ therefore still resolves the real repo
  root and writes new runs under the repo's runs/, never inside
  the archived run. If no such directory exists the script refuses
  to run (exit code 2) with a clear message.

No-overwrite guarantees (unchanged from 2.0.0):
  - the run directory is created with exist_ok=False; an existing
    directory is never reused;
  - every output file is created with exclusive mode ("x"); if a file
    already exists the script aborts with exit code 2 and writes
    nothing more;
  - the raw JSON is set read-only (chmod 0o444) immediately after
    capture, and the script never opens it for writing again;
  - the checksum manifest covers the raw JSON, metadata, CSV, the
    script copy, and the verification report, so any later change to
    any of them is detectable. The manifest does not hash itself:
    a file cannot contain its own hash.

Exit code: 0 when every check passes (PASS), 1 when a check fails
(FAIL), 2 when the script refuses to run (output already exists,
repository root not found) or another error prevents a clean run.
Raw data is written exactly as received and is never modified afterwards.
"""

import csv
import hashlib
import http.client
import io
import json
import os
import platform
import re
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

SCRIPT_VERSION = "2.0.1"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
TIMEOUT_SECONDS = 30
MAX_ATTEMPTS = 5
MAX_DRIFT_BLOCKS = 10

HEX_RE = re.compile(r"^0x[0-9a-f]+$")
HASH_RE = re.compile(r"^0x[0-9a-f]{64}$")


def find_repo_root(start_path):
    """Walk up from start_path to the repository root.

    The root is the first directory containing both a scripts/ and a
    runs/ directory. This works for the live script
    (scripts/01_network_identity.py) and for an archived copy run
    from runs/<run_id>/scripts/01_network_identity.py, which must
    still write new runs under the repo's runs/, never inside the
    archived run. Raises RuntimeError if no such directory exists.
    """
    current = Path(start_path).resolve()
    if current.is_file():
        current = current.parent
    while True:
        if (current / "scripts").is_dir() and (current / "runs").is_dir():
            return current
        parent = current.parent
        if parent == current:
            raise RuntimeError(
                "cannot locate repository root from %s "
                "(expected a directory containing both scripts/ and runs/)"
                % start_path
            )
        current = parent


def utc_now_iso():
    """Current UTC time as ISO 8601 with a Z suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_run_id(now=None):
    """Unique run ID based on the UTC timestamp (YYYYMMDDTHHMMSSZ)."""
    moment = now or datetime.now(timezone.utc)
    return moment.strftime("%Y%m%dT%H%M%SZ")


def resolve_run_dir(runs_dir, run_id):
    """Pick a run directory that does not exist yet.

    If runs/<run_id> already exists, append -2, -3, ... so the new run
    never reuses (and therefore never overwrites) an old run's files.
    Returns (final_run_id, run_dir).
    """
    candidate = run_id
    suffix = 2
    while (runs_dir / candidate).exists():
        candidate = "%s-%d" % (run_id, suffix)
        suffix += 1
        if suffix > 100:
            raise RuntimeError("could not find a free run directory for %s" % run_id)
    return candidate, runs_dir / candidate


def is_hex_string(value):
    """True when value is a '0x' + hex-digits string."""
    return isinstance(value, str) and HEX_RE.match(value) is not None


def is_full_hash(value):
    """True when value is a full 32-byte hash: '0x' + 64 hex digits."""
    return isinstance(value, str) and HASH_RE.match(value) is not None


def parse_hex_int(value):
    """Parse a hex string to int, or None when it is not a hex string."""
    if not is_hex_string(value):
        return None
    try:
        return int(value, 16)
    except ValueError:
        return None


def block_timestamp_iso(hex_timestamp):
    """Convert a hex block timestamp to UTC ISO 8601, or None if invalid.

    Invalid means: not a hex string, not a positive number, or out of
    range for a Unix timestamp. Never raises.
    """
    value = parse_hex_int(hex_timestamp)
    if value is None or value <= 0:
        return None
    try:
        return datetime.fromtimestamp(value, tz=timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
    except (ValueError, OverflowError, OSError):
        return None


def write_text_exclusive(path, text):
    """Create a file with exclusive mode ("x").

    Refuses to overwrite: raises FileExistsError if the file already
    exists. Parent directories are created as needed.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "x", encoding="utf-8") as handle:
        handle.write(text)


def write_bytes_exclusive(path, data):
    """Create a file with exclusive mode ("x") from bytes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "xb") as handle:
        handle.write(data)


def write_json_exclusive(path, data):
    """Create a JSON file with exclusive mode ("x")."""
    write_text_exclusive(path, json.dumps(data, indent=2, sort_keys=False) + "\n")


def rpc_call(method, params, call_id):
    """One read-only JSON-RPC call, retried on a fresh connection.

    The RPC endpoint can cut a chunked response mid-body
    (http.client.IncompleteRead). Each attempt opens a new connection.
    Returns (record, error_or_None). The record holds the request
    object, the parsed JSON response (or None), the HTTP status, the
    attempt count, and any transport error. The response is stored
    as parsed JSON, not as raw HTTP bytes.
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
    for attempt in range(1, MAX_ATTEMPTS + 1):
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


def validate_response(record, expected_id, result_kind):
    """Validate one captured JSON-RPC response.

    Checks, in order: the transport did not fail; the HTTP status is
    200 (when known); the response is a JSON object; the JSON-RPC
    version is "2.0"; the response id matches the request id; there
    is no RPC error object; a "result" field exists; and the result
    has the expected shape ("hex" for eth_chainId / eth_blockNumber,
    "block" for eth_getBlockByNumber, which must carry number, hash,
    and timestamp as hex strings, the hash being a full 64-hex hash).
    Returns (ok, problems): ok is True only when there are no problems.
    """
    problems = []
    if record.get("error") is not None:
        problems.append("transport failed: %s" % record["error"])
        return False, problems
    status = record.get("http_status")
    if status is not None and status != 200:
        problems.append("HTTP status %s, expected 200" % status)
    response = record.get("response")
    if not isinstance(response, dict):
        problems.append(
            "response is not a JSON object (got %s)" % type(response).__name__
        )
        return False, problems
    if response.get("jsonrpc") != "2.0":
        problems.append(
            "jsonrpc version is %r, expected '2.0'" % (response.get("jsonrpc"),)
        )
    if response.get("id") != expected_id:
        problems.append(
            "response id is %r, expected %r" % (response.get("id"), expected_id)
        )
    if "error" in response:
        problems.append("RPC error: %s" % (response["error"],))
    if "result" not in response:
        problems.append("response has no 'result' field")
        return False, problems
    result = response["result"]
    if result_kind == "hex":
        if not is_hex_string(result):
            problems.append("result is not a hex string: %r" % (result,))
    elif result_kind == "block":
        if result is None:
            problems.append("result is null, expected a block object")
        elif not isinstance(result, dict):
            problems.append(
                "result is not a block object (got %s)" % type(result).__name__
            )
        else:
            for field in ("number", "hash", "timestamp"):
                if field not in result:
                    problems.append("block is missing field %r" % field)
                elif field == "hash":
                    if not is_full_hash(result[field]):
                        problems.append(
                            "block hash is not a full 64-hex hash: %r"
                            % (result[field],)
                        )
                elif not is_hex_string(result[field]):
                    problems.append(
                        "block field %r is not a hex string: %r" % (field, result[field])
                    )
    return (not problems), problems


def sha256_hex(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def evaluate(calls):
    """Compute the checks and observed values from the call records.

    Never raises on malformed data: an invalid value becomes None and
    produces a FAIL check with a clear detail, so the failure is
    recorded instead of crashing the run. Returns
    (checks, values, status) where checks is a list of
    (name, ok, detail).
    """
    checks = []
    values = {}

    # 1-4. One response-validation check per call.
    specs = [
        ("eth_chainId", "hex"),
        ("eth_blockNumber", "hex"),
        ("eth_getBlockByNumber", "block"),
        ("eth_getBlockByNumber", "block"),
    ]
    validations = []
    results = []
    for index, (record, (method, kind)) in enumerate(zip(calls, specs), start=1):
        ok, problems = validate_response(record, index, kind)
        validations.append((ok, problems))
        if ok:
            results.append(record["response"]["result"])
        else:
            results.append(None)
        if kind == "block":
            tag = record.get("params", ["?"])[0]
            label = "latest" if tag == "latest" else "genesis"
        else:
            label = method
        checks.append(
            (
                "response_valid_%s" % label,
                ok,
                "valid" if ok else "; ".join(problems),
            )
        )

    # Transport / RPC errors, for the summary check.
    errors = []
    for record in calls:
        if record.get("error") is not None:
            errors.append("%s: %s" % (record["method"], record["error"]))
        elif isinstance(record.get("response"), dict) and "error" in record["response"]:
            errors.append(
                "%s: RPC error %s" % (record["method"], record["response"]["error"])
            )

    def valid_detail(index):
        ok, problems = validations[index]
        return "; ".join(problems) if not ok else "valid"

    # 5. Chain ID matches the expected value from the previous audit.
    chain_id_hex = results[0] if isinstance(results[0], str) else None
    chain_id = parse_hex_int(chain_id_hex)
    values["chain_id"] = chain_id
    values["chain_id_hex"] = chain_id_hex
    checks.append(
        (
            "chain_id_matches_expected",
            chain_id == EXPECTED_CHAIN_ID and chain_id_hex == EXPECTED_CHAIN_ID_HEX,
            (
                "expected %d (%s), observed %s (%s)"
                % (EXPECTED_CHAIN_ID, EXPECTED_CHAIN_ID_HEX, chain_id, chain_id_hex)
                if chain_id_hex is not None
                else "no valid chainId result (%s)" % valid_detail(0)
            ),
        )
    )

    # 6. eth_blockNumber is within drift of the latest block's own number.
    # The chain is live: the two reads happen seconds apart, so the latest
    # block may have advanced between them. The check allows the latest
    # block to be ahead by up to MAX_DRIFT_BLOCKS blocks, and never behind.
    # The name says "within drift" on purpose: the two numbers are NOT
    # required to be exactly equal.
    block_number_hex = results[1] if isinstance(results[1], str) else None
    block_number = parse_hex_int(block_number_hex)
    latest_block = results[2] if isinstance(results[2], dict) else None
    genesis_block = results[3] if isinstance(results[3], dict) else None
    latest_number = parse_hex_int(latest_block.get("number")) if latest_block else None
    values["latest_block"] = latest_number
    values["latest_block_hex"] = latest_block.get("number") if latest_block else None
    drift = (
        (latest_number - block_number)
        if (latest_number is not None and block_number is not None)
        else None
    )
    checks.append(
        (
            "block_number_within_drift_of_latest_block",
            drift is not None and 0 <= drift <= MAX_DRIFT_BLOCKS,
            (
                "eth_blockNumber=%s, latest.number=%s, drift=+%s blocks "
                "(allowed 0..+%d, never behind)"
                % (block_number, latest_number, drift, MAX_DRIFT_BLOCKS)
                if drift is not None
                else "cannot compare: eth_blockNumber=%s (%s), latest.number=%s (%s)"
                % (
                    block_number,
                    "valid" if block_number is not None else valid_detail(1),
                    latest_number,
                    "valid" if latest_number is not None else valid_detail(2),
                )
            ),
        )
    )

    # 7. Latest block carries a full 64-hex hash.
    latest_hash = latest_block.get("hash") if latest_block else None
    values["latest_block_hash"] = latest_hash
    checks.append(
        (
            "latest_block_has_hash",
            is_full_hash(latest_hash),
            (
                "hash=%s" % latest_hash
                if is_full_hash(latest_hash)
                else "hash is not a full 64-hex hash: %r" % (latest_hash,)
            ),
        )
    )

    # 8. Latest block timestamp is a valid, positive Unix time.
    latest_ts_hex = latest_block.get("timestamp") if latest_block else None
    latest_ts_iso = block_timestamp_iso(latest_ts_hex)
    values["latest_block_timestamp_utc"] = latest_ts_iso
    checks.append(
        (
            "latest_block_timestamp_valid",
            latest_ts_iso is not None,
            (
                "timestamp=%s (%s)" % (latest_ts_hex, latest_ts_iso)
                if latest_ts_iso is not None
                else "timestamp is not a valid positive hex time: %r" % (latest_ts_hex,)
            ),
        )
    )

    # 9. Genesis block is block 0.
    genesis_number = parse_hex_int(genesis_block.get("number")) if genesis_block else None
    values["genesis_block"] = genesis_number
    checks.append(
        (
            "genesis_block_is_zero",
            genesis_number == 0,
            (
                "genesis.number=%s" % genesis_number
                if genesis_number is not None
                else "no valid genesis block (%s)" % valid_detail(3)
            ),
        )
    )

    # 10. Genesis block carries a full 64-hex hash.
    genesis_hash = genesis_block.get("hash") if genesis_block else None
    values["genesis_hash"] = genesis_hash
    checks.append(
        (
            "genesis_block_has_hash",
            is_full_hash(genesis_hash),
            (
                "hash=%s" % genesis_hash
                if is_full_hash(genesis_hash)
                else "hash is not a full 64-hex hash: %r" % (genesis_hash,)
            ),
        )
    )

    # 11. Latest block is ahead of genesis.
    checks.append(
        (
            "latest_block_after_genesis",
            latest_number is not None and genesis_number == 0 and latest_number > 0,
            "latest=%s, genesis=%s" % (latest_number, genesis_number),
        )
    )

    # 12. Chain has not gone backwards versus the previous audit's observation.
    checks.append(
        (
            "latest_block_not_before_baseline",
            latest_number is not None and latest_number >= BASELINE_BLOCK,
            "latest=%s, baseline=%d at %s" % (latest_number, BASELINE_BLOCK, BASELINE_BLOCK_AT_UTC),
        )
    )

    # 13. No call failed.
    checks.append(
        ("all_rpc_calls_succeeded", not errors, "; ".join(errors) if errors else "4/4 calls OK")
    )

    # Genesis timestamp (observed value, not a check).
    genesis_ts_hex = genesis_block.get("timestamp") if genesis_block else None
    genesis_ts_iso = block_timestamp_iso(genesis_ts_hex)
    values["genesis_block_timestamp_utc"] = genesis_ts_iso

    passed = all(ok for _, ok, _ in checks)
    status = "PASS" if passed else "FAIL"
    return checks, values, status


def main():
    retrieved_at_utc = utc_now_iso()
    script_path = Path(__file__).resolve()
    script_bytes = script_path.read_bytes()
    script_sha256 = sha256_bytes(script_bytes)

    # Resolve the repository root (works from the live script and from
    # an archived copy under runs/<run_id>/scripts/).
    try:
        repo_root = find_repo_root(script_path)
    except RuntimeError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2
    runs_dir = repo_root / "runs"

    # Resolve a run directory that does not exist yet. Never reuse one.
    try:
        run_id, run_dir = resolve_run_dir(runs_dir, new_run_id())
        run_dir.mkdir(parents=True, exist_ok=False)
    except (FileExistsError, RuntimeError) as exc:
        print("REFUSED: %s" % exc, file=sys.stderr)
        print("Refusing to run: the run directory already exists. No file was written.", file=sys.stderr)
        return 2

    raw_path = run_dir / "raw-data" / "rpc-responses" / "01_network_identity_raw.json"
    dataset_path = run_dir / "datasets" / "01_network_identity.csv"
    metadata_path = run_dir / "datasets" / "01_network_identity_metadata.json"
    checksums_path = run_dir / "datasets" / "01_network_identity_checksums.sha256"
    report_path = run_dir / "findings" / "verified-facts" / "01_network_identity_verification.md"
    script_copy_path = run_dir / "scripts" / "01_network_identity.py"

    try:
        calls = []
        for call_id, (method, params) in enumerate(
            [
                ("eth_chainId", []),
                ("eth_blockNumber", []),
                ("eth_getBlockByNumber", ["latest", False]),
                ("eth_getBlockByNumber", ["0x0", False]),
            ],
            start=1,
        ):
            record, _error = rpc_call(method, params, call_id)
            kind = "hex" if method in ("eth_chainId", "eth_blockNumber") else "block"
            ok, problems = validate_response(record, call_id, kind)
            record["validation"] = {"ok": ok, "problems": problems}
            calls.append(record)

        # Raw request/response structures, exactly as sent and received
        # (parsed JSON, not raw HTTP bytes). Written once, in exclusive
        # mode, then set read-only.
        raw = {
            "module": "01_network_identity",
            "network": "Rayls Enygma Public Testnet",
            "rpc_endpoint": RPC_URL,
            "run_id": run_id,
            "retrieved_at_utc": retrieved_at_utc,
            "calls": calls,
        }
        write_json_exclusive(raw_path, raw)
        os.chmod(raw_path, 0o444)

        checks, values, status = evaluate(calls)
        checks_passed = sum(1 for _, ok, _ in checks if ok)
        chain_id = values["chain_id"]
        chain_id_hex = values["chain_id_hex"]
        latest_number = values["latest_block"]
        latest_hash = values["latest_block_hash"]
        latest_ts_iso = values["latest_block_timestamp_utc"]
        genesis_hash = values["genesis_hash"]
        genesis_ts_iso = values["genesis_block_timestamp_utc"]

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
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=list(dataset_row.keys()))
        writer.writeheader()
        writer.writerow(dataset_row)
        write_text_exclusive(dataset_path, csv_buffer.getvalue())

        # Byte copy of the exact script that ran, set read-only.
        # This makes the run self-contained: the code that produced it
        # is preserved even if scripts/01_network_identity.py changes later.
        write_bytes_exclusive(script_copy_path, script_bytes)
        os.chmod(script_copy_path, 0o444)

        # Metadata, including run ID and script version.
        metadata = {
            "module": "01_network_identity",
            "network": "Rayls Enygma Public Testnet",
            "rpc_endpoint": RPC_URL,
            "run_id": run_id,
            "run_dir": "runs/%s" % run_id,
            "script_version": SCRIPT_VERSION,
            "script": "scripts/01_network_identity.py",
            "script_copy": "runs/%s/scripts/01_network_identity.py" % run_id,
            "script_sha256": script_sha256,
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
            "checks_total": len(checks),
            "checks_passed": checks_passed,
            "retrieved_at_utc": retrieved_at_utc,
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "status": status,
        }
        write_json_exclusive(metadata_path, metadata)

        # Verification report.
        lines = []
        lines.append("# Module 01 - Network Identity Audit: Verification Report")
        lines.append("")
        lines.append("Network: Rayls Enygma Public Testnet")
        lines.append("RPC endpoint: %s" % RPC_URL)
        lines.append("Run ID: %s" % run_id)
        lines.append("Run directory: runs/%s" % run_id)
        lines.append("Retrieved at (UTC): %s" % retrieved_at_utc)
        lines.append("Script: scripts/01_network_identity.py (version %s)" % SCRIPT_VERSION)
        lines.append("Script copy in this run: runs/%s/scripts/01_network_identity.py" % run_id)
        lines.append("Python: %s (%s)" % (platform.python_version(), platform.python_implementation()))
        lines.append("")
        lines.append("## Status: %s (%d/%d checks)" % (status, checks_passed, len(checks)))
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
        lines.append("- raw-data/rpc-responses/01_network_identity_raw.json - %s" % sha256_hex(raw_path))
        lines.append("- datasets/01_network_identity_metadata.json - %s" % sha256_hex(metadata_path))
        lines.append("- datasets/01_network_identity.csv - %s" % sha256_hex(dataset_path))
        lines.append("- scripts/01_network_identity.py (copy of the script that ran) - %s" % script_sha256)
        lines.append("")
        lines.append("The checksum manifest datasets/01_network_identity_checksums.sha256 also covers this report itself.")
        lines.append("")
        lines.append("## Limitations")
        lines.append("")
        lines.append("- Read-only RPC calls only. Nothing here proves anything about the demo, the relayer, or contract behaviour.")
        lines.append("- Response validation: every RPC response is checked for JSON-RPC version 2.0, a response id matching the request id, no RPC error object, and a well-formed result (hex string for eth_chainId / eth_blockNumber; block object with number, hash, and timestamp for eth_getBlockByNumber). A response that fails any of these makes its response_valid_* check FAIL with the exact problem recorded; it never crashes the run.")
        lines.append("- The raw JSON file is a captured-and-serialized response structure (request object + parsed JSON response + transport metadata), not a byte-level HTTP capture: no raw HTTP bytes, headers, or TLS data are stored.")
        lines.append("- On a live chain, eth_blockNumber and eth_getBlockByNumber(latest) are read seconds apart, so the check block_number_within_drift_of_latest_block allows the latest block to be up to 10 blocks ahead of the blockNumber read, and never behind. The two numbers are not required to be exactly equal.")
        lines.append("- The RPC connection can drop mid-response through this VM's egress proxy (observed: RemoteDisconnected / IncompleteRead via urllib; the same call succeeds via curl). The script retries each call up to 5 times on a fresh connection and records the attempt count per call in the raw file.")
        lines.append("- The genesis block is read from the same RPC endpoint; an independent archive source was not cross-checked.")
        lines.append("- Block timestamps are the values reported by the chain, not independently measured wall-clock times.")
        lines.append("- A PASS here means network identity is consistent at retrieval time; it does not verify any other module.")
        lines.append("- This run's outputs live in runs/%s/ and are never overwritten: the script refuses to reuse an existing run directory and creates every file in exclusive mode." % run_id)
        lines.append("")
        write_text_exclusive(report_path, "\n".join(lines))

        # SHA256 checksums for every file this run produced, written last.
        # The manifest includes the verification report itself, so any
        # later change to any file in this run is detectable. The manifest
        # does not hash itself: a file cannot contain its own hash.
        # Verify from inside the run directory with:
        #   sha256sum -c datasets/01_network_identity_checksums.sha256
        raw_sha = sha256_hex(raw_path)
        metadata_sha = sha256_hex(metadata_path)
        dataset_sha = sha256_hex(dataset_path)
        report_sha = sha256_hex(report_path)
        manifest_lines = [
            "%s  %s\n" % (raw_sha, "raw-data/rpc-responses/01_network_identity_raw.json"),
            "%s  %s\n" % (metadata_sha, "datasets/01_network_identity_metadata.json"),
            "%s  %s\n" % (dataset_sha, "datasets/01_network_identity.csv"),
            "%s  %s\n" % (script_sha256, "scripts/01_network_identity.py"),
            "%s  %s\n" % (report_sha, "findings/verified-facts/01_network_identity_verification.md"),
        ]
        write_text_exclusive(checksums_path, "".join(manifest_lines))
    except FileExistsError as exc:
        print("REFUSED: %s already exists - refusing to overwrite evidence." % exc.filename, file=sys.stderr)
        print("No further files were written for this run.", file=sys.stderr)
        return 2
    except OSError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2

    print("module: 01_network_identity")
    print("script_version: %s" % SCRIPT_VERSION)
    print("run_id: %s" % run_id)
    print("run_dir: runs/%s" % run_id)
    print("rpc: %s" % RPC_URL)
    print("retrieved_at_utc: %s" % retrieved_at_utc)
    print("chain_id: %s (%s)" % (chain_id, chain_id_hex))
    print("latest_block: %s (%s)" % (latest_number, values["latest_block_hex"]))
    print("latest_block_hash: %s" % latest_hash)
    print("latest_block_timestamp_utc: %s" % latest_ts_iso)
    print("genesis_hash: %s" % genesis_hash)
    print("genesis_block_timestamp_utc: %s" % genesis_ts_iso)
    print("status: %s (%d/%d checks)" % (status, checks_passed, len(checks)))
    for name, ok, detail in checks:
        print("check %s: %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    print("sha256 raw: %s" % raw_sha)
    print("sha256 metadata: %s" % metadata_sha)
    print("sha256 dataset: %s" % dataset_sha)
    print("sha256 script: %s" % script_sha256)
    print("sha256 report: %s" % report_sha)
    print("raw: %s" % raw_path)
    print("dataset: %s" % dataset_path)
    print("metadata: %s" % metadata_path)
    print("checksums: %s" % checksums_path)
    print("report: %s" % report_path)
    print("script_copy: %s" % script_copy_path)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
