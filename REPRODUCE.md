# Reproduce — how to re-run these audits

"Read-only" here means the **blockchain interaction** is read-only: no
transactions are sent, nothing is signed, no wallet or key is used, and
nothing on-chain is changed. Reproduction itself **does write local
artifacts**: a Module 01 run creates a new `runs/<run_id>/` directory, the
decode step writes decoded JSON files, and rebuilding the video writes new
media files. What is never written over is **saved raw evidence**: raw JSON
is written once in exclusive mode and then chmod 444, and the fetch/decode
scripts refuse to overwrite existing evidence (see §2–§3). Treat a refusal
as the design working, not as a failure.

## Prerequisites

- `curl`, `python3` (stdlib only — no pip packages), `sha256sum`
- GNU sed (the `sed -i` in-place edits in §3 and §4 need GNU sed; BSD/macOS
  `sed` requires a backup-suffix argument and fails on the commands as
  written).
- Shell snippets use POSIX `sh` only — no Bash-only syntax. (The earlier
  process-substitution loop in §2 was replaced by the Python comparator
  in §2C, so no `diff <(...)` remains in this guide.)
- `ffmpeg` 8.x (only for rebuilding the video)
- Optional, PDF rebuild only: `bun` + the render script at
  `/opt/muse/assets/artifacts/scripts/render_audit.mjs` (the PDFs in this
  repo are review copies; rebuilding them is not required to verify the
  evidence)

## 1. Module 01 — Network Identity Audit

```bash
cd ~/workspace/rayls-enygma-public-testnet-research
python3 scripts/01_network_identity.py
```

- Creates a NEW run directory `runs/<UTC-timestamp>/` (existing runs are
  never overwritten; the script refuses collisions).
- Expected: exit 0, status PASS. A new run will show a NEW latest block and
  a new retrieval time — that is normal on a live chain. What must match the
  recorded runs: chain ID 7295799, genesis block 0 with hash
  `0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545`,
  and the check structure (13 checks in v2.0.1).
- Verify a recorded run (v2.0.1 manifests only — the v1.0.0 manifest used
  bare filenames, see `runs/README.md`):

```bash
cd runs/20261121T063327Z   # or 20261121T063234Z
sha256sum -c datasets/01_network_identity_checksums.sha256
# expect: 5/5 OK
```

## 2. Week 2 TX audit — fetch (re-fetch)

Target transaction (full hash):
`0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb`
(block 24825928, Rayls Public Testnet, chain ID 7295799, RPC
`https://testnet-rpc.rayls.com`, Explorer
`https://testnet-explorer.rayls.com`).

The raw package holds 9 files: 5 script-generated + 4 manual. The fetch
script regenerates only the 5; the other 4 come from manual steps and the
script never produces them — do not mix them up.

**Parameters (all requests):**

- RPC `eth_getTransactionByHash` / `eth_getTransactionReceipt`: params
  `[<full tx hash above>]`. `eth_getBlockByNumber`: params `["0x17ad048",
  false]` (0x17ad048 = block 24825928). `eth_chainId`, `eth_blockNumber`:
  no params.
- RPC `eth_getLogs` (logs.json cross-check): `fromBlock` = `toBlock` =
  `"0x17ad048"` (block 24825928 only), addresses
  `0x07e17E17e17E17e17e17e17E17E17E17E17e17EA` (RLS token proxy),
  `0xca11bde05977b3631167028862be2a173976ca11` (Multicall3),
  `0x9C5Ad5e5Ea5b5910E7fD1E1CC7b70ce0e4bF06c2` (SharedVault proxy).
- RPC `eth_getCode` (contracts.json):
  `0x9c5ad5e5ea5b5910e7fd1e1cc7b70ce0e4bf06c2`,
  `0xad9667049f14d1757d147f652c41dc241c57091c` (vault implementation),
  `0x07e17E17e17E17e17e17e17E17E17E17E17e17EA`,
  `0xca11bde05977b3631167028862be2a173976ca11`,
  `0xA473291FFb33e2276F364fAE169f03c4406719e9` (registry); plus
  `eth_getStorageAt` on the vault proxy, EIP-1967 implementation slot
  `0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`.
  (The full call list with params is stored in `contracts.json` itself,
  under `calls[]`.)
- Explorer `gettxinfo` / `gettxreceiptstatus` (from the stored requests in
  `explorer.json`, `calls[].endpoint`; TX-AUDIT-REPORT.md §1 names the same
  two calls):
  `https://testnet-explorer.rayls.com/api?module=transaction&action=gettxinfo&txhash=0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb`
  `https://testnet-explorer.rayls.com/api?module=transaction&action=gettxreceiptstatus&txhash=0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb`
- Explorer txlist (relayer `0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8`,
  from the stored requests in `explorer-relayer-txlist.json`,
  `calls[].endpoint`):
  `https://testnet-explorer.rayls.com/api?module=account&action=txlist&address=0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8&startblock=24825900&endblock=24826000&sort=asc`
  and the same with `startblock=24825800&endblock=24826200` (both return
  the same 2 txs).
- Explorer getLogs (registry `0xA473291FFb33e2276F364fAE169f03c4406719e9`,
  topic0 `0x74d8e560d2e870c35b35dc882df2a5c96e2bf1cdb5ef6dd2f9cb433c8d048853`,
  UsernameSet), 9 chunks of 200,000 blocks over 23212003–24910000:
  23212003–23412002 (28 logs), 23412003–23612002 (26), 23612003–23812002 (9),
  23812003–24012002 (0), 24012003–24212002 (25), 24212003–24412002 (46),
  24412003–24612002 (33), 24612003–24812002 (28), 24812003–24910000 (0);
  195 logs total.
- Related tx `0xacc7d175e08b72766796807b34141185e461fcec0d72df6ccb8dc621406509b2`
  (block 24825932 = `0x17ad04c`): `eth_getTransactionByHash` /
  `eth_getTransactionReceipt` with `[<that hash>]`, `eth_getBlockByNumber`
  with `["0x17ad04c", false]` — the same call pattern as the target tx's
  files, whose requests are fully recorded there.

**A. Script-generated files (5):** `transaction.json`, `receipt.json`,
`block.json`, `logs.json`, `contracts.json` (all RPC calls).

```bash
# 1. Start from a CLEAN scratch directory. If /tmp/rayls-repro already
#    exists (e.g. from an earlier attempt), remove it first — `cp -r`
#    into an existing directory creates a NESTED copy instead of
#    replacing it, and the paths below would then point at stale files.
rm -rf /tmp/rayls-repro
cp -r ~/workspace/rayls-enygma-public-testnet-research /tmp/rayls-repro

# 2. The copy already contains the saved raw/ directory, and the fetch
#    script refuses to overwrite it (exit 2, before any RPC call — see
#    below). Delete raw/ INSIDE THE COPY ONLY (the original is untouched),
#    then run the fetch script in the copy. This regenerates ONLY the 5
#    script files above — the 4 manual files (§2B) will be absent from
#    the fresh copy. That is EXPECTED, not evidence loss.
rm -rf /tmp/rayls-repro/experiments/transactions/tx-09edab2b/raw
python3 /tmp/rayls-repro/scripts/tx_audit_09edab2b.py
```

- The script (`scripts/tx_audit_09edab2b.py` v1.1.0) resolves the package
  directory from its own location (`__file__`), so a scratch copy writes
  into the copy, not into the original. It writes raw files once, exclusive
  mode, then `chmod 444`. In place it exits 2 with a REFUSAL (raw directory
  already exists) — that is the design, not a failure. The refusal happens
  at `os.makedirs(raw_dir, exist_ok=False)` before any RPC call, so the
  check is network-free (tested 22 Nov 2026: exit 2, no calls made).

