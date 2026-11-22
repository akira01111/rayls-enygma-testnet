# Initial Technical Audit — Rayls Enygma Public Testnet

**Purpose:** read-only audit in preparation for Rayls Week 3 research content (closes Sunday 22 November 2026, 23:59 UTC).
**Audit date:** 21 November 2026 (on-chain checks ~04:50–05:00 UTC / 11:50–12:00 WIB; GitHub checks 21 November 2026).
**Nature:** READ-ONLY. No transactions, no external account connections, no file/repo changes, no publication, no spending.
**Output:** this report only. Not an article, not an experiment, not a new repo.

## Evidence taxonomy (6 labels — binding for the entire report)

1. **verified fact** — proven directly from a primary source that was checked (RPC, explorer logs, repo files, bundle) and re-checkable.
2. **official claim** — stated officially by Rayls (docs, blog, AMA) but not independently verified in this audit.
3. **direct observation** — what was actually seen/measured in this check (log figures, hashes, file sizes), without further interpretation.
4. **reconstruction** — a result processed from raw data under explicit rules (e.g. classifying transaction types from event combinations); reproducible if the rules are followed, but not a label from the protocol.
5. **inference** — a reasonable interpretation of the available evidence; clearly marked as a hypothesis, not a fact.
6. **unknown** — not found / not verifiable; gaps are not filled with assumptions.

**Writing rules:** contract addresses and hashes are written IN FULL, never abbreviated. Documentation claims are not equated with verified implementation. The absence of public data is not treated as evidence (Enygma Sovereign activity on institutional private networks is not visible through the public explorer). Findings that look odd are recorded as "needs team context via ticket" before becoming public conclusions.

## Summary of findings

1. **The testnet is still active and in fact busier than ever.** Chain ID re-verified: **7,295,799** (`0x6f5337`), RPC `https://testnet-rpc.rayls.com` live, latest block at check time **24,793,989** (21 Nov 04:50:45 UTC). The yx vault grew from 803 logs / 204 tx (15 Nov baseline) to **2,128 logs / 511 tx**; the yx registry from 143 logs / 76 tx to **405 logs / 207 tx** with **131 new usernames** (16–21 Nov). Latest activity: registry 21 Nov 00:39 UTC, vault 21 Nov 03:25:55 UTC.
2. **No new auditors.** Still 7 `AuditorAdded`, 4 `AuditorKeyGiven`, 1 `AuditorPersonalKeySet` — all from 10 Nov 2026. The previous article's conclusion — *selective auditing on the tested Enygma Public deployment cannot yet be independently verified* — **STILL STANDS**; no new evidence changes it.
3. **The demo bundle was rebuilt, the configuration is unchanged.** The page and main bundle changed hash and filename (now split into many chunks), but all contract addresses and deployment files (`7295799.json`, `br/7295799.json`, `11155111.json`) are the same; the `retired: "2026-11-10"` flag remains.
4. **New finding — the live bx proxy implementations do not match the bundle.** The bx upgrade listed in the bundle (via `ownerCalls`) was never executed on the proxy: the live bx registry implementation (`0x66f87eaf23152bd5a155f96a85b7e5a64e3f6952`) and bx vault (`0x8551f451a5e7dc39d82ed08195eeda16abfe60a1`) are not in the bundle. The live yx implementations match the bundle. **Needs team context via ticket** before any public conclusion about bx.
5. **The three actions can be separated from the event combination per tx (reconstruction):** shielding 272 tx, shielded transfer 188 tx, unshielding 41 tx (out of 511 yx vault tx). **Unshielding is fully public** — 41 payouts, the `PartialWithdrawal` and `PaidOut` amounts match exactly (0 mismatches), total ≈ 752.58 tokens under an 18-decimal reading, 33 distinct recipients, 9 distinct tokens. **Shielded transfer shows neither who/how much/which token** — only `Commitment`/`Nullifier` hashes and 1,312-byte `EncryptedNote` ciphertext.
6. **Docs unchanged since 11–12 Nov.** The wording tension over scoped keys remains: the blog claims scoped viewing keys are the Enygma model; the Private Network doc writes "There are no scoped view keys" and "Audit access is network-wide"; the Public doc writes scope per deployment/country. **Still unresolved — needs team context via ticket.**
7. **On GitHub, the auditor escrow turns out to be implemented — but in `enygma_retail_payments`, not in `enygma_payments`.** The files `auditor.go` and `UserRegistry.sol` (`mlKemAuditCt`/`aesAuditCt`) prove auditor key-escrow code exists. This is important new context, but **not** proof that selective auditing is running/verified on the live testnet deployment (no on-chain audit/decryption event was found). Also new: ciphertext binding for DvP (`CiphertextHash.sol`, commit `6a6a23b1cffde9b4e3a37e27375ddff9ed397578`, 16 Nov). No `SharedVault` file exists in the repo; the repo contains no testnet addresses / chain ID 7295799 (default Hardhat config 1337).
8. **Shielded volume cannot be measured in full.** What is measurable with certainty: the number of registrations, the number and amounts of unshielding, the number of tx per type (reconstruction). What is not measurable: the amounts and parties in shielded transfers, and total shielded volume. Double counting must be avoided: `PartialWithdrawal` + `PaidOut` are one and the same economic event; `Commitment` appears in both shielding and transfers.
9. **The 0.0001 RLS fee discrepancy is still UNRESOLVED** — never call it rounding. Proof-time figures differ by source (408 ms vs ~2.2 s vs ~3 s vs "under 4 s") — not yet tested.

---

## A. Summary of workspace state and available material

### A.1 Workspace

- Workspace: `/home/hatch/workspace` — 37 git repos (this figure comes from the assignment brief already verified by Anara; this audit did not recount them).
- Previous Enygma research folder: `/home/hatch/workspace/rayls-enygma-research` — **an ordinary folder, NOT a local git repo** (verified fact — checked directly on 21 Nov 2026; no `.git` directory inside it). Its contents (20 files):
  - `README.md`
  - `ama/ama-notes.md`
  - `audit/audit-status.md`
  - `demo-testing/screenshots/1-fee-register.png`, `2-fee-shield.png`, `3-confirm-onchain.png`, `4-wallet-akhir.png`, `5-send-48-user.png`, `demo-testing/test-report.md`, `demo-testing/user-flow.md`
  - `findings/observations.md`, `findings/official-claims.md`, `findings/unknowns.md`, `findings/verified-facts.md`
  - `research/open-questions.md`, `research/research-plan.md`, `research/technical-overview.md`
  - `sources/source-register.md`
  - `technical-evidence/technical-evidence.md`
- GitHub mirror repo of the previous research: `github.com/akira01111/rayls-enygma-research` (public since 16 Nov 2026, head `ab523db`, 4 commits — from the brief; not re-cloned in this audit because the local folder was already checked).
- Quality-standard reference repo: `/home/hatch/workspace/rayls-mainnet-block-research-check` — a local git repo (2 commits: `4ef462f` "Add audited historical block comparisons", `a514353` "Add reproducible Rayls mainnet block analysis"). Its structure was studied as a documentation pattern: README (research question, network, results table, method, reproduce commands, interpretation + limitations, official references, source snapshot with commit hash), CSV datasets + raw JSON + metadata JSON per window (chain_id, rpc, sampling method, start/end block, total, elapsed, observed_tps, retrieved_at_utc), verification scripts (`verify_dataset.py`, `reproduce_fixed_600.py`), multi-window comparisons in `windows/`, `audit_report.json`. This standard is used as the reference for section H.

### A.2 Prior material and conclusions used as the starting point

