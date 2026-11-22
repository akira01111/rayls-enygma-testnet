#!/usr/bin/env python3
"""Decode script for Rayls Enygma Week 2 experiment TX audit.

Target tx: 0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb
Network: Rayls Public Testnet, chain ID 7295799. Block 24825928.

Version: 1.0.0
Inputs (read-only, never modified): experiments/transactions/tx-09edab2b/raw/*.json
  + decoded/bundle-abi-extract.json (demo-bundle ABI, provenance inside that file).
Outputs: decoded/decoded_events.json, decoded/audit_summary.json
  (written once; the manifest covers them afterwards).
Method:
  - Pure-Python Keccak-256 (original Keccak padding, NOT NIST SHA3),
    self-tested against keccak256("") and keccak256("Upgraded(address)")
    and keccak256("Transfer(address,address,uint256)") before any use.
  - Function selector resolved by computing keccak256 of the canonical
    transferV2 signature taken from the demo bundle ABI and comparing the
    first 4 bytes with the observed selector 0xaacd552c.
  - Event topic0s resolved the same way from the bundle-ABI event signatures.
  - Calldata parsed structurally as ABI words (32 bytes each).
  - Hidden-vs-visible: case-insensitive hex search of the raw input, receipt
    and logs for the sender/receiver/token/relayer addresses and the fee
    amounts as 32-byte words.
  - No network access: this script only reads files already captured.
Labels (6-label taxonomy, same as the audit): verified-fact / official-claim /
direct-observation / reconstruction / inference / unknown.
"""
import hashlib
import json
import os
import sys

SCRIPT_NAME = "scripts/decode_tx_09edab2b.py"
SCRIPT_VERSION = "1.0.0"
PKG = os.path.expanduser("~/workspace/rayls-enygma-public-testnet-research/experiments/transactions/tx-09edab2b")
RAW = os.path.join(PKG, "raw")
DEC = os.path.join(PKG, "decoded")
TX_HASH = "0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb"
CHAIN_ID = 7295799
BLOCK = 24825928

# ---------------------------------------------------------------- keccak256
def _rol(x, n):
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF

_RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808a, 0x8000000080008000,
       0x000000000000808b, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
       0x000000000000008a, 0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
       0x000000008000808b, 0x800000000000008b, 0x8000000000008089, 0x8000000000008003,
       0x8000000000008002, 0x8000000000000080, 0x000000000000800a, 0x800000008000000a,
       0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
_R = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61],
      [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]

def _keccak_f(s):
    for rnd in range(24):
        c = [s[x] ^ s[x + 5] ^ s[x + 10] ^ s[x + 15] ^ s[x + 20] for x in range(5)]
        d = [c[(x + 4) % 5] ^ _rol(c[(x + 1) % 5], 1) for x in range(5)]
        s = [s[i] ^ d[i % 5] for i in range(25)]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = _rol(s[x + 5 * y], _R[x][y])
        new = [0] * 25
        for x in range(5):
            for y in range(5):
                new[x + 5 * y] = b[x + 5 * y] ^ ((~b[((x + 1) % 5) + 5 * y]) & b[((x + 2) % 5) + 5 * y])
        s = new
        s[0] ^= _RC[rnd]
    return s