**B. Manual files (4):** `explorer.json` (gettxinfo +
gettxreceiptstatus), `explorer-relayer-txlist.json` (txlist, 2 bounded
queries), `registry-usernames.json` (getLogs, 9 chunks),
`related-tx-0xacc7d175.json` (3 RPC calls for the related tx). These were
made by manual curl steps documented in `TX-AUDIT-REPORT.md` — the fetch
script does not produce them. Re-fetch them with the IDENTICAL parameters
listed above and compare each fresh `result` payload against the saved
`calls[].response.result` in the original file — not a whole-file diff
(the wrapper fields — `finding`, `logs`, `total_logs`, `failed_attempts` —
are hand-assembled records derived from those payloads).

- `related-tx-0xacc7d175.json` — origin: the related tx was found by
  listing the relayer's txs in blocks 24825800–24826200 (exactly 2 txs: the
  target and the fee settlement; see `TX-AUDIT-REPORT.md` §6–§7). Its 3
  calls are manual curl to `https://testnet-rpc.rayls.com`
  (`eth_getTransactionByHash`, `eth_getTransactionReceipt`,
  `eth_getBlockByNumber`, retrieved 2026-11-21T16:25:18Z). Limitation: the
  call records store only `method` + `endpoint` — the request params were
  NOT saved. The re-fetch parameters are reconstructed from the file's own
  top-level fields (`tx_hash` + `expected_block` 24825932, see the list
  above). The file's `checks[]` is EMPTY — no checks were recorded for it,
  so a re-fetch can re-verify its payloads but not a checks array. It is
  NOT outside re-fetch scope: the data is historical and the calls are
  repeatable; only the parameter reconstruction is documented here instead
  of read from the call records.
- `registry-usernames.json` — the 9 chunk calls store only `fromBlock` /
  `toBlock` / `result_count` (no per-call endpoint); the full logs live in
  the file's top-level `logs` array (195 entries). Re-fetch the 9 chunks
  with the ranges above, concatenate the results in chunk order, and
  compare the whole list against the saved `logs` array.
- For a single fresh response (RPC or Explorer), compare its `result`
  against the saved call's `result` with:

```bash
python3 -c "
import json, sys
saved = json.load(open(sys.argv[1]))
fresh = json.load(open(sys.argv[2]))
call = saved['calls'][int(sys.argv[3])]
print('MATCH' if fresh.get('result') == call['response'].get('result') else 'DIFFERS')
" <saved-manual-file> /tmp/fresh.json <call-index>
```

The full manual comparison is done by comparator v2.1.1 (§2C) in one run over
all 9 files. It reads the fresh manual payloads from a directory laid out
exactly as: `explorer-0.json`, `explorer-1.json` (Explorer GETs, in call
order), `txlist-0.json`, `txlist-1.json`, `registry-chunk-0.json` …
`registry-chunk-8.json` (one file per chunk, in chunk order),
`related-0.json`, `related-1.json`, `related-2.json` (RPC POSTs, in call
order). The one-liner above remains as a spot check for a single call.

**C. What `diff` will and will not show — comparison criteria.**

A plain `diff -r` on the two raw/ directories WILL show differences, and
that is normal. Differences fall into three explicit categories (below).
The first is transport metadata:

- `retrieved_at_utc` (top level, every file) — WILL differ on every re-fetch.
- `calls[].attempts` — MAY differ (retries depend on transport that day).

Everything else is compared in three explicit categories — nothing is
silently dropped (comparator v2, below):

1. **Stable historical payload — MUST match** as parsed JSON values (see
   §5): every `calls[].response.result` payload (tx object, receipt, logs,
   block, contract code/storage, Explorer results), `calls[].method` /
   `params` / `request` (request ids are deterministic — the payload is
   built once per call and retries resend the same id), `validation.ok`,
   and the whole `checks[]` array (names, pass/fail, details — no check
   quotes an attempt count). The comparator parses both files and compares
   values, not raw bytes: whitespace and object key order are NOT compared;
   types and values must be equal; a key present in one file and absent in
   the other is a difference; array item order IS compared.
2. **Dynamic fields — recorded and shown, never compared as history.**
   Exactly two, keyed by (file, method, field path):
   - `eth_blockNumber`: the `response.result` of any call whose method is
     `eth_blockNumber` (in `transaction.json`) is the live current block,
     not historical payload. It is recorded (saved vs fresh value) and
     excluded from the stable comparison.
   - Explorer `confirmations`: the `confirmations` key inside a result
     object is derived from the live tip at fetch time — it was observed
     changing between fetches (the saved file itself holds 44,417 vs
     44,440 for the same tx). It is recorded per call/tx and excluded
     from the stable comparison, but ONLY at two determined locations:
     the `explorer.json` gettxinfo result and each tx object in the
     txlist results (identified by the saved call's `method` string,
     which embeds the Explorer action). A `confirmations` key anywhere
     else (e.g. a gettxreceiptstatus result) is stable data and is
     compared normally. If the field is present on one side only, that
     is reported explicitly as an asymmetric dynamic field AND fails the
     run — it is never silently skipped.
   There is no general tolerance and no wildcard: a same-named key anywhere
   else (e.g. inside a `validation` or `request` object) is evidence and
   still fails the run.
3. **Post-snapshot events (registry only) — counted and listed separately.**
   The registry can only be compared as a historical snapshot up to the
   snapshot tip — the chain tip recorded in the saved `transaction.json`
   (`eth_blockNumber` result at snapshot time: `0x17b79af` = 24,869,295 on
   21 Nov 2026). The comparison is TWO-WAY: every saved log at or below
   the tip must be in the fresh data and identical, AND every fresh log
   at or below the tip must have a match in the saved data — a fresh
   historical log with no saved match fails the run. A duplicated log
   identity (`blockNumber`, `transactionHash`, `logIndex`) in EITHER
   dataset fails the run. Identity is (`blockNumber`, `transactionHash`,
   `logIndex`); content is checked on (`address`, `topics`, `data`) — a
   missing, changed, unexpected, or duplicated log at or below the tip
   fails the run. The comparator does not compare every optional RPC log
   field — only the identity and content fields above. Logs above the tip are post-snapshot activity: counted,
   listed with block/tx/logIndex, and never failing the run.

Explorer envelopes are stable: `status` and `message` are compared for
`explorer.json` and both txlist responses — an unclassified envelope
change fails the run. Registry chunk envelopes are validated, not
ignored: only `1 / OK` with a list result, or `0 / No logs found` with
an empty list, is accepted. Thus chunk 8 may legitimately change from an
empty saved range to a nonempty fresh range, while an API error cannot
masquerade as an empty range. The comparator also rejects
missing/non-list results, unknown/error responses, malformed log
entries, missing required log fields, and invalid hex block numbers.
For related-tx, `jsonrpc` is compared; `id` is NOT — it is a request echo
(the re-fetch used ids 1,2,3; the saved run used 1,1,1).

Do NOT widen the allowed differences to make a check look clean: any
difference outside the two dynamic fields above and the post-snapshot
category is a real finding (e.g. contract code changed, Explorer data
changed) — document it, never normalize it away.

The comparator below (v2.1.1) covers all 9 raw files in one run: the 5
script files plus the 4 manual files. It parses the JSON (no `sed` on raw
text) and normalizes ONLY the two transport fields: top-level
`retrieved_at_utc` and `attempts` inside `calls[]`. It prints PASS/FAIL
per file for the stable payload, a separate DYNAMIC FIELDS section, and a
POST-SNAPSHOT EVENTS section, and exits 1 if ANY stable file differs — a
failure in an early file is never masked by later files passing.