- Previous Enygma article: "Can Rayls Enygma Make Private Payments Auditable?" (X, 16 Nov 2026, `status/2122127310585524690`). One of its main conclusions — selective auditing on the tested Enygma Public deployment **cannot yet be independently verified** — **STILL STANDS** unless new evidence appears. This audit found no new evidence that changes that conclusion (see B.4 and D.5).
- Previous mainnet article: "How Fast Is Rayls in Practice? I Audited 2,400 Mainnet Blocks" — score **90/100**, **9/10 Rayls Points**, Approved, bonus +3 Discord points. Used as the documentation quality standard: independent on-chain data collection, reproducible quantitative checks, source code analysis, raw RPC responses, CSV datasets, metadata + checksums, audit scripts, explanation of limitations. Reviewer feedback for future research applied here: (1) extend observations to more dates/times or continuous monitoring; (2) a separate finality experiment if possible; (3) consider a controlled load test in a suitable environment; (4) record the client version and block identifiers for every data collection.
- Rayls moderator guidance: the hands-on testnet approach is welcome; the old article does not need to be deleted; direct testing content is expected to keep being made; if a main finding cannot yet be verified, **open a ticket first** so the team can provide context (the mod does not mind receiving tickets even if replies take time); the mod explicitly **approved** making the next Enygma Testnet content for the Weekly Quest.
- Official Rayls community guidance: content should help the community understand what is being built, who uses it, why it matters, and how the product/ecosystem works. Avoid content that only highlights gaps in public data or negative conclusions without context. Enygma Sovereign activity on institutional private networks is **not automatically visible** through the public explorer — do not treat the absence of public data as evidence. Stay critical but constructive; no FUD/ragebait/unsubstantiated claims.
- The proposed new repo name `rayls-enygma-public-testnet-research` is still a **PROPOSAL — not approved** to be created/published. **No new repo was created in this audit.** Section H is only a structure recommendation.
- 15 Nov 2026 baseline used for comparison (from the previous research): yx registry 143 logs / 76 tx (63 registrations, last log 13 Nov 22:05:57 UTC); yx vault 803 logs / 204 tx (last log 15 Nov 14:41:04 UTC); bx registry 4 logs; bx vault 10 logs. Events at that time: Commitment 334, EncryptedNote 321, Nullifier 107, PartialWithdrawal 13, PaidOut 13, AuditorAdded 7, AuditorKeyGiven 4, AuditorPersonalKeySet 1, Upgraded 7. 15 Nov bundle: page SHA `b615fd73aa999fb72529d37553ba0943d754e2f2e0f50468a07fe2e8fcb636c5` (3,645 bytes); bundle `index-BmNruHc0.js` SHA `c878b635cab69d9c529f4cd9e6fcd8fb606c0e2a9a3bd42af39ea435f065ec81` (1,338,924 bytes); yx deployment marked retired 2026-11-10.

### A.3 Method of this audit

- **GitHub:** inspection of the `raylsnetwork/Enygma` repo (head, commits, source files, ABI/configuration) by one investigation agent; results summarized in section B.
- **On-chain + bundle + docs:** read-only checks via `curl` (RPC `https://testnet-rpc.rayls.com`, explorer API `https://testnet-explorer.rayls.com`, page and bundle `https://enygma-testnet.rayls.com/`) by one investigation agent; results summarized in sections C–F. Check time ~04:50–05:00 UTC, 21 Nov 2026.
- **Method limitations recorded:** the explorer API limits results to **max. 1,000 results per call** — a naive `fromBlock=0&toBlock=latest` call for the yx vault returned exactly 1,000 logs (truncated); the full total was obtained by paginating in 200,000-block ranges. One HTTP 403 from urllib without a User-Agent (resolved with curl + a browser User-Agent). Two `exec` calls during the on-chain investigation returned exit code 1 (nonzero) — no data was lost from the report because all figures above came from successful calls; those failures are recorded here as a tooling limitation, not as a finding.
- **What was not done:** no experiments on the testnet, no article writing, no repo creation, no transactions, no account connections.

---

## B. GitHub repository and relevant source code

### B.1 Main repo: `raylsnetwork/Enygma`

- **Head at check time:** `0b1945ae6c827745d1ad48eddcec39df4b20277a` (19 Nov 2026, 22:48 UTC) — verified fact (commit hash from the GitHub check).
- **Position relative to the previous research baseline:** 71 commits ahead of `3c61be782cbd31b108eacbda662d3a0a9219f6ae` — verified fact.
- **Branches:** 183 branches; the Rayls organization has 25 public repos — direct observation.
- **`protocol_description.md` unchanged byte-for-byte** since the baseline: blob `61b9447217a881dd3e47f7ade3fcc8d5e4df9a0f`, 37,302 bytes — verified fact. This means the protocol description in the repo has revised no claims since the previous article.

### B.2 What is implemented in code vs what is only documented

| Feature | Status | Evidence |
|---|---|---|
| Auditor key escrow (ML-KEM + AES view-key) | **Implemented — in `enygma_retail_payments`** | `auditor.go`; `UserRegistry.sol` (`mlKemAuditCt` / `aesAuditCt`) — verified fact (files and identifiers checked in the repo) |
| "No auditor role" | **Applies only to `enygma_payments`** | The "no auditor role" claim turns out to be scoped to that module only, not to all of Enygma — an important correction to the previous reading |
| Ciphertext binding for DvP | **Implemented (new)** | `CiphertextHash.sol` + tests + salt changes, commit `6a6a23b1cffde9b4e3a37e27375ddff9ed397578`, 16 Nov 2026 — verified fact |
| `SharedVault` | **No file by that name exists in the repo** | No `SharedVault` file was found — direct observation; the live vault contract on the testnet cannot be matched to a file in this repo |
| Testnet addresses / chain ID 7295799 | **Not in the repo** | Default Hardhat config 1337; no testnet deployment config — direct observation |
| `enygma_demo` | Unchanged since 29 Oct 2026 | direct observation |
| `address.json` contains `0xd908BaeE382191D15E479589D9661A9E9b55b827` | **Provenance unknown** | This address was found in the repo but its origin/purpose is unknown — unknown; do not use it as a deployment address without verification |

**Correction of a wrong inference:** the testnet chain ID **7,295,799 is not a typo of 72,957** (mainnet). Chain ID 7,295,799 was verified directly from the RPC (`eth_chainId` → `0x6f5337`); the repo simply contains no testnet deployment configuration. Do not write that the two were swapped.

### B.3 Related `akira01111` repos

- `github.com/akira01111/rayls-enygma-research` (public, head `ab523db`, 4 commits) — the previous research repo; its local copy was checked in A.1. No changes were made to it in this audit.

### B.4 What the GitHub code proves and does not prove

- **What it proves:** auditor key-escrow code exists in the retail payments module; new DvP ciphertext binding exists; the protocol description is unchanged.
- **What it does NOT prove:** that selective auditing is actually running or verifiable on the live testnet deployment. No on-chain event shows decryption/auditing by an auditor (see D.5), and the live vault contract is not matched to a repo file. The previous article's conclusion therefore still stands — **an inference supported by consistent negative evidence, not a positive fact**.
- **Implication for the article:** the escrow code is new context worth explaining (it shows the auditing mechanism was indeed designed and implemented in one module), but the article must keep distinguishing "the code exists" from "live auditing is verified".

---

## C. Architecture and configuration of the Enygma Public Testnet

### C.1 Network configuration — re-verified against the live deployment

| Item | Value | Status |
|---|---|---|
| Chain ID | **7,295,799** (`eth_chainId` → `0x6f5337`) | verified fact — same as baseline; **not** 72,957 (that is mainnet) |
| RPC | `https://testnet-rpc.rayls.com` | verified fact — live, no RPC failed during the check |
| Explorer | `https://testnet-explorer.rayls.com` | verified fact — the logs API was used for all counts in section D |
| Demo | `https://enygma-testnet.rayls.com/` | verified fact — page + bundle downloaded and hashed |
| Latest block at check time | **24,793,989**, timestamp **2026-11-21 04:50:45 UTC** | direct observation (`eth_blockNumber` → `0x17a5385`) |
| Growth since baseline | +847,658 blocks from 23,946,331 (15 Nov 14:40 UTC) | reconstruction (difference of two readings) |
| RLS token (Ethereum mainnet, NOT testnet) | `0xb5f7b021a78f470d31d762c1dda05ea549904fbd` | verified fact (from the previous research; not re-verified here) |

### C.2 Contract map (testnet 7295799) — all addresses complete, bytecode sizes from `eth_getCode`

**yx deployment (active):**

| Contract | Address | Bytecode (bytes) |
|---|---|---|
| RLS token (proxy) | `0x07e17E17e17E17e17e17e17E17E17E17E17e17EA` | 122 |
| RlsGasForwarder | `0x753cc3Abe9A1c49536ee74F1f424fCF693AAB5DD` | 4,394 |
| UserRegistry proxy | `0xA473291FFb33e2276F364fAE169f03c4406719e9` | 170 |
| SharedVaultProxy | `0x9C5Ad5e5Ea5b5910E7fD1E1CC7b70ce0e4bF06c2` | 170 |
| UsdrVault | `0x1edb224cf8637f92efadaf47ef9e70c044d75584` | 20,224 |
| RlsVault | `0x97b5d78dbe06d8c8c843f87b5aa2d8587b890795` | 20,224 |
| Verifier | `0xfa3a53ec650bfd4ca3e8461abce243382a1037af` | 4,652 |
| GenericGroth16Verifier | `0xc12f06f883b757c91069f9d94065a4c673ef356a` | 2,916 |
| Poseidon T3 | `0xc29f02220d8aed5c731de4aee9d7d8d24c94ef15` | 9,743 |
| Poseidon T5 | `0x078c99bbbbf9dcf827ff085c9a4634213b18018b` | 16,276 |
| Poseidon Wrapper | `0x0bc72bf5dd894164f7cc8f8b92c78eb7d2156f3f` | 687 |
| OwnerMultisig | `0xBf099175a241194C38E977735D59CCb22596d775` | 4,373 |
| UserRegistryRetired | `0xD1d92f1B183B84Ea528211302B1eCB881EeF2770` | (not measured; the `retired: "2026-11-10"` flag is unchanged) |