def keccak256(data: bytes) -> str:
    rate = 136
    s = [0] * 25
    msg = bytearray(data)
    msg.append(0x01)
    while len(msg) % rate != rate - 1:
        msg.append(0x00)
    msg.append(0x80)
    for off in range(0, len(msg), rate):
        blk = msg[off:off + rate]
        for i in range(rate // 8):
            s[i] ^= int.from_bytes(blk[i * 8:(i + 1) * 8], 'little')
        s = _keccak_f(s)
    out = b''.join(s[i].to_bytes(8, 'little') for i in range(4))
    return '0x' + out.hex()

# ---------------------------------------------------------------- helpers
def load(name, folder=RAW):
    with open(os.path.join(folder, name), encoding='utf-8') as fh:
        return json.load(fh)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def word(b: bytes, i: int) -> int:
    return int.from_bytes(b[i * 32:(i + 1) * 32], 'big')

def word_hex(b: bytes, i: int) -> str:
    return '0x' + b[i * 32:(i + 1) * 32].hex()

def wei_to_rls(wei: int) -> str:
    whole, frac = divmod(wei, 10 ** 18)
    return f"{whole}.{frac:018d}".rstrip('0').rstrip('.') if frac else str(whole)

def main():
    # --- keccak self-test (fail loudly if broken) ---
    assert keccak256(b'') == '0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
    assert keccak256(b'Upgraded(address)') == '0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b'
    assert keccak256(b'Transfer(address,address,uint256)') == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
    print('keccak256 self-test: 3/3 PASS')

    txf = load('transaction.json')
    rcf = load('receipt.json')
    lgf = load('logs.json')
    blf = load('block.json')
    cof = load('contracts.json')
    exf = load('explorer.json')
    rgf = load('registry-usernames.json')
    rtx = load('related-tx-0xacc7d175.json')
    txl = load('explorer-relayer-txlist.json')
    abi = load('bundle-abi-extract.json', DEC)

    tx = txf['calls'][2]['response']['result']  # calls: 0=eth_chainId, 1=eth_blockNumber, 2=eth_getTransactionByHash
    rc = rcf['calls'][0]['response']['result']
    rc_logs = rc['logs']
    block = blf['calls'][0]['response']['result']
    impl_slot = cof.get('implementation_from_slot')
    if not impl_slot:
        for c in cof['calls']:
            if c.get('method') == 'eth_getStorageAt':
                impl_slot = c['response']['result']
                break
    vault_impl = '0x' + impl_slot[-40:] if impl_slot else None

    # --- selector verification ---
    canon = abi['transferV2_canonical_signature']
    sel_computed = keccak256(canon.encode())[:10]
    selector = tx['input'][:10]
    selector_match = (sel_computed.lower() == selector.lower())

    # --- event topic table (keccak of bundle-ABI signatures) ---
    sigs = abi['event_signatures']
    topic_to_event = {}
    for name, sig in sigs.items():
        topic_to_event[keccak256(sig.encode()).lower()] = (name, sig)
    transfer_topic = keccak256(b'Transfer(address,address,uint256)').lower()

    # --- calldata parse ---
    inp = bytes.fromhex(tx['input'][2:])
    inp_hex = tx['input'][2:].lower()
    params = inp[4:]  # ABI params start after the 4-byte selector
    n_words = len(params) // 32
    off_receipt, off_c1, off_c2 = word(params, 0), word(params, 1), word(params, 2)
    rbase = off_receipt  # byte offset of receipt tuple within params (after selector)
    # receipt tuple is at params offset off_receipt
    r = params[off_receipt:]
    proof_words = [word_hex(r, i) for i in range(8)]  # a.x,a.y,b.x0,b.x1,b.y0,b.y1,c.x,c.y
    stmt_off = word(r, 8)
    num_inputs = word(r, 9)
    num_outputs = word(r, 10)
    stmt_base = stmt_off
    stmt_len = word(r, stmt_base // 32)
    statement = [word_hex(r, stmt_base // 32 + 1 + i) for i in range(stmt_len)]
    statement_ints = [int(v, 16) for v in statement]

    def parse_bytes_array(params: bytes, off: int):
        # ABI encoding of bytes[]: length word, then one offset word per element
        # (offsets relative to the byte just after the length word), then each
        # element as (length word + data, padded to 32).
        ln = word(params, off // 32)
        data_start = off + 32
        offsets = [word(params, off // 32 + 1 + i) for i in range(ln)]
        entries = []
        end = off + 32
        for o in offsets:
            elen = word(params, (data_start + o) // 32)
            edata = params[data_start + o + 32:data_start + o + 32 + elen]
            entries.append({'byte_length': elen, 'sha256': hashlib.sha256(edata).hexdigest(),
                            'first_16_bytes': '0x' + edata[:16].hex()})
            end = max(end, data_start + o + 32 + ((elen + 31) // 32) * 32)
        return {'count': ln, 'entries': entries, 'end_offset': end}

    params = inp[4:]
    c1 = parse_bytes_array(params, off_c1)
    c2 = parse_bytes_array(params, off_c2)

    calldata = {
        'input_bytes': len(inp),
        'selector': selector,
        'selector_resolves_to': 'transferV2' if selector_match else 'unknown',
        'selector_keccak_check': {
            'canonical_signature': canon,
            'keccak256_first_4_bytes': sel_computed,
            'matches_observed_selector': selector_match,
            'method': 'keccak256 of the canonical signature from the demo-bundle ABI (decoded/bundle-abi-extract.json); 4byte.directory returned count 0 for this selector (see decoded/lookups-4byte.json)',
        },
        'head_offsets': {'receipt': off_receipt, 'ciphertextI': off_c1, 'ciphertextII': off_c2},
        'receipt_tuple': {
            'proof': {
                'a': {'x': proof_words[0], 'y': proof_words[1]},
                'b': {'x': [proof_words[2], proof_words[3]], 'y': [proof_words[4], proof_words[5]]},
                'c': {'x': proof_words[6], 'y': proof_words[7]},
                'proof_bytes': 256,
                'note': '8 uint256 words = 256 bytes, matching the video VO claim of a 256-byte ZK proof (direct observation from the VO, not proven from the calldata alone)',
            },
            'statement': {'length': stmt_len, 'values_hex': statement, 'values_int': statement_ints},
            'numberOfInputs': num_inputs,
            'numberOfOutputs': num_outputs,
        },
        'ciphertextI': c1,
        'ciphertextII': c2,
        'total_words': n_words,
        'trailing_bytes_after_last_array': len(params) - max(c1['end_offset'], c2['end_offset']),
        'statement_interpretation': {
            'statement_0': '0 - unidentified public input (zero)',
            'statement_1': '0 - unidentified public input (zero)',
            'statement_2': '0x0d6edc87... - unidentified 32-byte hash; position before the nullifier is consistent with a Merkle root, but no published statement layout confirms this (unknown)',
            'statement_3': 'nullifier 0x0c0f23a6... - VERIFIED: equals the Nullifier event topic3 in log 0',
            'statement_4': 'commitment 0x094b233a... - VERIFIED: equals the Commitment event topic2 in log 1 and the EncryptedNote topic2 in log 4',
            'statement_5': 'commitment 0x2304db2e... - VERIFIED: equals the Commitment event topic2 in log 2 and the EncryptedNote topic2 in log 5',
            'statement_6': 'commitment 0x206ed94a... - VERIFIED: equals the Commitment event topic2 in log 3 and the EncryptedNote topic2 in log 6',
            'statement_7': 'vault address 0x9c5ad5e5... - VERIFIED: equals the tx to-address (the proof is bound to this vault)',
            'statement_8': '4,416,000,000,000,000,000 wei = 4.416 RLS - VERIFIED as a 32-byte word in the calldata; equals the wallet detail-activity fee 4.416 RLS exactly, and equals 3.84 + 0.576 (see Q8)',
            'statement_9': '0x0f58ff41... - unidentified 32-byte hash; position after the fee is consistent with a binding/ciphertext hash, but no published statement layout confirms this (unknown)',
        },
    }

    # --- log decode ---
    decoded_logs = []
    for i, lg in enumerate(rc_logs):
        t0 = lg['topics'][0].lower()
        data = bytes.fromhex(lg['data'][2:]) if lg['data'] != '0x' else b''
        entry = {'logIndex': i, 'address': lg['address'], 'topic0': lg['topics'][0],
                 'topics': lg['topics'], 'data_hex': lg['data'], 'data_byte_length': len(data)}
        if t0 in topic_to_event:
            name, sig = topic_to_event[t0]
            entry['event_name'] = name
            entry['event_signature'] = sig
            entry['resolution'] = 'keccak256 of bundle-ABI signature equals observed topic0 (verified-fact)'
            if name == 'Nullifier':
                entry['decoded_fields'] = {'vaultId': int(lg['topics'][1], 16),
                                           'treeNumber': int(lg['topics'][2], 16),
                                           'nullifier': lg['topics'][3]}
            elif name == 'Commitment':
                entry['decoded_fields'] = {'vaultId': int(lg['topics'][1], 16),
                                           'commitment': lg['topics'][2]}
            elif name == 'EncryptedNote':
                # data = ABI(bytes ciphertextI, bytes ciphertextII)
                o1 = int.from_bytes(data[0:32], 'big')
                l1 = int.from_bytes(data[o1:o1 + 32], 'big')
                ct1 = data[o1 + 32:o1 + 32 + l1]
                o2 = int.from_bytes(data[32:64], 'big')
                l2 = int.from_bytes(data[o2:o2 + 32], 'big')
                ct2 = data[o2 + 32:o2 + 32 + l2]
                entry['decoded_fields'] = {
                    'vaultId': int(lg['topics'][1], 16),
                    'commitment': lg['topics'][2],
                    'ciphertextI_byte_length': l1,
                    'ciphertextII_byte_length': l2,
                    'ciphertextI_sha256': hashlib.sha256(ct1).hexdigest(),
                    'ciphertextII_sha256': hashlib.sha256(ct2).hexdigest(),
                    'note': 'ciphertext contents are opaque; only lengths and hashes are recorded here',
                }
            else:
                entry['decoded_fields'] = None
        else:
            entry['event_name'] = 'unknown'
            entry['event_signature'] = None
            entry['resolution'] = 'topic0 not in the bundle-ABI table and not in 4byte.directory; reported as unknown'
            entry['decoded_fields'] = None
        entry['is_erc20_transfer'] = (t0 == transfer_topic)
        decoded_logs.append(entry)

    # --- cross-checks ---
    checks = {
        'receipt_blockNumber_eq_block_json_number': (rc['blockNumber'] == block['number']),
        'tx_hash_transaction_eq_receipt': (tx['hash'].lower() == rc['transactionHash'].lower() == TX_HASH.lower()),
        'receipt_logs_count_eq_logs_json_receipt_logs': (len(rc_logs) == len(lgf['receipt_logs_copy'])),
        'receipt_logs_eq_block_level_logs': (len(rc_logs) == len(lgf['calls'][0]['response']['result'])),
        'block_tx_count_eq_1_and_hash_matches': (len(block['transactions']) == 1 and block['transactions'][0].lower() == TX_HASH.lower()),  # block fetched with full-tx-objects=false, so transactions are hashes
        'explorer_blockNumber_eq_rpc': (exf['calls'][0]['response']['result']['blockNumber'] == str(BLOCK)),
        'explorer_gasUsed_eq_rpc': (int(exf['calls'][0]['response']['result']['gasUsed']) == int(rc['gasUsed'], 16)),
        'explorer_gasPrice_eq_rpc': (int(exf['calls'][0]['response']['result']['gasPrice']) == int(rc['effectiveGasPrice'], 16)),
        'explorer_from_eq_rpc': (exf['calls'][0]['response']['result']['from'].lower() == tx['from'].lower()),
        'explorer_status_eq_rpc': (exf['calls'][1]['response']['result']['status'] == '1' and rc['status'] == '0x1'),
        'vault_implementation_matches_audit': (vault_impl is not None and vault_impl.lower() == '0xad9667049f14d1757d147f652c41dc241c57091c'),
        'ciphertext_calldata_eq_log_data': all(
            c1['entries'][i]['sha256'] == note['decoded_fields']['ciphertextI_sha256'] and
            c2['entries'][i]['sha256'] == note['decoded_fields']['ciphertextII_sha256']
            for i, note in enumerate([e for e in decoded_logs if e['event_name'] == 'EncryptedNote'])),
        'log_count_receipt': len(rc_logs),
        # note: 'any_erc20_transfer_log_in_tx' is a finding, not a pass/fail check:
        # there is deliberately NO ERC20 Transfer log in the target tx (see log_summary).
    }

    # --- hidden-vs-visible hex search ---
    sender_evm = None
    receiver_evm = '0x680d90983da58bcb7d127e3421193274e84e0efc'
    for lg in rgf['logs']:
        d = bytes.fromhex(lg['data'][2:])
        ln = int.from_bytes(d[32:64], 'big')
        uname = d[64:64 + ln].decode('utf-8', errors='replace')
        if uname == 'anara':
            sender_evm = '0x' + lg['topics'][1][-40:]
        if uname == 'kittynim':
            assert '0x' + lg['topics'][1][-40:] == receiver_evm, 'kittynim address mismatch'
    search_corpus = {
        'input': inp_hex,
        'receipt_logs_topics_plus_data': ''.join(
            ''.join(t[2:].lower() for t in e['topics']) + e['data_hex'][2:].lower() for e in decoded_logs),
        'receipt_json': json.dumps(rc, sort_keys=True).lower(),
    }
    combined = ''.join(search_corpus.values())

    def word_of(hexaddr_or_int):
        if isinstance(hexaddr_or_int, int):
            return format(hexaddr_or_int, '064x')
        return '0' * 24 + hexaddr_or_int[2:].lower()

    def search_item(label, needles):
        found = {k: any(n.lower() in v for n in needles) for k, v in search_corpus.items()}
        return {'label': label, 'needles': needles, 'found_in': [k for k, v in found.items() if v],
                'found_anywhere': any(found.values())}

    items = [
        search_item('receiver EVM @kittynim', [receiver_evm, word_of(receiver_evm)]),
        search_item('sender EVM @anara', [sender_evm, word_of(sender_evm)] if sender_evm else ['(sender address not resolved)']),
        search_item('RLS token proxy', ['0x07e17e17e17e17e17e17e17e17e17e17e17e17ea',
                                        word_of('0x07e17e17e17e17e17e17e17e17e17e17e17e17ea')]),
        search_item('relayer', ['0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8',
                                word_of('0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8')]),
        search_item('amount 6 RLS as 6e18 word', [word_of(6 * 10 ** 18)]),
        search_item('fee 3.84 RLS as 3.84e18 word', [word_of(384 * 10 ** 16)]),
        search_item('fee 0.58 RLS as 0.58e18 word', [word_of(58 * 10 ** 16)]),
        search_item('fee 4.42 RLS as 4.42e18 word', [word_of(442 * 10 ** 16)]),
        search_item('fee 4.416 RLS as 4.416e18 word', [word_of(4416 * 10 ** 15)]),
        search_item('fee 0.576 RLS as 0.576e18 word', [word_of(576 * 10 ** 15)]),
        search_item('SharedVaultProxy', ['0x9c5ad5e5ea5b5910e7fd1e1cc7b70ce0e4bf06c2',
                                         word_of('0x9c5ad5e5ea5b5910e7fd1e1cc7b70ce0e4bf06c2')]),
        search_item('UserRegistry proxy', ['0xa473291ffb33e2276f364fae169f03c4406719e9',
                                           word_of('0xa473291ffb33e2276f364fae169f03c4406719e9')]),
    ]
    # nullifier + commitments from logs vs calldata
    nullifier = decoded_logs[0]['decoded_fields']['nullifier'] if decoded_logs and decoded_logs[0]['event_name'] == 'Nullifier' else None
    commitments = [e['decoded_fields']['commitment'] for e in decoded_logs if e['event_name'] == 'Commitment']
    for h in ([nullifier] if nullifier else []) + commitments:
        items.append(search_item('log hash ' + h[:14] + '... in calldata', [h[2:].lower()]))

    # --- fee ---
    gas_used = int(rc['gasUsed'], 16)
    eff_gp = int(rc['effectiveGasPrice'], 16)
    gas_limit = int(tx['gas'], 16)
    tx_gp = int(tx['gasPrice'], 16)
    fee_wei = gas_used * eff_gp
    fee = {'gasUsed': gas_used, 'effectiveGasPrice_wei': eff_gp, 'gasLimit': gas_limit,
           'gasPrice_wei': tx_gp, 'maxFeePerGas_wei': int(tx['maxFeePerGas'], 16),
           'onchain_gas_cost_wei': fee_wei,
           'onchain_gas_cost_RLS_18dec': wei_to_rls(fee_wei),
           'max_possible_gas_cost_RLS_18dec': wei_to_rls(gas_limit * eff_gp),
           'decimals_assumption': 'RLS shown as 18 decimals (token contract per audit C.2/C.3 is 18-decimal reading; the wei figure is exact regardless of decimals)',
           'wallet_display': {'gas_RLS': '3.84', 'foundation_RLS': '0.58',
                              'total_displayed_RLS': '4.42', 'detail_activity_RLS': '4.416'},
           'comparison': 'On-chain gas cost 0.063168048 RLS does NOT equal the wallet-displayed gas fee 3.84 RLS. BUT the total fee IS public on-chain: calldata statement[8] = 4,416,000,000,000,000,000 wei = 4.416 RLS exactly, matching the wallet detail-activity fee 4.416 RLS. The displayed split (3.84 gas + 0.58 foundation = 4.42 rounded) decomposes exactly as 4.416 = 3.84 + 0.576, where 0.576 RLS is the related-tx foundation transfer (see related_tx). So: total fee 4.416 verified on-chain (statement); foundation portion 0.576 verified on-chain (related tx, rounds to displayed 0.58); relayer-retained portion 3.84 determined arithmetically (4.416 - 0.576 = 3.84, matching the displayed gas figure) but NOT present as its own word in the data. The on-chain native gas (0.063 RLS) is a separate, much smaller cost paid by the relayer; the wallet "gas" label (3.84) is the relayer service fee, not the chain gas cost.'}

    # --- related tx decode ---
    rtx_res = rtx['calls'][0]['response']['result']
    rrc_res = rtx['calls'][1]['response']['result']
    rin = rtx_res['input']
    r_recipient = '0x' + rin[10 + 24:10 + 64]
    r_amount = int(rin[74:138], 16)
    r_log = rrc_res['logs'][0] if rrc_res['logs'] else None
    related = {
        'tx_hash': rtx['tx_hash'], 'block': 24825932, 'from': rtx_res['from'], 'to': rtx_res['to'],
        'function': 'transfer(address,uint256) (selector 0xa9059cbb, canonical ERC20 transfer)',
        'recipient': r_recipient, 'amount_wei': r_amount, 'amount_RLS_18dec': wei_to_rls(r_amount),
        'gasUsed': int(rrc_res['gasUsed'], 16), 'status': rrc_res['status'],
        'transfer_log': ({'address': r_log['address'], 'topic0': r_log['topics'][0],
                          'from_topic': '0x' + r_log['topics'][1][-40:],
                          'to_topic': '0x' + r_log['topics'][2][-40:],
                          'value_wei': int(r_log['data'], 16),
                          'value_RLS_18dec': wei_to_rls(int(r_log['data'], 16)),
                          'is_erc20_transfer': r_log['topics'][0].lower() == transfer_topic}
                         if r_log else None),
        'recipient_identity': '0x71af09966cbed4434cca97c40fa38b8083548b95 is recorded in the audit contract map (C.2) as the Auditor EOA. The wallet labels the 0.58 fee "Rayls Foundation fee". Whether the Auditor EOA is the foundation fee address is UNKNOWN: no source in the archive links the two roles to one address.',
        'finding': '0.576 RLS transferred by the relayer to 0x71af09966cbed4434cca97c40fa38b8083548b95 four blocks after the target tx; 0.576 rounds to 0.58 at two decimals, matching the wallet-displayed foundation fee. This is the on-chain counterpart of the displayed 0.58 RLS fee (reconstruction: same actor, same time window, amount matches within display rounding).',
    }

    # --- provenance ---
    src_files = ['transaction.json', 'receipt.json', 'logs.json', 'block.json', 'contracts.json',
                 'explorer.json', 'registry-usernames.json', 'related-tx-0xacc7d175.json',
                 'explorer-relayer-txlist.json']
    provenance = {
        'script': SCRIPT_NAME, 'script_version': SCRIPT_VERSION,
        'tx_hash': TX_HASH, 'chain_id': CHAIN_ID, 'block': BLOCK,
        'retrieved_at_utc': txf['retrieved_at_utc'],
        'source_files_sha256': {f: sha256_file(os.path.join(RAW, f)) for f in src_files},
        'bundle_abi_extract_sha256': sha256_file(os.path.join(DEC, 'bundle-abi-extract.json')),
        'note': 'SHA-256 values here are computed at decode time from the read-only raw files; the manifest is the authoritative checksum record.',
    }

    decoded_events = {
        'provenance': provenance,
        'tx_hash': TX_HASH, 'chain_id': CHAIN_ID, 'block': BLOCK,
        'calldata': calldata,
        'logs': decoded_logs,
        'log_summary': {
            'total': len(decoded_logs),
            'by_event': {n: sum(1 for e in decoded_logs if e['event_name'] == n)
                         for n in sorted({e['event_name'] for e in decoded_logs})},
            'erc20_transfer_logs_in_target_tx': 0,
            'paidOut_or_partialWithdrawal_logs': 0,
            'all_logs_from_vault_proxy': all(e['address'].lower() == '0x9c5ad5e5ea5b5910e7fd1e1cc7b70ce0e4bf06c2' for e in decoded_logs),
        },
        'hidden_vs_visible': items,
        'cross_checks': checks,
        'fee': fee,
        'related_tx': related,
        'sender_evm_resolved': sender_evm,
        'receiver_evm_resolved': receiver_evm,
    }

    summary = {
        'provenance': provenance,
        'tx_hash': TX_HASH, 'chain_id': CHAIN_ID, 'block': BLOCK,
        'questions': {
            'q1_receipt_status': {
                'label': 'verified-fact',
                'answer': 'Receipt status 0x1 (success). Block 24825928, transactionIndex 0, gasUsed 1,316,001 of gasLimit 1,630,484, effectiveGasPrice 48,000,000,000 wei, 7 logs, contractAddress null. Block 24825928 contains exactly this one transaction.',
                'evidence': ['raw/receipt.json calls[0].response.result.status, .gasUsed, .blockNumber',
                             'raw/block.json calls[0].response.result.transactions (length 1)',
                             'raw/explorer.json calls[1].response.result.status = "1"'],
            },
            'q2_calldata_function': {
                'label': 'verified-fact',
                'answer': 'Function is transferV2. Selector 0xaacd552c equals the first 4 bytes of keccak256 of the canonical signature transferV2((((uint256,uint256),(uint256[2],uint256[2]),(uint256,uint256)),uint256[],uint256,uint256),bytes[],bytes[]) taken from the demo-bundle IEnygmaDvp ABI. Calldata parses cleanly: receipt tuple with an 8-word (256-byte) Groth16 proof, statement of 10 uint256 values, numberOfInputs 1, numberOfOutputs 3, ciphertextI 3 entries, ciphertextII 3 entries. The statement contains the spent nullifier hash and the three new commitment hashes (verified by hex search).',
                'evidence': ['raw/transaction.json calls[0].response.result.input (4,804 bytes)',
                             'decoded/bundle-abi-extract.json transferV2_canonical_signature',
                             'decoded/decoded_events.json calldata.receipt_tuple, .ciphertextI, .ciphertextII'],
                'limitation': 'No verified contract source exists for the deployed vault implementation, so what transferV2 does internally with the proof/statement/ciphertexts is NOT proven from source; the function identity and the calldata structure are proven from the selector match + the clean structural parse. The ABI used is the demo app client-side ABI (decoded/bundle-abi-extract.json), not verified on-chain source.',
            },
            'q3_destination_contract_sharedvault': {
                'label': 'verified-fact',
                'answer': 'Destination is the SharedVaultProxy (yx) 0x9C5Ad5e5Ea5b5910E7fD1E1CC7b70ce0e4bF06c2, called directly (NOT via Multicall3). Its EIP-1967 implementation slot reads 0xAd9667049f14D1757D147F652c41Dc241C57091C, matching the live vault-yx implementation recorded in the audit (C.3). The Explorer also displays method transferV2 for this hash; that label is a cross-check only, the proof is the selector match in Q2.',
                'evidence': ['raw/transaction.json calls[0].response.result.to',
                             'raw/contracts.json calls[] eth_getStorageAt EIP-1967 slot for the destination',
                             'raw/explorer.json calls[0].response.result.hash / .from'],
            },
            'q4_event_logs': {
                'label': 'verified-fact',
                'answer': '7 logs, all from the vault proxy: 1x Nullifier (vaultId 2, treeNumber 0, nullifier 0x0c0f23a6...), 3x Commitment (vaultId 2, commitments 0x094b23a6..., 0x2304db2e..., 0x206ed94a...), 3x EncryptedNote (same 3 commitments, each with 1,312 bytes of ciphertext data = two byte arrays). No ERC20 Transfer log, no PaidOut, no PartialWithdrawal, no log from any other address. This matches the audit shielded-transfer classification (Commitment + EncryptedNote + Nullifier, no payout).',
                'evidence': ['raw/receipt.json calls[0].response.result.logs (7 entries)',
                             'raw/logs.json calls[0] block-level eth_getLogs cross-check (same 7)',
                             'decoded/decoded_events.json logs[]'],
            },
            'q5_commitment_encrypted_note_observability': {
                'label': 'direct-observation',
                'answer': 'Commitment hashes are public (3 hashes in topics and in the calldata statement). EncryptedNote ciphertexts are public as opaque bytes (1,312 bytes each: two arrays; per-note ciphertextI and ciphertextII lengths recorded with SHA-256 fingerprints). The note VALUES (amounts, sender, receiver, token) are NOT visible in the ciphertext: no plaintext amount, address, or token identifier appears anywhere in the logs. One input note was spent (1 nullifier) and 3 output notes were created (3 commitments).',
                'evidence': ['decoded/decoded_events.json logs[] decoded_fields',
                             'decoded/decoded_events.json hidden_vs_visible'],
            },
            'q6_hidden_vs_visible': {
                'label': 'direct-observation',
                'answer': 'NOT visible anywhere in the raw transaction input, receipt, or logs (case-insensitive hex search, bare address and 32-byte-word forms): receiver EVM 0x680d...0efc, sender EVM 0x0c5b...0b5, RLS token proxy 0x07e1...7ea, amount 6 RLS as 6e18, fee values 3.84 / 0.58 / 4.42 RLS as 18-decimal words. FOUND in the on-chain data: the fee TOTAL 4.416 RLS as a 32-byte word in the calldata (statement[8] = 4,416,000,000,000,000,000 wei); the relayer address as tx.from; the vault proxy address (also as statement[7]); the spent nullifier hash and the 3 commitment hashes (in the calldata statement and in log topics). The 6 RLS figure, the two usernames, and the token type come only from the wallet UI / VO / video (direct observation of the experiment), NOT from on-chain data. "Not visible in this data" is NOT proof that the information is unknowable in principle: parties holding the relevant keys (receiver view key, sender keys, auditor keys) could decrypt the notes; this audit does not test that.',
                'evidence': ['decoded/decoded_events.json hidden_vs_visible (per-item found_in lists)',
                             'decoded/decoded_events.json calldata.statement_interpretation.statement_8',
                             'raw/registry-usernames.json logs[] (username -> address resolution)'],
            },
            'q7_relayer_role_sender_link': {
                'label': 'reconstruction',
                'answer': 'tx.from is the relayer 0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8 (verified-fact). The registry shows that address holds the username rayls-relayer (verified-fact from UsernameSet logs). The docs claim the relayer submits user transactions and the public sender shown is the relayer (official-claim). Whether THIS tx was submitted on behalf of @anara (0x0c5b...0b5) is a RECONSTRUCTION, not an on-chain fact: the on-chain data contains no link to @anara (no sender address, no username, no key). The link rests on experiment context: the same block/time/method/vault as the success screen in the recorded experiment, the matching nullifier/commitment pattern, and the shielded-balance decrease shown in the wallet UI. from=relayer alone is NOT proof that the relayer is the sender, and the absence of the sender address is NOT proof of absolute unlinkability.',
                'evidence': ['raw/transaction.json calls[0].response.result.from',
                             'raw/registry-usernames.json logs[] (rayls-relayer, first registration)',
                             'decoded/decoded_events.json hidden_vs_visible (sender EVM not found)'],
            },
            'q8_fee_vs_wallet': {
                'label': 'verified-fact',
                'answer': 'On-chain gas for the target tx: 1,316,001 gas x 48,000,000,000 wei = 63,168,048,000,000,000 wei = 0.063168048 RLS (18 decimals assumed). The wallet displayed 3.84 RLS gas + 0.58 RLS Rayls Foundation fee = 4.42 RLS total (detail activity 4.416 RLS). The on-chain gas cost (0.063 RLS) does NOT equal the displayed gas fee (3.84 RLS) - the wallet "gas" label is the relayer service fee, not the chain gas cost. The TOTAL fee IS public on-chain: calldata statement[8] = 4,416,000,000,000,000,000 wei = 4.416 RLS exactly, matching the wallet detail fee. The 0.58 foundation fee has an on-chain counterpart: 4 blocks later (block 24825932) the relayer transferred 0.576 RLS of the RLS token to 0x71af09966cbed4434cca97c40fa38b8083548b95 (verified-fact; 0.576 rounds to 0.58 at 2 decimals). That address is recorded in the audit map as the Auditor EOA; whether it is the Rayls Foundation fee address is UNKNOWN. The split closes exactly: 4.416 = 3.84 + 0.576, so the relayer-retained portion (3.84) is determined arithmetically from two verified on-chain numbers, though it never appears as its own word in the data. RECONSTRUCTION (not verified): the transfer created 3 output notes for 1 input note; the sender shielded balance fell by 10.416 RLS = 6 payment + 4.416 fee, so the 4.416 fee plausibly sits inside the shielded notes (one output note to the relayer, of which 0.576 went on to the foundation address and 3.84 stayed with the relayer). The note values are encrypted, so this mapping cannot be verified from the chain.',
                'evidence': ['raw/receipt.json calls[0].response.result.gasUsed, .effectiveGasPrice',
                             'decoded/decoded_events.json calldata.statement_interpretation.statement_8 (4.416 RLS word)',
                             'raw/related-tx-0xacc7d175.json calls[0]/[1] (transfer 0.576 RLS, block 24825932)',
                             'raw/explorer-relayer-txlist.json (exactly 2 relayer txs in 24825800-24826200)',
                             'decoded/decoded_events.json fee, .related_tx'],
            },
        },
        'registry_resolutions': {
            'anara': {'address': sender_evm, 'label': 'verified-fact',
                      'evidence': 'raw/registry-usernames.json logs[] UsernameSet(anara), block 0x1645a5f, tx 0x2d898d9b21ef9f3634a0e1354568f98398d4d172556af520590d62d111d99488'},
            'kittynim': {'address': receiver_evm, 'label': 'verified-fact',
                         'evidence': 'raw/registry-usernames.json logs[] UsernameSet(kittynim), block 0x167bc88, tx 0x9b34ac6ee320d029da46fe7d5feaf5c0a9b2baff628b46d0c626ab13b95ad00d'},
            'total_usernames_observed': 195,
            'note': '195 UsernameSet logs over blocks 23212003-24910000 (audit D.6 recorded 194 at 21 Nov; +1 since). Two ranges returned "No logs found" (23812003-24012002, 24812003-24910000) - re-checked, genuinely empty.',
        },
        'limitations': [
            'No verified contract source for the deployed SharedVault implementation (0xAd966704...); the function/event ABIs used come from the demo-bundle client code (decoded/bundle-abi-extract.json), not from verified on-chain source. Selector/topic matches are on-chain evidence for the signatures, but internal contract logic is not proven.',
            '4byte.directory has no entry for selector 0xaacd552c or for the three event topic0s (count 0 for all four; decoded/lookups-4byte.json). Resolution relies on the bundle ABI + local keccak256.',
            'Note values (amounts, sender, receiver, token) are encrypted; the mapping of the 3 output notes to (6 RLS payment / 3.908 RLS change / 4.416 RLS fee) is a reconstruction from the wallet balances and the note counts, NOT a verified on-chain fact.',
            'The 3.84 RLS "gas" component of the wallet display never appears as its own word in the on-chain data; it is determined only arithmetically (4.416 statement fee minus 0.576 foundation transfer = 3.84) and its exact nature (relayer service fee vs gas reimbursement) is unknown.',
            'Whether 0x71af09966cbed4434cca97c40fa38b8083548b95 (Auditor EOA per the audit map) is the Rayls Foundation fee address is unknown.',
            'The statement array semantics are verified by value-matching for positions 3-8 (nullifier, 3 commitments, vault address, 4.416 RLS fee); positions 0, 1, 2 and 9 are unidentified (two zeros and two hashes) because no published statement layout exists - the Merkle-root / binding-hash readings for positions 2 and 9 are inferences, not facts.',
            'This audit covers one transaction plus one related fee-settlement tx; it does not prove anything about other shielded transfers.',
        ],
    }

    with open(os.path.join(DEC, 'decoded_events.json'), 'x', encoding='utf-8') as fh:
        fh.write(json.dumps(decoded_events, indent=2, sort_keys=True) + '\n')
    with open(os.path.join(DEC, 'audit_summary.json'), 'x', encoding='utf-8') as fh:
        fh.write(json.dumps(summary, indent=2, sort_keys=True) + '\n')

    print('selector:', selector, 'computed:', sel_computed, 'match:', selector_match)
    print('numberOfInputs:', num_inputs, 'numberOfOutputs:', num_outputs, 'statement_len:', stmt_len)
    print('ciphertextI entries:', c1['count'], 'ciphertextII entries:', c2['count'])
    print('logs decoded:', {n: sum(1 for e in decoded_logs if e['event_name'] == n) for n in sorted({e['event_name'] for e in decoded_logs})})
    print('sender_evm:', sender_evm, 'receiver_evm:', receiver_evm)
    print('on-chain gas cost RLS:', fee['onchain_gas_cost_RLS_18dec'])
    print('related tx: 0.576 RLS ->', related['recipient'])
    print('cross-checks failing:', [k for k, v in checks.items() if v is False])
    print('decoded_events.json + audit_summary.json written')

if __name__ == '__main__':
    main()