> Note on the embedded code (outside the code block, so the copy stays
> byte-identical): the comparator's own docstring inside the block still
> shows `Usage: python3 compare_raw_v2_1.py …` — a stale filename carried
> over from v2.1.0. Do NOT edit the block for this; run the comparator
> with the command given after the block (`/tmp/compare_raw_v2_1_1.py`).

```bash
cat > /tmp/compare_raw_v2_1_1.py <<'EOF'
#!/usr/bin/env python3
"""Comparator v2.1.1 — re-fetch verification for TX 0x09edab2b (REPRODUCE §2C).

Supersedes v2.1.0. Changes (22 Nov 2026, review round 8):
  P1  Validate every registry chunk envelope and result shape before
      aggregation. Only (status="1", message="OK", result=list) and
      (status="0", message="No logs found", result=[]) are accepted.
      Missing/invalid results, API errors, unknown envelopes, malformed
      log entries, and missing required log fields fail the run. This
      prevents an API failure with an empty result from passing as an
      empty range.
  Earlier v2.1.0 fixes remain: two-way registry matching + duplicate
  detection; location-specific confirmations + asymmetric-field failure;
  Explorer envelope checks; related-tx jsonrpc check (request id excluded).

Categories (unchanged from v2.0.0):
  1. STABLE HISTORICAL PAYLOAD — must match as parsed JSON values.
  2. DYNAMIC FIELDS — recorded and shown, never compared as history:
     * (transaction.json) any call with method == "eth_blockNumber":
       its response.result is the live current block.
     * (explorer.json gettxinfo, txlist tx objects) the "confirmations"
       key, derived from the live tip at fetch time.
     Rules are keyed by (file, method, field path). No general tolerance,
     no wildcard.
  3. POST-SNAPSHOT EVENTS (registry only) — logs with blockNumber above
     the snapshot tip are new chain activity, counted and listed
     separately. They never fail the run.

The snapshot tip is derived from the SAVED transaction.json: the
response.result of the call whose method == "eth_blockNumber" at
snapshot time (0x17b79af = 24869295 on 21 Nov 2026).

Usage:
  python3 compare_raw_v2_1.py <new_script_dir> <old_raw_dir> <new_manual_dir>
  (same layout as v2.0.0 — see its docstring.)

Exit code: 0 iff every stable payload passes and no unclassified
difference exists. Dynamic fields and post-snapshot events never
cause a failure by themselves.
"""
import collections
import copy
import json
import sys

VERSION = "2.1.1"
SCRIPT_FILES = ["transaction.json", "receipt.json", "block.json",
                "logs.json", "contracts.json"]
DYNAMIC_SENTINEL = "<dynamic:live-read>"


def normalize(obj):
    """Remove ONLY transport metadata: top-level retrieved_at_utc and
    attempts inside calls[]. Same-named keys anywhere else are evidence
    and are left untouched."""
    obj = copy.deepcopy(obj)
    obj.pop("retrieved_at_utc", None)
    for call in obj.get("calls", []):
        if isinstance(call, dict) and "attempts" in call:
            call["attempts"] = 1
    return obj


def diff_paths(a, b, path="$"):
    """Value diff with exact paths. a = re-fetch (new), b = saved (old)."""
    if type(a) is not type(b):
        yield f"{path}: type {type(a).__name__} != {type(b).__name__}"
        return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                yield f"{path}.{k}: only in saved"
            elif k not in b:
                yield f"{path}.{k}: only in re-fetch"
            else:
                yield from diff_paths(a[k], b[k], f"{path}.{k}")
    elif isinstance(a, list):
        if len(a) != len(b):
            yield f"{path}: length {len(a)} != {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            yield from diff_paths(x, y, f"{path}[{i}]")
    elif a != b:
        yield f"{path}: {a!r} != {b!r}"


def extract_live_block(obj):
    """Find calls with method == eth_blockNumber, record their
    response.result as dynamic, and replace it with the sentinel so the
    stable diff sees both sides as equal. Returns (obj, dynamics)."""
    dynamics = []
    for i, call in enumerate(obj.get("calls", [])):
        if isinstance(call, dict) and call.get("method") == "eth_blockNumber":
            val = call.get("response", {}).get("result")
            dynamics.append((f"$.calls[{i}].response.result "
                             f"(eth_blockNumber)", val))
            call["response"]["result"] = DYNAMIC_SENTINEL
    return obj, dynamics


def returns_confirmations(call):
    """True only for the determined confirmations locations: the
    gettxinfo result and txlist tx objects. The saved call record's
    `method` string embeds the Explorer action."""
    method = call.get("method", "") if isinstance(call, dict) else ""
    return "action=gettxinfo" in method or "action=txlist" in method


def split_confirmations(result):
    """Remove the dynamic 'confirmations' key from a result object.
    Returns (cleaned, present, value). The caller decides what an
    asymmetric presence means — this function never hides it."""
    if isinstance(result, dict) and "confirmations" in result:
        cleaned = copy.deepcopy(result)
        return cleaned, True, cleaned.pop("confirmations")
    return result, False, None


def log_id(log):
    return (log.get("blockNumber"), log.get("transactionHash"),
            log.get("logIndex"))


def log_content(log):
    return (log.get("address"),
            json.dumps(log.get("topics"), sort_keys=True),
            log.get("data"))


def find_duplicates(logs):
    """Identity keys occurring more than once. A duplicated log identity
    in either dataset is a finding, not a dedup opportunity."""
    counts = collections.Counter(log_id(l) for l in logs)
    return sorted(k for k, c in counts.items() if c > 1)


def validate_registry_chunk(chunk, index):
    """Validate the Explorer envelope before accepting a registry chunk.

    Accepted responses are exactly (1, "OK", list) or
    (0, "No logs found", empty list). This prevents transport/API errors
    with an empty or missing result from being mistaken for an empty range.
    """
    if not isinstance(chunk, dict):
        return None, f"chunk {index}: response is not an object"
    status = str(chunk.get("status"))
    message = chunk.get("message")
    result = chunk.get("result")
    if not isinstance(result, list):
        return None, (f"chunk {index}: result must be a list; "
                      f"got {type(result).__name__}")
    if status == "1" and message == "OK":
        pass
    elif status == "0" and message == "No logs found" and not result:
        pass
    else:
        return None, (f"chunk {index}: unaccepted envelope "
                      f"status={status!r}, message={message!r}, "
                      f"result_count={len(result)}")
    for j, log in enumerate(result):
        if not isinstance(log, dict):
            return None, f"chunk {index} log {j}: entry is not an object"
        required = ("blockNumber", "transactionHash", "logIndex",
                    "address", "topics", "data")
        missing = [key for key in required if key not in log]
        if missing:
            return None, (f"chunk {index} log {j}: missing required "
                          f"field(s) {', '.join(missing)}")
        try:
            int(log["blockNumber"], 16)
        except (TypeError, ValueError):
            return None, f"chunk {index} log {j}: invalid blockNumber"
    return result, None


def main():
    new_dir, old_dir, man_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    stable_failed = 0
    stable_total = 0
    dynamics = []   # (file, location, saved_value, fresh_value, note)
    post_snapshot = []  # fresh registry logs above the tip

    print(f"comparator v{VERSION} — stable / dynamic / post-snapshot")
    print("== STABLE HISTORICAL PAYLOAD ==")

    # ---- 1. Script files (5) ----
    for f in SCRIPT_FILES:
        stable_total += 1
        try:
            with open(f"{new_dir}/{f}") as fh:
                fresh = normalize(json.load(fh))
        except FileNotFoundError:
            stable_failed += 1
            print(f"FAIL {f}: missing in re-fetch")
            continue
        with open(f"{old_dir}/{f}") as fh:
            saved = normalize(json.load(fh))
        # dynamic: eth_blockNumber result (live read, by method)
        fresh, dyn_f = extract_live_block(fresh)
        saved, dyn_s = extract_live_block(saved)
        if len(dyn_f) != len(dyn_s):
            stable_failed += 1
            print(f"FAIL {f}: eth_blockNumber call count differs "
                  f"(fresh {len(dyn_f)} vs saved {len(dyn_s)})")
        for (loc, fv), (_, sv) in zip(dyn_f, dyn_s):
            dynamics.append((f, loc, sv, fv, ""))
        diffs = list(diff_paths(fresh, saved))
        if diffs:
            stable_failed += 1
            print(f"FAIL {f}: {len(diffs)} difference(s)")
            for d in diffs[:10]:
                print("   ", d)
        else:
            print(f"PASS {f}: identical (modulo transport metadata)")

    # ---- 2. Manual files (4) ----
    # 2a. explorer.json — gettxinfo + gettxreceiptstatus
    stable_total += 1
    saved = json.load(open(f"{old_dir}/explorer.json"))
    ok = True
    for i, call in enumerate(saved["calls"]):
        with open(f"{man_dir}/explorer-{i}.json") as fh:
            fresh = json.load(fh)
        # P2: envelope status AND message are stable for historical queries
        for key in ("status", "message"):
            if fresh.get(key) != call["response"].get(key):
                ok = False
                print(f"FAIL explorer.json calls[{i}]: envelope {key} "
                      f"{fresh.get(key)!r} != "
                      f"{call['response'].get(key)!r}")
        fr = copy.deepcopy(fresh.get("result"))
        sr = copy.deepcopy(call["response"].get("result"))
        if returns_confirmations(call):
            # P1: dynamic only at this determined location; asymmetry fails
            fr, f_present, f_val = split_confirmations(fr)
            sr, s_present, s_val = split_confirmations(sr)
            loc = f"calls[{i}].result.confirmations"
            if f_present and s_present:
                dynamics.append(("explorer.json", loc, s_val, f_val, ""))
            elif f_present != s_present:
                ok = False
                side = ("present in re-fetch, missing in saved"
                        if f_present else
                        "present in saved, missing in re-fetch")
                print(f"FAIL explorer.json calls[{i}]: confirmations "
                      f"{side} (asymmetric dynamic field)")
                dynamics.append(("explorer.json", loc + " [ASYMMETRIC]",
                                 s_val, f_val, side))
            else:
                dynamics.append(("explorer.json", loc,
                                 None, None, "absent on both sides"))
        for d in diff_paths(fr, sr, f"$.calls[{i}].result"):
            ok = False
            print(f"FAIL explorer.json calls[{i}]: {d}")
    if ok:
        print("PASS explorer.json: identical (modulo transport metadata "
              "and dynamic confirmations)")
    else:
        stable_failed += 1

    # 2b. explorer-relayer-txlist.json — 2 bounded queries
    stable_total += 1
    saved = json.load(open(f"{old_dir}/explorer-relayer-txlist.json"))
    ok = True
    for i, call in enumerate(saved["calls"]):
        with open(f"{man_dir}/txlist-{i}.json") as fh:
            fresh = json.load(fh)
        # P2: envelope status AND message, per call
        for key in ("status", "message"):
            if fresh.get(key) != call["response"].get(key):
                ok = False
                print(f"FAIL txlist calls[{i}]: envelope {key} "
                      f"{fresh.get(key)!r} != "
                      f"{call['response'].get(key)!r}")
        fr_list = fresh.get("result")
        sr_list = call["response"].get("result")
        if not isinstance(fr_list, list) or not isinstance(sr_list, list):
            ok = False
            print(f"FAIL txlist calls[{i}]: result is not a list")
            continue
        if len(fr_list) != len(sr_list):
            ok = False
            print(f"FAIL txlist calls[{i}]: length "
                  f"{len(fr_list)} != {len(sr_list)}")
            continue
        conf_here = returns_confirmations(call)
        for j, (ftx, stx) in enumerate(zip(fr_list, sr_list)):
            ftx = copy.deepcopy(ftx)
            stx = copy.deepcopy(stx)
            if conf_here:
                ftx, f_present, f_val = split_confirmations(ftx)
                stx, s_present, s_val = split_confirmations(stx)
                loc = f"calls[{i}].result[{j}].confirmations"
                if f_present and s_present:
                    dynamics.append(("explorer-relayer-txlist.json", loc,
                                     s_val, f_val, ""))
                elif f_present != s_present:
                    ok = False
                    side = ("present in re-fetch, missing in saved"
                            if f_present else
                            "present in saved, missing in re-fetch")
                    print(f"FAIL txlist calls[{i}]: confirmations "
                          f"[{j}] {side} (asymmetric dynamic field)")
                    dynamics.append(("explorer-relayer-txlist.json",
                                     loc + " [ASYMMETRIC]",
                                     s_val, f_val, side))
                else:
                    dynamics.append(("explorer-relayer-txlist.json", loc,
                                     None, None, "absent on both sides"))
            for d in diff_paths(ftx, stx, f"$.calls[{i}].result[{j}]"):
                ok = False
                print(f"FAIL txlist calls[{i}]: {d}")
    if ok:
        print("PASS explorer-relayer-txlist.json: identical (modulo "
              "dynamic confirmations)")
    else:
        stable_failed += 1

    # 2c. registry-usernames.json — TWO-WAY identity comparison to tip
    stable_total += 1
    saved = json.load(open(f"{old_dir}/registry-usernames.json"))
    saved_tx = json.load(open(f"{old_dir}/transaction.json"))
    tip = None
    for call in saved_tx.get("calls", []):
        if call.get("method") == "eth_blockNumber":
            tip = int(call["response"]["result"], 16)
    if tip is None:
        print("FAIL registry-usernames.json: snapshot tip not found in "
              "saved transaction.json (no eth_blockNumber call)")
        stable_failed += 1
    else:
        print(f"      snapshot tip (from saved eth_blockNumber): "
              f"{tip} (0x{tip:x})")
        fresh_logs = []
        chunk_errors = []
        for i in range(9):
            try:
                with open(f"{man_dir}/registry-chunk-{i}.json") as fh:
                    chunk = json.load(fh)
            except (FileNotFoundError, json.JSONDecodeError) as exc:
                chunk_errors.append(f"chunk {i}: cannot read valid JSON ({exc})")
                continue
            chunk_logs, error = validate_registry_chunk(chunk, i)
            if error:
                chunk_errors.append(error)
            else:
                fresh_logs.extend(chunk_logs)
        # A missing/failed chunk must never masquerade as an empty range.
        for error in chunk_errors:
            print(f"FAIL registry-usernames.json: {error}")
        # P0: duplicate identity in either dataset fails
        dup_saved = find_duplicates(saved["logs"])
        dup_fresh = find_duplicates(fresh_logs)
        problems = [("invalid registry chunk", error)
                    for error in chunk_errors]
        for k in dup_saved:
            problems.append(("duplicate identity in saved", k))
        for k in dup_fresh:
            problems.append(("duplicate identity in re-fetch", k))
        s_by_id = {log_id(l): l for l in saved["logs"]}
        f_by_id = {log_id(l): l for l in fresh_logs}
        # direction 1: every saved historical log in fresh, identical
        for k, slog in s_by_id.items():
            if int(k[0], 16) > tip:
                problems.append(("saved log above snapshot tip", k))
            elif k not in f_by_id:
                problems.append(("missing in re-fetch", k))
            elif log_content(slog) != log_content(f_by_id[k]):
                problems.append(("changed in re-fetch", k))
        # direction 2 (P0): every fresh historical log in saved
        for k, flog in f_by_id.items():
            bn = int(k[0], 16)
            if bn > tip:
                post_snapshot.append(flog)
            elif k not in s_by_id:
                problems.append(
                    ("fresh historical log with no saved match", k))
        if problems:
            stable_failed += 1
            print(f"FAIL registry-usernames.json: {len(problems)} "
                  f"problem(s) at or below tip {tip}")
            for why, k in problems[:8]:
                print("   ", why, ":", k)
        else:
            print(f"PASS registry-usernames.json: "
                  f"{len(s_by_id)} stable logs identical two-way "
                  f"(at or below tip {tip})")

    # 2d. related-tx-0xacc7d175.json — 3 RPC calls, all historical
    stable_total += 1
    saved = json.load(open(f"{old_dir}/related-tx-0xacc7d175.json"))
    ok = True
    for i, call in enumerate(saved["calls"]):
        with open(f"{man_dir}/related-{i}.json") as fh:
            fresh = json.load(fh)
        if "error" in fresh and fresh["error"] is not None:
            ok = False
            print(f"FAIL related-tx calls[{i}]: RPC error "
                  f"{fresh['error']!r}")
            continue
        # P2 (RPC envelope): jsonrpc is compared; id is NOT — it is a
        # request echo (re-fetch used 1,2,3; saved run used 1,1,1).
        if fresh.get("jsonrpc") != call["response"].get("jsonrpc"):
            ok = False
            print(f"FAIL related-tx calls[{i}]: jsonrpc "
                  f"{fresh.get('jsonrpc')!r} != "
                  f"{call['response'].get('jsonrpc')!r}")
        for d in diff_paths(fresh.get("result"),
                            call["response"].get("result"),
                            f"$.calls[{i}].result"):
            ok = False
            print(f"FAIL related-tx calls[{i}]: {d}")
    if ok:
        print("PASS related-tx-0xacc7d175.json: identical")
    else:
        stable_failed += 1

    # ---- 3. Dynamic fields (recorded, never failing on their own) ----
    print("== DYNAMIC FIELDS (recorded, not compared as history) ==")
    if not dynamics:
        print("  (none)")
    for fname, loc, sv, fv, note in dynamics:
        extra = f" — {note}" if note else ""
        print(f"  {fname} {loc}: saved {sv!r} vs fresh {fv!r}{extra}")

    # ---- 4. Post-snapshot events ----
    print("== POST-SNAPSHOT EVENTS (registry, above tip) ==")
    if not post_snapshot:
        print("  (none)")
    for lg in sorted(post_snapshot, key=lambda l: int(l["blockNumber"], 16)):
        print(f"  block {lg['blockNumber']} = "
              f"{int(lg['blockNumber'], 16):,} | "
              f"tx {lg['transactionHash']} | logIndex {lg['logIndex']}")

    print("== SUMMARY ==")
    print(f"stable: {stable_total - stable_failed}/{stable_total} files PASS")
    print(f"dynamic fields recorded: {len(dynamics)}")
    print(f"post-snapshot events: {len(post_snapshot)}")
    if stable_failed:
        print("RESULT: FAIL (stable historical payload differs)")
        return 1
    print("RESULT: PASS (stable historical payload identical)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
EOF
python3 /tmp/compare_raw_v2_1_1.py \
  /tmp/rayls-repro/experiments/transactions/tx-09edab2b/raw \
  ~/workspace/rayls-enygma-public-testnet-research/experiments/transactions/tx-09edab2b/raw \
  /tmp/refetch-manual
echo "exit code: $?"
```