**bx deployment (inactive since 3 Nov — see D.2):**

| Contract | Address | Bytecode (bytes) |
|---|---|---|
| RlsGasForwarder | `0x2ef592329B8e01320170f8f8d759d9bcA94d1066` | 4,394 |
| UserRegistry proxy | `0x3E9435c1fe8432e21E80D7A8ab81EBfc8eC708E3` | 170 |
| UserRegistryImplementation (in bundle) | `0xB23124D2eE339d1E8175B9ec10D20217CE015c1C` | 14,492 |
| SharedVaultProxy | `0x94dafa3bf372cad68143ac535f845e74751d75ef` | 170 |
| TokenFactory | `0x7416094FFC5A1D0C2659DA0D5b81CeCc18f1BdAc` | 7,274 |

**Other contracts:**

| Contract | Address | Notes |
|---|---|---|
| Auditor | `0x71AF09966CBED4434ccA97c40Fa38B8083548B95` | 0 bytes of code = EOA (verified fact) |
| Relayer (sender address of all vault/registry tx) | `0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8` | Registered username `rayls-relayer` (see D.4) |
| Multicall3 | `0xca11bde05977b3631167028862be2a173976ca11` | Used by the relayer for shielded payment delivery |
| Forwarder "next" (yx) | `0x12B6640048DEB2e8fFDa4Bc10Bb2a640B70eCA6d` | Listed in the bundle (block 23395717); already used by the latest registration (see D.4) |
| EnygmaDvp | `0x7ec57a8f97b636a4b54633df826b2a4311018996` | Appears in the new bundle; the baseline did not record it — unknown whether it is new or was simply not recorded before |

**Known trap — restated:** `0x753cc3Abe9A1c49536ee74F1f424fCF693AAB5DD` is the **RlsGasForwarder, NOT the RLS token**. The testnet RLS token is `0x07e17E17e17E17e17e17e17E17E17E17E17e17EA` (proxy, 122 bytes).

### C.3 EIP-1967 implementation slots — main finding

Slot `0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc` read via `eth_getStorageAt`:

| Proxy | Live implementation | Matches bundle? |
|---|---|---|
| Registry yx | `0x9686a3d5a9Fd2101d15888c6a09a64faFA7EE349` | **Yes** — same as `UserRegistryImplementation` in the bundle (upgrade already executed) |
| Vault yx | `0xAd9667049f14D1757D147F652c41Dc241C57091C` | **Yes** — same as `SharedVaultImplementation` in the bundle |
| Registry bx | `0x66f87eaf23152bd5a155f96a85b7e5a64e3f6952` (14,440 bytes) | **NO** — the bundle lists `0xB23124D2eE339d1E8175B9ec10D20217CE015c1C` (14,492 bytes); this live address **does not appear at all** in the current bundle |
| Vault bx | `0x8551f451a5e7dc39d82ed08195eeda16abfe60a1` (23,641 bytes) | **NO** — the bundle lists `0xe023791669A54EC41Ef1affA2c1B44460C1943CD` |

- The EIP-1967 beacon slot (`0xa3f0ad74…`) = 0 for all three proxies checked → not a beacon proxy (direct observation).
- **Upgrade evidence (event `Upgraded`):** the yx registry rose to `0x9686a3d5a9Fd2101d15888c6a09a64faFA7EE349` at block 23,400,006, 11 Nov 21:25:18 UTC, tx `0x908fdae3efbee9b058da2088eaf73f7f0031257df79953974fb87b1c5ac96fe8`; the yx vault rose to `0xAd9667049f14D1757D147F652c41Dc241C57091C` at block 23,399,976, 11 Nov 21:25:01 UTC, tx `0xc841126f7cf05d937967743f7db5cb80d04cf32ed1dca929aac23d952e97f3c4`. The bx registry/vault **each have only 1 `Upgraded` log, from the 3 Nov deployment** (to `0x66f87eaf23152bd5a155f96a85b7e5a64e3f6952` / `0x8551f451a5e7dc39d82ed08195eeda16abfe60a1`) — the bx `ownerCalls` upgrade in the bundle (block ~23,395,9xx) **was never executed** on the proxy.
- **Inference:** the `Implementation` + `next` + `ownerCalls` entries in the bundle are a planned/pending upgrade; for yx it is already live, for bx it is not yet. **Needs team context via ticket** — do not conclude in public that bx is "broken" or "abandoned"; all that is proven is the mismatch between the bundle and live state.
- **Other anomaly (unknown):** the RLS token implementation slot contains its own address (`0x07e17e17e17E17e17e17e17E17E17E17E17e17EA`) — not the usual EIP-1967 proxy pattern; its meaning is **unknown**, not verified further.

### C.4 Demo bundle — new build, same configuration

- Page `https://enygma-testnet.rayls.com/`: **3,872 bytes, SHA-256 `d709dc0639a80d71b127681fbd56ae7f6f9a9f83c38bf4b7f42239b4b961a28e`** (baseline 3,645 bytes / `b615fd73aa999fb72529d37553ba0943d754e2f2e0f50468a07fe2e8fcb636c5`) — **changed** (verified fact).
- The main bundle is now **`assets/index-Dlv-HYaZ.js`, 1,422,052 bytes, SHA-256 `7530bbc2d7a301c50e28923529cb9315f88145a9a25a7c71db8a1f34afd9ca68`** (baseline `index-BmNruHc0.js`, 1,338,924 bytes / `c878b635cab69d9c529f4cd9e6fcd8fb606c0e2a9a3bd42af39ea435f065ec81`) — **a new build** (verified fact). The build is now split into many chunks (`rolldown-runtime-DLMaRju-.js`, `utils-62W0Csdc.js`, `sha3-Dlq0T7vU.js`, etc.) — previously a single bundle.
- Deployment configuration inside the bundle (bundled at build time, not fetched at runtime — `GET /contracts/deployments/7295799.json` and `/br/7295799.json` return **HTTP 404 "Not found"**): still **3 files: `7295799.json`, `br/7295799.json`, `11155111.json` (Sepolia)** — **no new deployment** (verified fact).
- All baseline contract addresses are still in the bundle and **unchanged** (verified fact).
- Auditor in the bundle: `0x71AF09966CBED4434ccA97c40Fa38B8083548B95` (8 occurrences) — unchanged. `auditorPublicKeyHash` of the yx registry: `0x4151c50e9250f5818a53f9e48e734bd4209407d19f966ede4f7988dd4af863e5` — same as baseline.
- Relayer URLs in the bundle: `7295799=https://enygma-relayer-aafjr.ondigitalocean.app/rayls`, `11155111=https://enygma-relayer-aafjr.ondigitalocean.app/sepolia` (the baseline did not record these values — they cannot be compared).
- Other yx details verified from the bundle: `UserRegistryImplementation` `0x9686a3d5a9Fd2101d15888c6a09a64faFA7EE349` (tx `0xe029bde6…` — the hash was recorded truncated in the check notes, full hash **unknown** — block 23395761), `SharedVaultImplementation` `0xAd9667049f14D1757D147F652c41Dc241C57091C` (block 23395769).

### C.5 Shielding / unshielding / shielded transfer mechanism (from docs + logs)

**Official claim (docs `how-enygma-public-works`, `rayls-high-level-architecture`):**
- "Shielding and unshielding are public: the chain shows the address, the token and the amount moving in or out."
- "A send between shielded balances shows only that a send happened, the relayer that submitted it and its gas fee."
- "In the shared vault, a payment doesn't show which token it moved."
- Groth16 requires a trusted setup; "The testnet's proving and verifying keys come from a single-party setup, which is suitable for testing only."
- Relayer fee 15% to the Rayls Foundation; unshield/shield USDr +0.25%.
- Pilot blog (12 Nov): AES-256-GCM + ML-KEM + HKDF cryptography for the Public pilot; shielding/unshielding are public; an invite flow exists; usage policy (all fees in $RLS); roadmap (WalletConnect custody, shielded swaps, DvP, sealed-bid auctions); faucet 1×/hour.

**Verified from the logs (section D):** unshielding is indeed fully public (address, token, amount in the logs); shielded transfer indeed shows neither party/amount/token; registration is indeed public (address + username). **Not verified from the logs in this audit:** the ERC-20 token transfer side of shielding (whether the shielding amount is visible through token logs) — the docs claim on that is recorded as an official claim, not a verified fact.

**Proof-time figures differ by source (official claim, mutually inconsistent — not yet tested):** 408 ms (rayls.com) vs ~2.2 s (AMA) vs ~3 s (pilot blog) vs "under 4 s". Do not quote a single figure as fact without testing it yourself.