Comparator v1 (tested 22 Nov 2026, in /tmp, on copies — no original
touched) compared every `result` payload including live reads, so it
exited 1 on the first real re-fetch solely because of `eth_blockNumber`
(see below). Its control tests:
- Positive: all 5 files with `retrieved_at_utc` + `attempts` changed →
  5/5 PASS, exit 0.
- Negative: one hex digit changed in `receipt.json`
  (`blockNumber` `0x17ad049` vs `0x17ad048` — the last digit, `8` → `9`,
  one hex digit, not a whole byte) → FAIL `receipt.json` with the
  exact path `$.calls[0].response.result.blockNumber`, the other 4 files
  PASS, overall exit 1.
- Decoy: same-named keys injected in the wrong place
  (`calls[0].validation.attempts = 999`,
  `calls[0].request.retrieved_at_utc`) → FAIL `transaction.json`
  (`only in re-fetch` for both), exit 1. (The first version of this
  comparator had the "only in saved" / "only in re-fetch" labels inverted;
  the decoy test caught it, the labels were fixed, and scenarios A and C
  were re-run — scenario B's value-diff path was unaffected by the label
  bug.)
- NOTE: v1's exit 1 on the real run is preserved as a fact, not rewritten
  as a PASS. v1's rule (compare everything except transport metadata)
  was stricter than §5's own rule (live reads will differ); v2 resolves
  that tension explicitly instead of hiding it.