### C.6 Docs — dates and wording (verified fact)

| Page | Updated | Key wording (verbatim) |
|---|---|---|
| `docs.rayls.com/docs/enygma-privacy-and-auditing` | 2026-11-11T15:26:41.000Z | **Unchanged:** "Audit access is network-wide" and "There are no scoped view keys" are still written verbatim. Note: this page discusses the **Private Network (Besu Hub)** model, not the Public testnet. |
| `docs.rayls.com/docs/enygma-public` | 2026-11-11T21:36:24.000Z | Public model: "An auditor for every deployment… A deployment can be set up per country, so that each auditor reads only its own country's activity." |
| `docs.rayls.com/docs/enygma-public-who-sees-what` | 2026-11-11T21:36:27.000Z | "One auditor per deployment. An auditor reads only its own deployment, for example its own country's." + "The auditor… Every shielded transaction, decrypted: who paid whom, the amount and the token" + "It can't freeze… Nobody can ask to be an auditor. An existing auditor adds new ones." |
| `docs.rayls.com/docs/how-enygma-public-works` | 2026-11-11T15:27:18.000Z | "In the shared vault, a payment doesn't show which token it moved." + Groth16 single-party setup, testing only. |
| `docs.rayls.com/docs/rayls-high-level-architecture` | 2026-11-11T21:37:02.000Z | Shielding/unshielding public (address, token, amount); shielded send only shows that a send happened, the relayer, and the gas fee; relayer fee 15% to the Rayls Foundation; unshield/shield USDr +0.25%. |
| Blog `rayls.com/blog/auditability-without-surveillance-…` | Published 2026-09-12, Updated 2026-11-12 | Claims scoped viewing keys **are** the Enygma model ("keys that can be scoped to particular subsets of data… mathematically enforced") — **contradicts in wording** the Private Network doc ("There are no scoped view keys"). |
| Blog "controlled visibility" | Updated 15 Nov 2026 | Repeats the scoped-auditor claim — newer than the docs pages (11 Nov). |

**The auditor-access scope conflict is STILL UNRESOLVED (official claims in tension with each other):** blog = the general Enygma/Sovereign model (scoped keys); the privacy-and-auditing doc = a Private Network operator sees network-wide; the Public doc = scope per deployment/country. All three are unchanged since the baseline (all updated 11–12 Nov, except the "controlled visibility" blog of 15 Nov). This report presents all three sides without deciding. **Needs team context via ticket.**

**New source (not in the previous research):** IACR ePrint papers **2025/1638** (Rayls II) and **2025/1639** (Rayls) — official claim (Rayls cryptography publications); their contents were not reviewed in this audit, noted as further reading.

---

## D. Observable on-chain activity

All figures in this section are **direct observation** from the explorer logs API (`https://testnet-explorer.rayls.com/api?module=logs&action=getLogs`), paginated in 200,000-block ranges because of the 1,000-result cap per call. Check time ~04:50–05:00 UTC, 21 Nov 2026. Reference block at that time: 24,793,989.

### D.1 Registry yx — `0xA473291FFb33e2276F364fAE169f03c4406719e9`

- **405 logs / 207 unique tx** (baseline 143 / 76 → **+262 logs / +131 tx**). Blocks 23,212,003–24,766,266.
- First log 10 Nov 13:57:50 UTC; **last log 21 Nov 00:39:06 UTC**, tx `0x0c7419d5d3d334dae29f5e87bdde78481ed61b6ae2907429044b4e56903beb0a` (username `rq3faucet26`).
- **The yx registry is still active after 13 Nov 22:05 UTC — yes, very active.**
- Per event: UserRegistered 194, UsernameSet 194, AuditorAdded 7, AuditorKeyGiven 4, Upgraded 2, Initialized 1, ImportClosed 1, OwnershipTransferred 1, AuditorPersonalKeySet 1.
- New since 15 Nov 14:41:04 UTC: **262 logs / 131 tx — all UserRegistered (131) + UsernameSet (131)**. No new auditor events.

### D.2 Registry bx — `0x3E9435c1fe8432e21E80D7A8ab81EBfc8eC708E3`

- **4 logs / 3 tx, UNCHANGED** from the baseline. Blocks 22,210,868–22,211,254, 3 Nov 12:32:40–12:36:33 UTC. Upgraded 1, Initialized 1, ImportClosed 1, OwnershipTransferred 1.

### D.3 SharedVault yx — `0x9C5Ad5e5Ea5b5910E7fD1E1CC7b70ce0e4bF06c2`

- **2,128 logs / 511 unique tx** (baseline 803 / 204 → **+1,325 logs / +307 tx**). Blocks 21,568,375–24,784,630.
- First log 30 Oct 00:04:35 UTC; **last log 21 Nov 03:25:55 UTC**, tx `0x7f72b00105ab01cb600461487dad6ff7932bdb302c6a85d00a01b67df3117dd1` (`PaidOut`).
- **The yx vault is still active after 15 Nov 14:41 UTC — yes.**
- Per event: Commitment 888, EncryptedNote 847, Nullifier 296, PartialWithdrawal 41, PaidOut 41, RoleGranted 5, CoinLocked 5, Upgraded 3, Initialized 2.
- New since 15 Nov 14:41:04 UTC: **1,325 logs / 307 tx** — Commitment 554, EncryptedNote 526, Nullifier 189, PartialWithdrawal 28, PaidOut 28.

### D.4 SharedVault bx — `0x94dafa3bf372cad68143ac535f845e74751d75ef`

- **10 logs / 6 tx, UNCHANGED** from the baseline. Blocks 22,211,086–22,211,236, 3 Nov 12:34:50–12:36:23 UTC. RoleGranted 6, RoleRevoked 2, Upgraded 1, Initialized 1.

### D.5 Auditors — nothing new (verified fact)

`AuditorAdded` remains **7**, all 10 Nov 2026, all by `0x08fbf5b9c2faeb669b9cbdcfe685ff9afc444dae` (the first 3) or auditor `0x71af09966cbed4434cca97c40fa38b8083548b95` (the last 4):

| # | Auditor address | Block | Time (UTC) | Tx hash |
|---|---|---|---|---|
| 1 | `0x71af09966cbed4434cca97c40fa38b8083548b95` | 23212015 | 10 Nov 13:57:57 | `0xf1b398d51a3d5f507c1fa13016361b499fefabd37e0777697e82bc60a4ca53dd` |
| 2 | `0x3bffb10f6f17f15164fbc0416f1bc42c56b2c191` | 23212021 | 10 Nov 13:58:00 | `0x0ef89d3739e3a24a15daf14377fc46bfea48d36e48a86213603d027e3d4d635e` |
| 3 | `0xd04004a3715f8428674a01ffde2069c181d4b0fd` | 23212029 | 10 Nov 13:58:05 | `0xe2d442f5550172fa1b4235b7e6f84afeaaa951ffceea55a053feed942b23c428` |
| 4 | `0x23c5a5138ad66ff376a7a20248ec47a64d7b3fc9` | 23222870 | 10 Nov 15:48:10 | `0xc6261618d2cc6dd250f9b30504f27a16a0378e16b2a4e927f13a933e2eca1aef` |
| 5 | `0x67359d4ed15116fc5d15c96d0f0b049bae34688f` | 23225307 | 10 Nov 16:12:56 | `0x61874cfb2277bd640ae20e8ed08bafb68449c08f6484a7377c3ca3f16a9833d6` |
| 6 | `0x7dd26477c7f86a1d4cdfaeb73741577def7905ef` | 23225360 | 10 Nov 16:13:28 | `0xa90caaf3cdc40a5c5f0b6a52bdf2a4fc8887a62d7418a0b0c62d8ae222480073` |
| 7 | `0xf52b7eba863ee3378cc9dd60efd62df1bb08f567` | 23225410 | 10 Nov 16:13:58 | `0x8075169c584b0b616874fa91513f017fd45fe7eae30e5a1568825a803c6f6dc9` |

- `AuditorKeyGiven` remains **4** (the first 3 above + `0x23c5a5138ad66ff376a7a20248ec47a64d7b3fc9`, block 23224952, 10 Nov 16:09:19 UTC, tx `0x6d7df5de9919f9d52b1b7f9dd100141c8def1063a1df25f1bad7409548a1690c`).
- `AuditorPersonalKeySet` remains **1**: `0x23c5a5138ad66ff376a7a20248ec47a64d7b3fc9`, block 23223818, 10 Nov 15:57:51 UTC, tx `0x787bbe3cd3369aa325fdfbebf8b41e7554270c8867ca82505acd5f1e0edaf9a5`.
- **So: 7 auditors registered, only 4 with `AuditorKeyGiven` — same as the baseline, no additions.** Never write "7 auditors received keys" — that is wrong; the correct statement is 7 registered, 4 with keys.
- **No on-chain event shows decryption/auditing by an auditor** (no audit event in the vault/registry logs). This is consistent with the previous article's conclusion, which still stands (A.2).

### D.6 New usernames — 131 since 15 Nov (verified fact)

Total **194 usernames, all unique, 1:1 with 194 registered addresses**. The first username remains `rayls-relayer` (`0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8`, 10 Nov 13:58 UTC). List of the 131 new usernames (chronological order, 16–21 Nov):

deepsync, testing, api_1, api_2, notyourbunnyy, testingg, 9ytshade, qa-test, aashy, monarch321, momonen, lotosbi, jil, wallet_101, fujiyama, andro, freeboy_dev, compi, richar, yuno, zolas, rayls_guest_2026, solcops-test, alanxft, vol, eddi, pavel, tomas, romunas, mantas, kristof, max, oleg, stasis, heismellow, vasiliy, sergey, yuriy, gerda, polina, qa-fb7k3a, qa-fb7k3b, metalawyerdemo, qa-dn7k2, qa-leo-dn7k, permit_after_e2e, permit_before_e2e, tenant-a-45x8d8, tenant-b-b2fg4a, tenant_a, tenant_b, tenant_01, tenant_02, testing0890, shakthi, tenant_03, eric, amulu, tenant_04, niceguy, swimfanimfan, lavanya, ralys, nishu, 9874, 0764, subbu, selvam, sathya, 7542, 9078, tenant_g1, tenant_g2, 0xstauf, qual-a-3adeae04, qual-b-3adeae04, mb-piloto-dev, rls-333, yetu891, horizontev-dev, r20-cofre-dev, coinlayer, bosqu99, dino, oshadha44, sooody, windut39, demo22, cahusil65, lazarus, ghostwalker, footprinta, meta, demo111, niloy34, theobullish, jianeth, rizkymahreza, cryptoram89, cryptoram3669, 0xwysi, cryptoram01, ikihin, kobe, tiny91511, tinyb48213, mr_aniqul, hanbongdubong, ted, tupro, maxwellifeanyi, hanbongdubong2, maxoil, blazetorc, railfeetrace1, railfeetrace2, immortal, 798879, bankiakun, fengzheng, tesgin123456789, fengzheng2, swapspeedtest1120, smsms, testing099789, testging9876, falcongr, god, rq3dev26, devil, rq3faucet26.

The full address + tx hash mapping per name was verified from the logs. First example: `deepsync` = `0x98de6a698d5dc11173e82ba71da701645b606db5`, 16 Nov 12:50 UTC, block 24082221, tx `0x67e579e18c80d6f4690fd51b3b0e3d11a8d00b49244d9725fd18aa9f266168e7`. Last: `rq3faucet26` = `0xe1136dcf839c4ad2704094241928fa2896a118c5`, 21 Nov 00:39 UTC, block 24766266, tx `0x0c7419d5d3d334dae29f5e87bdde78481ed61b6ae2907429044b4e56903beb0a`.

**Pattern note (inference, not an identity fact):** many names are testing/QA-themed (`qa-test`, `qa-fb7k3a`, `permit_after_e2e`, `tenant_*`, `testing*`, `demo*`, `swapspeedtest1120`) — this activity appears to be dominated by internal/developer testing, not organic end users. Do not claim identities behind these names without evidence.

### D.7 Transaction-type classification from event combinations (reconstruction)

The three actions **can be identified separately** from the event combination per tx (511 yx vault tx). The classification rules used (explicit, reproducible):

| Type | Rule (events within one tx) | Tx count |
|---|---|---|
| Shielding (in) | Only `Commitment` + `EncryptedNote`, no `Nullifier`/payout | **272** |
| Shielded transfer (spend without exiting) | `Commitment` + `EncryptedNote` + `Nullifier`, no `PaidOut`/`PartialWithdrawal` | **188** |
| Unshielding (out) | `Commitment` + `Nullifier` + `PaidOut` + `PartialWithdrawal` (35 tx; 6 additional tx also carry an `EncryptedNote`, i.e. a change note) | **41** |
| CoinLocked only | Only `CoinLocked` (nullifier lock, 30 Oct–3 Nov) | 5 |
| Admin | `RoleGranted`/`Upgraded`/`Initialized` | 3 |
| **Total** | | **511** |

Status label: **reconstruction** — this classification was built from event patterns, not from protocol labels. The rules are explicit so they can be re-checked, but the "shielding" vs "transfer" interpretation follows event semantics, not confirmation from the team.

### D.8 Unshielding — fully public (verified fact)

- **41 unshieldings**, the per-tx amounts **match exactly** between `PartialWithdrawal` and `PaidOut` (**0 mismatches**).
- `PartialWithdrawal(vaultId, recipient, amount, changeCommitment)` — the amount is in the plaintext `data`; `PaidOut(vaultId, token, recipient, amount)` — token + recipient in the topics, amount in `data`.
- Total ≈ **752.58 tokens** (18-decimal reading):
  - RLS `0x07e17e17e17E17e17e17e17E17E17E17E17e17EA` — 196.6795808 (14x)
  - USDr `0x0000000000000000000000000000000000000400` — 20.7 (16x)
  - `0x3ab29f9e8ef3a730731eda5e88eaf986ff824b4d` — 10.0 (1x)
  - `0xc66cb3ce397e70888e69d6e7e75474046c6617e4` — 500.0 (1x)
  - `0x076e2256c36196fce6e4cb7537f1edeb27d3a6b3` — 20.0 (1x)
  - `0x68660d8de06045f80c749400abc347081073ff5f` — 5.2 (2x)
  - Dust: `0xf4cf04f4173fbff71a8718517199e57e11b20af0` — 2 wei (2x); `0xe50ab75c55db6a98d6e2d89496e54e4f5a391523` — 500,000 wei (1x); `0xc81b66f670124d345b1a60165192508e31d39150` — 1,500,000 wei (3x)
- Amount range 1 wei–500 tokens. **33 distinct recipients, 9 distinct tokens.** All `vaultId = 2` (shared vault).
- **Caveat (important):** decimals of non-RLS/USDr tokens are **unknown**, so the combined total is only meaningful under an 18-decimal reading — do not present "752.58 tokens" as a single volume figure without this caveat.

### D.9 What is visible and not visible from the logs (verified fact)

**Publicly visible:**
- Unshielding: recipient address, token, amount (D.8).
- Registration: address + plaintext username (`UsernameSet`), plus `UserRegistered` with `data` still **5,186 bytes** (ML-KEM + AES view-key escrow ciphertext, per the bundle ABI) — its contents are encrypted, but its existence + size + address are public.
- The relayer submits all tx: of the 4 tx checked via `eth_getTransactionByHash`, `from` is always **`0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8`** (username `rayls-relayer`). Examples: shielded transfer `0xee8b31ad3d0f00437ce36d4058af16f08af5c4103a60c896da34ad0bbf359211` (`to` = yx vault); unshield `0x282db91e109533bfd1e89ddde65021ec36ef38d54b721a64ed368855dbf19110` (`to` = old yx forwarder); registration `0x0c7419d5d3d334dae29f5e87bdde78481ed61b6ae2907429044b4e56903beb0a` (`to` = **new** forwarder `0x12B6640048DEB2e8fFDa4Bc10Bb2a640B70eCA6d`); latest vault tx `0x7f72b00105ab01cb600461487dad6ff7932bdb302c6a85d00a01b67df3117dd1` (`to` = Multicall3 `0xca11bde05977b3631167028862be2a173976ca11`) — consistent with the docs claim that shielded payments are sent via Multicall3 by the relayer.

**Not visible (shielded payment):**
- `Commitment` — `data` empty (`0x`), only a hash in the topic.
- `Nullifier` — `data` empty, only a hash.
- `EncryptedNote` — `data` always **1,312 bytes** of ciphertext (847 logs, identical size).
- No amount, sender/recipient address, or token in these logs.

**Unknown from this check:**
- The indexed `topics[2]`/`topics[3]` values on `UserRegistered` — the explorer API returns `null` for both in all 194 logs (an API quirk, not empty data); the meaning of those fields cannot be determined from these logs.
- Whether any shielding activity has amounts visible through ERC-20 token logs (not collected in this task).

### D.10 Summary of changes vs the 15 Nov baseline (verified fact)

1. **Activity surged, not died:** yx registry +131 new users (194 total), yx vault +307 tx (511 tx / 2,128 logs total). Latest activity: registry 21 Nov 00:39 UTC, vault 21 Nov 03:25:55 UTC.
2. **No new auditors** — still 7 registered / 4 with keys, all from 10 Nov.
3. **Bundle rebuilt** (hash + filename changed, new chunking), but **contract addresses and deployment configuration unchanged**; `retired: 2026-11-10` remains.
4. **Docs unchanged** since 11–12 Nov; the wording tension over scoped keys (blog vs Private Network doc) remains.
5. **New finding:** the live **bx** proxy implementations **do not match the bundle** (the bx upgrade was never executed; the bundle shows a "next" implementation that is not active). The live yx implementations match the bundle.
6. **No RPC failed**; the only obstacles were the explorer API's 1,000-result cap and one HTTP 403 from urllib without a User-Agent (resolved with curl + UA).