Comparator v2.0.0 (tested 22 Nov 2026, in /tmp, on copies — no original
touched; full outputs in `~/workspace/rayls-refetch-2026-11-22/`):
- Real run (saved 21 Nov vs fresh 22 Nov 11:02 WIB): stable **9/9 files
  PASS**, 6 dynamic fields recorded (1 `eth_blockNumber`, 5
  `confirmations`), 4 post-snapshot registry events detected, **exit 0**.
- Negative (same hex-digit change in a fresh `receipt.json` copy): FAIL
  `receipt.json`, 8/9, exit 1 — the stable check still catches it.
- Decoy (same injected keys as v1): FAIL `transaction.json` (2
  differences), exit 1.
- Dynamic-only (fresh `confirmations` changed to `999999` and fresh
  `eth_blockNumber` changed): stable 9/9 PASS, exit 0 — the changed
  values appear in the DYNAMIC FIELDS section, not as failures.
- Manual mismatch (fresh txlist `gasUsed` changed; fresh registry chunk-0
  log `data` changed): FAIL txlist (`$.calls[0].result[0].gasUsed`) and
  FAIL registry (1 changed), 7/9, exit 1.
- GAPS found in v2.0.0 on review (22 Nov, round 7): registry comparison
  was one-way only (saved → fresh) and silently dropped duplicate log
  identities; the `confirmations` rule was applied wherever the key
  appeared and asymmetric presence was silently skipped through `zip`;
  txlist envelopes were not checked at all. These are fixed in v2.1.0
  below; v2.0.0's test results above are unchanged.

Comparator v2.1.0 (tested 22 Nov 2026, in /tmp, on copies — no original
touched; full outputs in `~/workspace/rayls-refetch-2026-11-22/`):
- Real run (same saved vs fresh pair): stable **9/9 files PASS**,
  6 dynamic fields recorded, 4 post-snapshot registry events detected,
  **exit 0**. The registry PASS is now two-way
  ("195 stable logs identical two-way").