---

## E. Feasibility of measuring transaction and token volume

### E.1 Three volume categories — must be distinguished explicitly

| Category | Definition | Status for this testnet |
|---|---|---|
| **Observed volume** | Figures read directly from the logs (log/tx counts, unshielding amounts, registration counts) | **Measurable with certainty** — see E.2 |
| **Reconstructed volume** | Figures processed under explicit rules (tx-type classification D.7; counts per day) | **Measurable with caveats** — the rules must be stated; not protocol labels |
| **Estimated volume** | Estimates of what is not observed (e.g. total shielded transfer value) | **Cannot be made responsibly** — no estimation basis from public data |
| **Unobservable activity** | Activity that by design is not visible (amounts/parties/tokens of shielded transfers; Sovereign activity on private networks) | **Not measurable from the public explorer** — do not treat its absence as evidence |

### E.2 What can actually be measured

- **Registrations:** exact counts (194 usernames / 194 addresses), the full list, time and block per registration, address ↔ username mapping (D.1, D.6). All of this is direct observation.
- **Unshielding:** tx count (41), amounts per tx and totals per token (D.8), recipients (33 distinct), tokens (9 distinct). The `PartialWithdrawal` vs `PaidOut` amounts match exactly — a strong internal cross-check.
- **Tx counts per type:** 272 shielding / 188 shielded transfers / 41 unshielding / 5 locks / 3 admin (D.7) — reconstruction under explicit rules.
- **Activity over time:** log/tx counts per day can be computed from block timestamps; growth since the baseline is measurable (+131 users, +307 vault tx in 6 days).
- **Relayer submissions:** `from` is always `0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8` in the sample checked; this pattern can be tested on all 511 tx (follow-up work, not yet done).
- **Contract upgrades:** the `Upgraded` events + EIP-1967 slots give a verifiable implementation history (C.3).

### E.3 What cannot be measured

- **Total shielded volume (amounts of transfers between shielded balances):** there is no amount in the `Commitment`/`Nullifier`/`EncryptedNote` logs. There is no public way to sum it.
- **Incoming shielding volume (amounts):** shielding amounts are not visible from the vault logs; their ERC-20 token transfer side was not collected in this audit (unknown — see G.2).
- **Combined volume across all tokens:** the "≈752.58 tokens" figure is only meaningful under an 18-decimal reading and mixes different tokens whose decimals are partly unknown (D.8). Do not present it as a single volume figure without the caveat.
- **The actual number of active users:** 194 registered addresses ≠ 194 humans — many usernames look like testing/QA accounts (D.6). The number of unique users cannot be inferred from the number of addresses.
- **Economic value (USD):** there is no market price for testnet tokens; do not convert to USD.

### E.4 Double counting — pitfalls to avoid

1. **`PartialWithdrawal` + `PaidOut` = one event.** Both record the same payout; summing both doubles unshielding volume. Count it once (41 payouts, not 82).
2. **`Commitment` ≠ a payment.** Commitments appear in shielding (272 tx) as well as transfers (188 tx); 888 Commitment logs are not 888 payments.
3. **One tx can produce many logs.** The correct counting unit is **unique tx per type** (D.7), not the raw log count (2,128 vault logs ≠ 2,128 transactions; the correct figure is 511 tx).
4. **Shielding vs transfer vs unshielding are three different economic events** — do not sum them into a "total Enygma transactions" figure without explaining the composition.
5. **`EncryptedNote` logs 847 vs `Commitment` 888:** the difference of 41 = the number of unshieldings (which create no new note, except for 6 change-note tx). This internal consistency supports the D.7 classification rules — a coherent reconstruction, not a coincidence.

### E.5 Reproducible data-collection method

Following the mainnet repo standard (A.1) and reviewer feedback:

1. **RPC commands (general pattern):**
   - `curl -s -X POST https://testnet-rpc.rayls.com -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"eth_chainId","params":[]}'`
   - `eth_blockNumber`, `eth_getCode`, `eth_getStorageAt` (EIP-1967 slot `0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`), `eth_getTransactionByHash` — the same pattern.
2. **Explorer log commands (pagination mandatory):**
   - `curl -s -A 'Mozilla/5.0' 'https://testnet-explorer.rayls.com/api?module=logs&action=getLogs&address=<addr>&fromBlock=<n>&toBlock=<n>'` — max. 200,000-block range per call (1,000-result cap). Without a User-Agent, urllib once hit HTTP 403; use curl + UA.
3. **Bundle:** download the page + `assets/index-Dlv-HYaZ.js`, record byte sizes and SHA-256 hashes (C.4).
4. **What must be recorded at every data collection (reviewer feedback):** the client version used (here: curl + the explorer API, not a self-run node), block identifiers (start/end block of each window), the UTC timestamp of collection, and dataset checksums. The research repo must later store raw JSON + CSV + metadata JSON + verification scripts, following the mainnet repo pattern (see H).
5. **Cross-checks already performed:** `PartialWithdrawal` vs `PaidOut` (0 mismatches); EIP-1967 slots vs bundle; bundle hashes vs baseline; log counts vs unique tx.

### E.6 Issues still unresolved (do not resolve them with assumptions)

- **The 0.0001 RLS fee discrepancy: UNRESOLVED.** Never call it rounding. It needs its own fee testing (G.3) and/or team context via ticket.
- **Proof-time figures** (408 ms / ~2.2 s / ~3 s / "under 4 s") differ across official sources — not yet tested (G.4).

---

## F. Data limitations caused by the privacy mechanism

### F.1 What leaks to the public by design (inference from facts + official claim)

1. **Shielding/unshielding leak address + token + amount publicly** — for unshielding proven from the vault logs (D.8); for shielding, this claim comes from the docs and has **not been verified from token logs** in this audit (only from vault logs + docs claims).
2. **Registration leaks the address ↔ username mapping for all 194 accounts** (D.6) — fully public data, including for accounts that appear to belong to the team/testers.
3. **Activity patterns are visible:** the number of shielding vs transfer vs unshielding per day, and frequency per vault — but **not** who paid whom or how much in shielded transfers.
4. **The relayer is fully identified** (`0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8`, username `rayls-relayer`) — every vault/registry tx checked was submitted by it.

### F.2 What is hidden by design

- Shielded transfer: no sender, recipient, amount, or token in the logs (D.9). This is the core of Enygma Public privacy — and at the same time the limit on volume measurement (E.3).
- The contents of `UserRegistered` (5,186 bytes) and `EncryptedNote` (1,312 bytes) are ciphertext; their size and existence are public, their contents are not.

### F.3 Auditor — what is claimed vs what is proven

- **Official claim (docs `who-sees-what`):** "The auditor… Every shielded transaction, decrypted: who paid whom, the amount and the token." The auditor holds the keys to decrypt everything — this is by design, not a leak to the public.
- **Verified fact:** 7 auditors registered, 4 with keys, no changes since 10 Nov; no on-chain event shows decryption/auditing.
- **Not yet proven:** whether selective auditing is actually performed/tested on this deployment, and whether its scope is per deployment (Public doc), network-wide (Private Network doc), or scoped keys (blog). **The previous article's conclusion still stands.** The three conflicting official wordings are presented in C.6 — team context via ticket is needed before the article concludes anything about auditor scope.
- **New context from GitHub (B.2):** auditor key-escrow code exists in `enygma_retail_payments`. This strengthens the case that the auditing mechanism was designed/implemented in one module — but it is still not proof of live verification.

### F.4 Other limitations not related to privacy

- **Enygma Sovereign activity on institutional private networks is not visible through the public explorer.** The absence of public data about Sovereign is not evidence of the absence of activity. The article must explain this separation explicitly.
- **The bx deployment has been silent since 3 Nov** (4 + 10 logs, unchanged) — this is a log fact, not proof that bx is "dead"; the status and plans for bx are **unknown, needs team context**.
- **`topics[2]`/`topics[3]` data on `UserRegistered` is `null` in the explorer API** — an API quirk, not empty data; the meaning of the fields cannot be determined from this source.
- **The RLS token implementation-slot anomaly** (C.3) — unknown, not verified further.

---

## G. Opportunities for new experiments

**Recommendations only — nothing was executed in this audit.** All experiments below require Anara's approval before being run, and their results must be matched against tx/RPC/contracts/event logs/ABI/GitHub source following the planned article structure (introduction → architecture → historical activity → verified volume → experiments → matching → conclusions on what was observed vs what cannot yet be confirmed).