- New negative (fresh registry log injected at block 23,212,110, at or
  below the tip): FAIL registry ("fresh historical log with no saved
  match"), 8/9, exit 1.
- New negative (exact duplicate of a chunk-0 log appended to the fresh
  chunk): FAIL registry ("duplicate identity in re-fetch"), 8/9,
  exit 1.
- New negative (`confirmations` deleted from fresh gettxinfo only): FAIL
  explorer.json ("present in saved, missing in re-fetch (asymmetric
  dynamic field)"), 8/9, exit 1 — and the DYNAMIC FIELDS section shows
  it as `[ASYMMETRIC]`, not as a normal match.
- New negative (explorer message "OK" → "NOTOK"; txlist status
  "1" → "0"): FAIL explorer.json (envelope message) and FAIL txlist
  (envelope status), 7/9, exit 1.
- Retained: receipt hex-digit FAIL exit 1; decoy FAIL exit 1;
  dynamic-only 9/9 PASS exit 0; txlist `gasUsed` FAIL exit 1; registry
  log `data` change FAIL exit 1.
- The v2.1.0 real-run result above is NOT rewritten; it remains a
  historical result.

Comparator v2.1.1 (patch from ChatGPT, SHA-256 verified 22 Nov 2026;
canonical file `compare_raw_v2_1_1.py`; embedded verbatim below):
- Change: every registry chunk envelope and result shape is validated
  before aggregation (see §2C). v2.1.0's two-way matching, duplicate
  detection, confirmations, and envelope rules are unchanged.
- DEFECT in the delivered patch (reported as-is, not hidden): the
  supplied regression test
  (`test_registry_chunk_validation_v2_1_1.py`) imports
  `compare_raw_v2_1.py` (v2.1.0) instead of `compare_raw_v2_1_1.py`, so
  it crashes with
  `AttributeError: module 'comparator' has no attribute
  'validate_registry_chunk'` (exit 1) and does NOT test v2.1.1 as
  delivered. The same 8 focused cases run against the actual v2.1.1
  module pass 8/8. The test file was left byte-identical (hash
  preserved); the filename reference needs fixing by the patch author
  (or an explicit decision by Anara) before the regression test can be
  claimed passing. v2.1.1 is therefore NOT marked certified on the
  strength of the delivered test file alone.
- Integrated tests (22 Nov, same saved vs fresh pair, /tmp copies):
  real run stable **9/9 PASS, exit 0** (6 dynamics, 4 post-snapshot
  events); missing `result` FAIL; API-error empty chunk FAIL; unknown
  envelope FAIL; non-list result FAIL; malformed log FAIL; invalid hex
  `blockNumber` FAIL; failed chunk 8 FAIL (even though chunk 8 is
  expected to hold the 4 post-snapshot events); fresh historical log
  below tip FAIL; duplicate identity FAIL; asymmetric `confirmations`
  FAIL; Explorer message/status FAIL; receipt hex-digit FAIL; decoy
  FAIL; txlist `gasUsed` FAIL; registry log `data` FAIL; dynamic-only
  9/9 PASS exit 0.
- Minor: the v2.1.1 docstring's Usage line still says
  `compare_raw_v2_1.py` (stale filename from v2.1.0); the file itself is
  embedded verbatim and the command in this document uses the correct
  filename.
- **RESOLVED 22 Nov 12:27 WIB:** ChatGPT supplied a fixed regression
  test (one line changed: the import now points to
  `compare_raw_v2_1_1.py`; SHA-256 `e159a96f…` verified before use).
  The fixed file replaced `test_registry_chunk_validation_v2_1_1.py`;
  the original defective file is preserved as
  `test_registry_chunk_validation_v2_1_1_original_defective.py`
  (SHA-256 `d2e96c7f…`) as evidence of the initial patch defect. Run
  from the same directory as the v2.1.1 comparator: **8/8 focused
  cases PASS, exit 0** (stdout in
  `~/workspace/rayls-refetch-2026-11-22/v211-regression-test-fixed.log`).
  Comparator v2.1.1 hash unchanged (`bfef1f66…`); raw evidence 9/9 SHA
  unchanged before/after; v1 and v2.1.0 files and results untouched;
  verifier 23/23 PASS. The certification decision is Anara's.
- **CERTIFIED 22 Nov 12:33 WIB (Anara's decision):** comparator v2.1.1
  **PASSES CERTIFICATION** for the re-fetch validation scope tested in
  this round: regression test 8/8 PASS, real run 9/9 PASS, all 15
  integrated negative tests rejected as expected, dynamic-only PASS,
  TX verifier 23/23 PASS. Comparator and raw-evidence hashes intact.
  The import defect in the regression test is resolved; the original
  file is kept as evidence. **Scope: this certification applies ONLY
  to comparator v2.1.1 and the recorded test scope — NOT to the whole
  repo and NOT to all Rayls audit claims.** The comparator must not be
  changed again without a new review round. The TX-package TODO
  re-fetch checkbox is NOT checked by this certification; stage 1
  close-out remains a separate decision by Anara.

- Re-fetch status: **RUN 22 Nov 2026 11:02 WIB** (retrieved_at_utc
  2026-11-22T04:02:07Z). Results: `~/workspace/rayls-refetch-2026-11-22/REFETCH-REPORT-2026-11-22.md`
  (with a correction note for three misgrouped block numbers, verified in
  `~/workspace/rayls-refetch-check-2026-11-22/CHECK-REPORT-2026-11-22.md`).
  Stable historical payload identical (v2.1.1 exit 0); v1's exit 1 on the
  same run was solely the live `eth_blockNumber` read.


## 3. Week 2 TX audit — decode + verify

```bash
cd ~/workspace/rayls-enygma-public-testnet-research
python3 scripts/verify_tx_audit_09edab2b.py
# expect: 23/23 checks PASS, exit 0
```

- The verifier (v1.0.1) is independent: it does not import the fetch or
  decode scripts. It re-reads the evidence from disk, recomputes every
  SHA-256 against `manifest.json`, and re-derives the cross-consistency
  facts (block numbers, tx hash, log counts, statement[8] = 4.416 RLS,
  ciphertext SHAs, registry resolutions, fee). Its repo path is also
  hard-coded (`REPO = os.path.expanduser("~/workspace/rayls-enygma-
  public-testnet-research")`, line 46): running a scratch copy's verifier
  still checks the ORIGINAL evidence. Always run it in place, as in the
  command above.
- The decode script (`scripts/decode_tx_09edab2b.py` v1.0.0) reads raw files
  only (no network) and writes decoded outputs. Its package path is
  hard-coded to this repository (`PKG = os.path.expanduser("~/workspace/
  rayls-enygma-public-testnet-research/experiments/transactions/tx-09edab2b")`,
  line 35) — so running a scratch copy of the script AS-IS still reads
  and writes the ORIGINAL repository, not the copy. Tested 22 Nov 2026:
  an unedited scratch copy failed with `FileExistsError` on the original
  `decoded/decoded_events.json` (exclusive mode `x` saved it from being
  overwritten — the failure was the protection working, not a bug).
  Safe procedure for re-running the decode:

```bash
rm -rf /tmp/rayls-repro-decode
cp -r ~/workspace/rayls-enygma-public-testnet-research /tmp/rayls-repro-decode
# Point PKG at the copy (edit the COPY only, never the original script):
sed -i 's|~/workspace/rayls-enygma-public-testnet-research/experiments/transactions/tx-09edab2b|/tmp/rayls-repro-decode/experiments/transactions/tx-09edab2b|' \
  /tmp/rayls-repro-decode/scripts/decode_tx_09edab2b.py
# The copy already contains the decoded outputs; delete them IN THE COPY:
rm /tmp/rayls-repro-decode/experiments/transactions/tx-09edab2b/decoded/decoded_events.json \
   /tmp/rayls-repro-decode/experiments/transactions/tx-09edab2b/decoded/audit_summary.json
python3 /tmp/rayls-repro-decode/scripts/decode_tx_09edab2b.py
# Compare against the saved decoded files:
diff /tmp/rayls-repro-decode/experiments/transactions/tx-09edab2b/decoded/decoded_events.json \
     ~/workspace/rayls-enygma-public-testnet-research/experiments/transactions/tx-09edab2b/decoded/decoded_events.json
diff /tmp/rayls-repro-decode/experiments/transactions/tx-09edab2b/decoded/audit_summary.json \
     ~/workspace/rayls-enygma-public-testnet-research/experiments/transactions/tx-09edab2b/decoded/audit_summary.json
```

  Tested 22 Nov 2026: the copy's outputs were byte-identical to the saved
  decoded files (`diff` empty), and the originals' SHA-256 were unchanged
  afterwards (`5a8ad453…`, `19c3a36e…`). Do NOT edit `PKG` in the original
  script — it is covered by the manifest.

## 4. Week 2 video — rebuild

Inputs (in this repo): source footage + VO in `raw-data/videos/`,
`build_subs.py`, `build_video_v2.py` in
`experiments/testnet-journeys/week2-private-payment/`.

**Limitation — read before rebuilding:** `build_subs.py` and
`build_video_v2.py` are archived verbatim, but both hard-code the ORIGINAL
workdir (`/home/hatch/workspace/enygma-week2-video`): `build_subs.py`
writes `subs.ass` there (line 137), and `build_video_v2.py` reads segments
and `zoom_long.mp4` from there (lines 2–4). Running them from the repo
journey folder as-is does NOT rebuild from the repo — it writes/reads the
old workdir. The video intermediates (`segments_v2/`, `zoom_long.mp4`,
`video_only_v2.mp4`) are NOT in this repo (see `INDEX.md` §9). So a full
video rebuild from this repo alone is NOT currently possible. What IS
reproducible from the repo:

- Regenerating `subs.ass` — TESTED 22 Nov 2026: copy the repo to scratch,
  edit the two hard-coded output paths in the COPY of `build_subs.py`
  (lines 137 and 142) to point at the copy's journey folder, delete the
  copy's `subs.ass`, run the copy. Result: 44 cues, 0 bare RLS, 16 $RLS,
  @kittynim 3, @kittymin 0 — and the regenerated file was byte-identical
  to the saved `subs.ass` (`diff` empty; SHA-256 `f9aa42fa…`). The originals
  (repo + old workdir) were unchanged afterwards. The script is stdlib-only
  (`import re`) and all subtitle data lives in the script itself, so the
  regeneration is deterministic. Exact commands (tested 22 Nov 2026):

```bash
rm -rf /tmp/rayls-repro-subs
cp -r ~/workspace/rayls-enygma-public-testnet-research /tmp/rayls-repro-subs
sed -i 's|/home/hatch/workspace/enygma-week2-video/subs.ass|/tmp/rayls-repro-subs/experiments/testnet-journeys/week2-private-payment/subs.ass|g' \
  /tmp/rayls-repro-subs/experiments/testnet-journeys/week2-private-payment/build_subs.py
rm /tmp/rayls-repro-subs/experiments/testnet-journeys/week2-private-payment/subs.ass
python3 /tmp/rayls-repro-subs/experiments/testnet-journeys/week2-private-payment/build_subs.py
diff /tmp/rayls-repro-subs/experiments/testnet-journeys/week2-private-payment/subs.ass \
     ~/workspace/rayls-enygma-public-testnet-research/experiments/testnet-journeys/week2-private-payment/subs.ass
# expected: cues: 44, bare RLS occurrences: 0, $RLS occurrences: 16,
# @kittynim: 3 @kittymin: 0, NBSP in file: False, and an empty diff.
# delete the scratch copy afterwards: rm -rf /tmp/rayls-repro-subs
```
- The final mux: the exact ffmpeg recipe is in `QA-REPORT-V2.md`
  (video-only track + VO mp3, audio adelay=800 ms, volume ×2.0,
  alimiter=0.89, subtitles burned in via the ass filter, libx264 CRF 20,
  AAC, +faststart → 1280×720 final; 1080p: ffmpeg lanczos scale to
  1920×1080, CRF 18, audio copied). The video-only track it needs is NOT
  in this repo, so the mux can only be re-run once that track is rebuilt
  (which needs the intermediates above). The final 720p/1080p files in the
  repo are the reference outputs for that mux.

- The 1080p file is an upscale of the 720p master (no new detail).
- The source footage's native audio is effectively silent (-91 dB); no
  audio bed was mixed. The VO is used as-is, never regenerated.

### Public sanitized versions (22 Nov 2026)

The public finals and spelling-check frames are sanitized copies: the
originals still show truncated Enygma Spend/View key fragments (the
`@kittynim` account header), so the originals are LOCAL-ONLY
(gitignored) and the sanitized versions are the committed files.

- Detection: 1 fps frames from each final were compared (grayscale,
  key-line band) against the `chk-21`/`chk-22` captures. The key line
  appears in 5 ranges: t 20–24, 82–88, 109–115, 138–144, 176–185.533 s
  (identical frame numbers in both resolutions; verified by viewing one
  frame per range plus a control frame at t=60 s with no blur).
- Video blur (ffmpeg, re-encode libx264 CRF 18, preset medium, audio
  copied): full-width boxblur of the header band — 1080p: crop
  `iw:175:0:85`, `boxblur=25`, overlay at `0:85`; 720p: crop
  `iw:116:0:57`, `boxblur=17`, overlay at `0:57` — enabled only during
  the 5 ranges above. Everything outside the band and the ranges is the
  original content (re-encoded, so bytes differ; duration 185.533 s and
  audio unchanged).
- Screenshot blur (PIL): `chk-21-public.jpg` — GaussianBlur r=25, box
  x 585–1315, y 180–252; `chk-22-public.jpg` — same radius, box x 585–1315,
  y 90–162. Verified by viewing: the key line is unreadable; balances,
  EVM address, and the rest of the UI are intact.
- Originals (hashes in the journey manifest): final 720p `49a1bc13…`,
  final 1080p `b1834d72…`, `chk-21.jpg` `9cb7c0ea…`, `chk-22.jpg`
  `b714aca7…`. They are not overwritten or deleted.

## 5. What "identical" means

- Historical on-chain data (a past tx, receipt, block, log set): on
  re-fetch, the parsed JSON values must match (see §2C). Whitespace and
  object key order are not compared; types and values must be equal; a key
  present in one file and absent in the other is a difference; array item
  order is compared. Any difference other than the two allowed transport
  fields (`retrieved_at_utc`, `calls[].attempts`) must be documented, never
  forced to match. Byte-level identity (exact bytes, checked with `diff`,
  `cmp`, or SHA-256) is a different, stricter claim and applies only to:
  the decode outputs (§3), the regenerated `subs.ass` (§4), and the
  audit-report copy (§6 level 1) — NOT to the TX re-fetch, which uses
  parsed-value comparison.
- Live-chain reads (latest block, block counts): will differ. Compare the
  structure and the method, not the block number. `eth_blockNumber` is a
  live read, not historical payload (§2C rule 2). Explorer `confirmations`
  is a dynamic field derived from the live tip (§2C rule 2). The registry
  is a snapshot valid only up to the snapshot tip (24,869,295 on 21 Nov
  2026); logs above the tip are post-snapshot activity, not mismatches
  (§2C rule 3). Explorer envelope `status`/`message` are compared
  (§2C P2); an asymmetric `confirmations` field fails the run (§2C
  rule 2). Registry chunk envelopes are validated (§2C, v2.1.1).
- Manifests: `sha256sum -c` must pass for every entry. A manifest never
  lists itself (self-reference is impossible); its own hash is recorded in
  the review PDF appendix / the integration report.

## 6. Reproducibility levels (what each step can and cannot repeat)

| level | what | status |
|---|---|---|
| 1 — fully repeatable from local files | TX verifier (23/23); `sha256sum -c` on Module 01 v2.0.1 manifests; decode from saved raw (byte-identical outputs, tested 22 Nov 2026); audit-report copy check (`cmp` byte-identical) | works offline, no network |
| 2 — needs RPC or Explorer | Module 01 fresh run (a new latest block is expected; chain ID + genesis hash must match); TX re-fetch (historical data must match as parsed JSON values; `retrieved_at_utc` + per-call attempt counts will differ; live reads recorded separately) | live chain; re-fetch RUN 22 Nov 2026 11:02 WIB — stable payload 9/9 PASS with comparator v2.1.1 (exit 0) |
| 3 — Depends on external artifacts or mutable sources | demo-bundle download (recorded hashes `d709dc06…`, `7530bbc2…` are 21 Nov snapshots; the live bundle changes); Explorer API responses (1,000-result cap, pagination); video rebuild (needs the old workdir's intermediates + path edits in a scratch copy; see §4) | snapshot-dependent — record the date + hash of what you fetched |
| 4 — Not reproducible from this repository alone | (a) genuinely not found: the 12:30 WIB inventory review (chat only, no file); the 13 Nov demo screen recordings (referenced by hash in the old source register, files not in any inventoried folder). (b) exists outside this repo, not included — NOT lost: the old research repo (19 files, still at `~/workspace/rayls-enygma-research/`) and the baseline technical-evidence PDF (23 pp, 494,423 B, still at `~/workspace/your_files/rayls-enygma-technical-evidence/`) — referenced, not copied | (a) recorded as gaps, not reconstructed. (b) the sources still exist; only their copies are absent here |

A verifier PASS proves the SAVED evidence is internally consistent (hashes
match the manifest; block numbers, tx hash, log counts, statement[8],
ciphertexts, and registry resolutions re-derive). It does NOT prove the
original discovery process was repeated — the Explorer pagination, the
registry sweep, and the bundle download were one-time observations.
Repeating the fetch (§2) is the actual repeat test for the fetch step — it
ran 22 Nov 2026 11:02 WIB (stable payload 9/9 PASS, comparator v2 exit 0;
live reads recorded separately). Do not read a verifier PASS as "the whole search was
re-done".

## 7. Article audit (r3 + addendum F17)

The article audit is the evidence-classified audit of the two-account
experiment written for the article "What Can the Public Actually See
When Two Accounts Make a Private Transfer on Rayls Enygma?". It lives
in `experiments/testnet-journeys/week2-private-payment/`:

- Current: `ARTICLE-AUDIT-2026-11-22-r3.md` (61,062 B,
  SHA-256 `709565aca40b32a5061d2bfd0513777b5674fd01f5ce230f1f7f8bf7720e327e`).
  English translation (23 Nov 2026) of the frozen Indonesian source
  (59,742 B, SHA-256 `6a1be437ce51227286f23861615781c01d8e394c5a3b07ea34262ba785c6638f`,
  retained privately).
- Addendum: `ARTICLE-AUDIT-2026-11-22-addendum-f17.md` (18,593 B,
  SHA-256 `f3f165500761f6c67d25a28da270f78c1a6f60fd606a310620f48b0047b0dfb1`).
  English translation (23 Nov 2026) of the frozen Indonesian source
  (17,777 B, SHA-256 `b8e64ffff4c5a028ffc036994b8ff66e9ba6eed7a8ee36fa1b6ca476fd1c347a`,
  retained privately)
  — §6 F17 split (F17a: statement[3–7] = verified fact; F17b:
  statement[8] integer 4.416 × 10¹⁸ = verified fact, RLS unit =
  interpretation, "total fee" = inference) + pre-commit content and
  publication-suitability checks (including the sanitization recorded
  in §4 above and the ticket-draft exclusion).
- Superseded: r1 and r2 (local record only, NOT committed).
- The audit is a report, not a re-runnable step: its numbers re-derive
  from the TX package (§2–§3) and the journey video (§4). It does not
  change raw evidence, the comparator, or the video/VO originals.

## 8. Datasets + audit_report.json (root, 22 Nov 2026)

Tabular datasets derived deterministically from the TX package JSONs
(`experiments/transactions/tx-09edab2b/`), plus a machine-readable summary
at the repo root. Added in the Phase 1 restructure; no raw evidence was
changed to produce them.

### What exists

| File | Rows | Source | Rule |
|---|---|---|---|
| `datasets/tx_logs.csv` | 7 | `raw/logs.json` + `decoded/decoded_events.json` | One row per log, ordered by logIndex; event name + decoded fields from the decoded file |
| `datasets/registry_usernames.csv` | 195 | `raw/registry-usernames.json` | username = ABI-decode of `data` (offset 0x20, length N, N ASCII bytes); address = topics[1] last 20 bytes |
| `datasets/statement.csv` | 10 | `raw/transaction.json` (calldata, re-parsed) + `decoded_events.json` + r3 §4.1/F17 labels | One row per statement word; classifications from r3/F17, NOT from the old JSON labels |
| `datasets/relayer_txs.csv` | 2 | `raw/explorer-relayer-txlist.json` | Deduplicated by tx hash (the 2 calls return the same 2 txs; only `confirmations` differs between calls — call-time metadata, excluded) |
| `audit_report.json` | — | 11 JSON sources (see `datasets/build_datasets.py`) | Generated; `integrity` (PASS = data integrity + internal consistency only) vs `findings` (each finding classified) |

### Reproduce

```bash
# Rebuild everything from the JSON sources (refuses to overwrite: delete
# the outputs first, in a scratch copy — never in the committed tree):
python3 datasets/build_datasets.py
# expect: build_datasets: OK; 7 / 195 / 10 / 2 rows; manifests TX 20/20, journey 16/16

# Verify the committed files without rebuilding:
python3 datasets/verify_datasets.py
# expect: 9/9 checks PASS, exit 0

# Check the checksums file:
sha256sum -c datasets/datasets_checksums.sha256
# expect: 5 entries OK (run from datasets/; the audit_report.json entry
# is listed as ../audit_report.json)
```

### What the verifier does NOT do

`verify_datasets.py` re-derives the CSVs and checks `audit_report.json`
field by field, but it does NOT run the TX verifier
(`scripts/verify_tx_audit_09edab2b.py`, 23/23) — run that separately
(§3). It also does not re-run the Module 01 fetch (§1). The
`audit_report.json` `verifier` field is a recorded value from the
22 Nov 2026 run, not a live re-run.

### Governing interpretation

The CSVs and `audit_report.json` use the r3 §4.1 / addendum F17 labels.
The old JSONs' labels are superseded and were deliberately NOT copied:
`audit_summary.json` q8 and `decoded_events.json` `fee.comparison` call
statement[8] "the TOTAL fee … = 4.416 RLS exactly" as a verified fact —
per F17b the integer is a verified fact, the RLS unit is an
interpretation, and "total fee" is an inference. Event names in
`tx_logs.csv` are signature matches against the demo-bundle ABI, not
verified vault source (the deployed vault implementation has no verified
source). See `datasets/README.md` and INDEX.md §11.