### G.1 Core experiment: the full shield → transfer → unshield flow

- Create a new testnet wallet, request the faucet (1×/hour, per the pilot blog), then perform registration → shielding → shielded transfer to a second address → unshielding, each in a small and distinct amount so it can be traced.
- For each step, record: tx hash, block, the event logs that appear, and compare against the D.7 classification (does the experiment's event pattern match the reconstruction rules?). This directly tests whether the three actions are indeed separate as classified.
- Test whether shielding produces ERC-20 token logs that reveal the amount (closing the gap in F.1 point 1).

### G.2 Test shielding visibility through ERC-20 token logs

- Fetch the `Transfer` logs of the testnet RLS token (`0x07e17E17e17E17e17e17e17E17E17E17E17e17EA`) and USDr (`0x0000000000000000000000000000000000000400`) over the same block range as the yx vault, then match them against the shielding tx (272 tx). Question: is the shielding amount publicly visible through token logs even though the vault logs do not show it?

### G.3 Test fees and the 0.0001 RLS discrepancy

- Measure the actual fee per action (registration, shielding, transfer, unshielding) from the experiment tx receipts; compare against the docs claims (relayer 15% to the Rayls Foundation; USDr +0.25%) and investigate the origin of the still-unresolved 0.0001 RLS discrepancy. **Do not call that discrepancy rounding until there is evidence.**

### G.4 Test proof time

- Measure proving time locally (or record the time from the demo UI) and compare against the four mutually differing official figures (408 ms / ~2.2 s / ~3 s / "under 4 s"). Record the device, input size, and network conditions — figures without context are meaningless.

### G.5 Test the bx deployment and the "next" forwarder

- Try the demo with the bx configuration: is bx still usable, or is it really only an early deployment that was not continued? Confirm via ticket first (C.3) before concluding anything in public.
- Watch whether new registrations keep using the forwarder `0x12B6640048DEB2e8fFDa4Bc10Bb2a640B70eCA6d` (already seen on the latest registration, D.9) — this tests whether a forwarder rotation is underway.

### G.6 Continuous monitoring and finality (reviewer feedback)

- Extend observations to more dates/times or continuous monitoring (not just two snapshots on 15 Nov and 21 Nov) — for example, daily recording of tx counts per type over a week.
- A separate finality experiment if possible (time until a tx is considered final according to the RPC/explorer).
- A controlled load test only in a suitable environment — not by flooding the public testnet without consideration.

### G.7 Reading material and context before experimenting

- Review the IACR ePrint papers **2025/1638** (Rayls II) and **2025/1639** (Rayls) — new sources not in the previous research.
- Re-read `protocol_description.md` (blob `61b9447217a881dd3e47f7ade3fcc8d5e4df9a0f`) and the `enygma_retail_payments` code (`auditor.go`, `UserRegistry.sol`) to explain the auditor key-escrow mechanism accurately in the article.
- **Ticket-first (moderator guidance):** before publishing conclusions about (a) the bx proxy vs bundle mismatch, (b) auditor-access scope, (c) the 0.0001 RLS fee discrepancy, (d) the RLS token slot anomaly — open a ticket so the team can provide context. The mod does not mind receiving tickets even if replies take time.

### G.8 What is NOT recommended

- Do not try to become an auditor (docs: "Nobody can ask to be an auditor. An existing auditor adds new ones.").
- Do not conclude anything about Enygma Sovereign from the absence of public data.
- Do not present "volume" figures that mix different tokens without the decimal caveat (E.3).

---

## H. Recommended research repository structure

**Recommendations only. No new repo was created in this audit.** The proposed name `rayls-enygma-public-testnet-research` has not been approved to be created/published; create and publish it only after Anara's approval. The structure below follows the mainnet repo pattern (A.1) that has already proven itself by passing review (90/100):

```
rayls-enygma-public-testnet-research/
├── README.md                    # research question, network, method, verified results,
│                                # interpretation + limitations, official references, source snapshot (commit hash)
├── data/
│   ├── raw/                     # raw RPC + raw explorer API responses (JSON, as-is)
│   ├── csv/                     # processed datasets: registrations.csv, unshielding.csv,
│   │                            # vault-tx-classification.csv, daily-activity.csv
│   ├── metadata.json            # chain_id, rpc, method, start/end block, retrieved_at_utc,
│   │                            # client/version, SHA-256 of each dataset (mainnet repo pattern)
│   └── checksums.sha256         # checksums of all datasets
├── scripts/
│   ├── fetch_logs.py            # 200,000-block pagination (API cap of 1,000 results)
│   ├── classify_tx.py           # D.7 classification rules (explicit, re-checkable)
│   ├── verify_dataset.py        # verify CSV vs raw + PartialWithdrawal vs PaidOut
│   └── reproduce.py             # re-fetch a fixed block range
├── contracts/
│   ├── addresses.md             # contract map C.2 + EIP-1967 slots C.3
│   └── abis/                    # ABIs from the demo bundle (if available)
├── bundle/
│   ├── bundle-hashes.md         # page and bundle sizes + SHA-256 per date (C.4)
│   └── deployments-7295799.md   # contents of 7295799.json / br/7295799.json / 11155111.json
├── docs-review/
│   └── docs-wording.md          # update dates + verbatim quotes from each docs/blog page (C.6)
├── experiments/
│   ├── plan.md                  # experiment plan G.1–G.6 (not yet executed)
│   └── results/                 # experiment results + tx hashes + receipts (after approval & execution)
├── findings/
│   ├── verified-facts.md
│   ├── official-claims.md
│   ├── reconstructions.md       # rules + processed results, kept separate from facts
│   ├── unknowns.md              # list of unknowns + tickets opened
│   └── tickets.md               # ticket log to the Rayls team (date, content, answers)
└── audit_report.json            # machine-readable summary (mainnet repo pattern)
```

**Documentation principles to preserve:** (1) raw data is always stored as-is + checksums; (2) processed data (reconstruction) is kept separate from facts and its rules are written explicitly; (3) every data collection records client/version + block identifiers + timestamp; (4) limitations are explained in the README, not hidden; (5) observed vs reconstructed/estimated vs unobservable are distinguished for every volume figure; (6) no hash/address is invented — unknown is written as unknown.

---

## I. List of sources, commit hashes, contract addresses, transaction hashes, and file paths actually found

### I.1 Network and endpoints (verified fact)

- Testnet chain ID: **7,295,799** (`0x6f5337`); mainnet: 72,957
- RPC: `https://testnet-rpc.rayls.com`
- Explorer: `https://testnet-explorer.rayls.com`
- Demo: `https://enygma-testnet.rayls.com/`
- Relayer: `https://enygma-relayer-aafjr.ondigitalocean.app/rayls` (7295799), `https://enygma-relayer-aafjr.ondigitalocean.app/sepolia` (11155111)

### I.2 Contracts (all addresses complete — from C.2/C.3)

- Testnet RLS token (proxy): `0x07e17E17e17E17e17e17e17E17E17E17E17e17EA`
- Ethereum mainnet RLS token: `0xb5f7b021a78f470d31d762c1dda05ea549904fbd`
- RlsGasForwarder (yx): `0x753cc3Abe9A1c49536ee74F1f424fCF693AAB5DD`
- UserRegistry proxy (yx): `0xA473291FFb33e2276F364fAE169f03c4406719e9`
- SharedVaultProxy (yx): `0x9C5Ad5e5Ea5b5910E7fD1E1CC7b70ce0e4bF06c2`
- UsdrVault: `0x1edb224cf8637f92efadaf47ef9e70c044d75584`
- RlsVault: `0x97b5d78dbe06d8c8c843f87b5aa2d8587b890795`
- Verifier: `0xfa3a53ec650bfd4ca3e8461abce243382a1037af`
- GenericGroth16Verifier: `0xc12f06f883b757c91069f9d94065a4c673ef356a`
- Poseidon T3: `0xc29f02220d8aed5c731de4aee9d7d8d24c94ef15`
- Poseidon T5: `0x078c99bbbbf9dcf827ff085c9a4634213b18018b`
- Poseidon Wrapper: `0x0bc72bf5dd894164f7cc8f8b92c78eb7d2156f3f`
- OwnerMultisig: `0xBf099175a241194C38E977735D59CCb22596d775`
- UserRegistryRetired (yx): `0xD1d92f1B183B84Ea528211302B1eCB881EeF2770`
- RlsGasForwarder (bx): `0x2ef592329B8e01320170f8f8d759d9bcA94d1066`
- UserRegistry proxy (bx): `0x3E9435c1fe8432e21E80D7A8ab81EBfc8eC708E3`
- UserRegistryImplementation (bx, in bundle): `0xB23124D2eE339d1E8175B9ec10D20217CE015c1C`
- SharedVaultProxy (bx): `0x94dafa3bf372cad68143ac535f845e74751d75ef`
- TokenFactory (bx): `0x7416094FFC5A1D0C2659DA0D5b81CeCc18f1BdAc`
- Auditor (EOA): `0x71AF09966CBED4434ccA97c40Fa38B8083548B95`
- Relayer: `0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8`
- Multicall3: `0xca11bde05977b3631167028862be2a173976ca11`
- Forwarder "next" (yx): `0x12B6640048DEB2e8fFDa4Bc10Bb2a640B70eCA6d`
- EnygmaDvp: `0x7ec57a8f97b636a4b54633df826b2a4311018996`
- Live registry yx implementation: `0x9686a3d5a9Fd2101d15888c6a09a64faFA7EE349`
- Live vault yx implementation: `0xAd9667049f14D1757D147F652c41Dc241C57091C`
- Live registry bx implementation: `0x66f87eaf23152bd5a155f96a85b7e5a64e3f6952`
- Live vault bx implementation: `0x8551f451a5e7dc39d82ed08195eeda16abfe60a1`
- SharedVaultImplementation bx (in bundle): `0xe023791669A54EC41Ef1affA2c1B44460C1943CD`
- `auditorPublicKeyHash` of the yx registry: `0x4151c50e9250f5818a53f9e48e734bd4209407d19f966ede4f7988dd4af863e5`
- USDr: `0x0000000000000000000000000000000000000400`
- Other unshielding tokens: `0x3ab29f9e8ef3a730731eda5e88eaf986ff824b4d`, `0xc66cb3ce397e70888e69d6e7e75474046c6617e4`, `0x076e2256c36196fce6e4cb7537f1edeb27d3a6b3`, `0x68660d8de06045f80c749400abc347081073ff5f`, `0xf4cf04f4173fbff71a8718517199e57e11b20af0`, `0xe50ab75c55db6a98d6e2d89496e54e4f5a391523`, `0xc81b66f670124d345b1a60165192508e31d39150`
- Address with unknown provenance: `0xd908BaeE382191D15E479589D9661A9E9b55b827` (from `address.json` in the repo)

### I.3 Transaction hashes actually found

- yx registry upgrade: `0x908fdae3efbee9b058da2088eaf73f7f0031257df79953974fb87b1c5ac96fe8` (block 23,400,006, 11 Nov 21:25:18 UTC)
- yx vault upgrade: `0xc841126f7cf05d937967743f7db5cb80d04cf32ed1dca929aac23d952e97f3c4` (block 23,399,976, 11 Nov 21:25:01 UTC)
- Latest registration (yx registry): `0x0c7419d5d3d334dae29f5e87bdde78481ed61b6ae2907429044b4e56903beb0a` (block 24766266, 21 Nov 00:39 UTC, username `rq3faucet26`)
- Latest vault tx: `0x7f72b00105ab01cb600461487dad6ff7932bdb302c6a85d00a01b67df3117dd1` (21 Nov 03:25:55 UTC, `PaidOut`)
- First registration recorded in the new list: `0x67e579e18c80d6f4690fd51b3b0e3d11a8d00b49244d9725fd18aa9f266168e7` (`deepsync`, block 24082221, 16 Nov 12:50 UTC)
- Shielded transfer (example): `0xee8b31ad3d0f00437ce36d4058af16f08af5c4103a60c896da34ad0bbf359211`
- Unshield (example): `0x282db91e109533bfd1e89ddde65021ec36ef38d54b721a64ed368855dbf19110`
- Seven `AuditorAdded` tx: listed in full in D.5
- 4th `AuditorKeyGiven` tx: `0x6d7df5de9919f9d52b1b7f9dd100141c8def1063a1df25f1bad7409548a1690c`
- `AuditorPersonalKeySet` tx: `0x787bbe3cd3369aa325fdfbebf8b41e7554270c8867ca82505acd5f1e0edaf9a5`
- yx registry implementation tx in bundle: `0xe029bde6…` — **recorded truncated, full hash unknown** (block 23395761)

### I.4 Commit hashes and GitHub files

- `raylsnetwork/Enygma` head: `0b1945ae6c827745d1ad48eddcec39df4b20277a` (19 Nov 2026, 22:48 UTC)
- Comparison baseline: `3c61be782cbd31b108eacbda662d3a0a9219f6ae` (71 commits behind head)
- `protocol_description.md` blob: `61b9447217a881dd3e47f7ade3fcc8d5e4df9a0f` (37,302 bytes, unchanged)
- DvP ciphertext binding: commit `6a6a23b1cffde9b4e3a37e27375ddff9ed397578` (16 Nov 2026) — `CiphertextHash.sol` + tests + salt changes
- Relevant files: `enygma_retail_payments` (`auditor.go`, `UserRegistry.sol` — `mlKemAuditCt`/`aesAuditCt`); `enygma_payments` (no auditor role); `enygma_demo` (unchanged since 29 Oct 2026)
- Previous research repo: `github.com/akira01111/rayls-enygma-research`, head `ab523db`, 4 commits
- Mainnet repo (quality-standard reference): `/home/hatch/workspace/rayls-mainnet-block-research-check`, commits `4ef462f` and `a514353`

### I.5 Bundle and page hashes

- Demo page 21 Nov: 3,872 bytes, SHA-256 `d709dc0639a80d71b127681fbd56ae7f6f9a9f83c38bf4b7f42239b4b961a28e` (baseline: 3,645 bytes, `b615fd73aa999fb72529d37553ba0943d754e2f2e0f50468a07fe2e8fcb636c5`)
- Main bundle 21 Nov: `assets/index-Dlv-HYaZ.js`, 1,422,052 bytes, SHA-256 `7530bbc2d7a301c50e28923529cb9315f88145a9a25a7c71db8a1f34afd9ca68` (baseline: `index-BmNruHc0.js`, 1,338,924 bytes, `c878b635cab69d9c529f4cd9e6fcd8fb606c0e2a9a3bd42af39ea435f065ec81`)

### I.6 Docs and publications (dates + links)

- `docs.rayls.com/docs/enygma-privacy-and-auditing` — updated 2026-11-11T15:26:41.000Z
- `docs.rayls.com/docs/enygma-public` — updated 2026-11-11T21:36:24.000Z
- `docs.rayls.com/docs/enygma-public-who-sees-what` — updated 2026-11-11T21:36:27.000Z
- `docs.rayls.com/docs/how-enygma-public-works` — updated 2026-11-11T15:27:18.000Z
- `docs.rayls.com/docs/rayls-high-level-architecture` — updated 2026-11-11T21:37:02.000Z
- Blog `rayls.com/blog/auditability-without-surveillance-…` — published 2026-09-12, updated 2026-11-12
- Blog "controlled visibility" — updated 15 Nov 2026
- Rayls pilot blog — 12 Nov 2026 (AES-256-GCM + ML-KEM + HKDF; faucet 1×/hour; roadmap) — exact URL not recorded in this audit (unknown)
- IACR ePrint **2025/1638** (Rayls II) and **2025/1639** (Rayls)
- Previous article: X `status/2122127310585524690` (16 Nov 2026)

### I.7 Local file paths

- This report: `~/workspace/rayls-enygma-audit/ENYGMA-TESTNET-AUDIT-REPORT.md`
- Previous research folder: `~/workspace/rayls-enygma-research/` (README.md, ama/ama-notes.md, audit/audit-status.md, demo-testing/, findings/, research/, sources/source-register.md, technical-evidence/technical-evidence.md)
- Quality-standard reference repo: `~/workspace/rayls-mainnet-block-research-check/` (README.md, rayls_blocks.csv, recent_600_blocks.csv, recent_600_metadata.json, recent_600_raw.json, reproduce_fixed_600.py, verify_dataset.py, windows/, audit_report.json)

### I.8 What is deliberately absent from this list

No hashes/addresses/test results were invented. Everything not found is marked **unknown** in its own section (among others: the full hash of the yx registry implementation tx in the bundle; the meaning of the RLS token implementation slot; decimals of non-RLS/USDr tokens; the meaning of `topics[2]`/`topics[3]` on `UserRegistered`; the exact pilot blog URL; the origin of address `0xd908BaeE382191D15E479589D9661A9E9b55b827`).

---

## Closing — audit status

This initial audit is **complete** as briefed: the report A–I above is the only output. No experiment was run, no repo was created, no article was written, no publication was made, no transaction was sent.

**Next steps requiring Anara's decision/approval:**
1. Review this report; decide whether to open ticket-first to the Rayls team for the bx finding, auditor scope, the 0.0001 RLS fee, and the RLS token slot anomaly.
2. Approve/reject creating the `rayls-enygma-public-testnet-research` repo (the structure in H is only a proposal).
3. Approve/reject experiments G.1–G.6 (each needs approval before being run).
4. Only after that can article writing begin — with the previous article's conclusions still standing unless new evidence comes from experiments/tickets.
