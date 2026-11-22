# Audit Teknis Awal — Rayls Enygma Public Testnet

**Tujuan:** audit read-only untuk persiapan konten riset Rayls Week 3 (tutup Minggu 22 November 2026, 23:59 UTC).
**Tanggal audit:** 21 November 2026 (pemeriksaan on-chain ~04:50–05:00 UTC / 11:50–12:00 WIB; pemeriksaan GitHub 21 November 2026).
**Sifat:** READ-ONLY. Tidak ada transaksi, tidak ada koneksi akun eksternal, tidak ada perubahan file/repo, tidak ada publikasi, tidak ada pengeluaran dana.
**Output:** laporan ini saja. Bukan artikel, bukan eksperimen, bukan repo baru.

## Taksonomi bukti (6 label — mengikat untuk seluruh laporan)

1. **verified fact** — terbukti langsung dari sumber primer yang diperiksa (RPC, log explorer, file repo, bundle) dan dapat dicek ulang.
2. **official claim** — dinyatakan resmi oleh Rayls (docs, blog, AMA) tetapi belum diverifikasi independen dalam audit ini.
3. **direct observation** — apa yang benar-benar terlihat/terukur dalam pemeriksaan ini (angka log, hash, ukuran file), tanpa penafsiran lebih jauh.
4. **reconstruction** — hasil olahan dari data mentah dengan aturan eksplisit (mis. klasifikasi tipe transaksi dari kombinasi event); dapat direproduksi bila aturannya diikuti, tetapi bukan label dari protokol.
5. **inference** — penafsiran yang masuk akal dari bukti yang ada; ditandai jelas sebagai dugaan, bukan fakta.
6. **unknown** — tidak ditemukan / tidak dapat diverifikasi; kekosongan tidak diisi asumsi.

**Aturan penulisan:** alamat kontrak dan hash ditulis LENGKAP, tidak disingkat. Klaim dokumentasi tidak disamakan dengan implementasi yang terverifikasi. Ketidakhadiran data publik tidak diperlakukan sebagai bukti (aktivitas Enygma Sovereign di jaringan privat institusi tidak terlihat lewat public explorer). Temuan yang tampak janggal dicatat sebagai "perlu konteks tim via ticket" sebelum menjadi kesimpulan publik.

## Ringkasan temuan

1. **Testnet masih aktif dan justru makin ramai.** Chain ID terverifikasi ulang: **7.295.799** (`0x6f5337`), RPC `https://testnet-rpc.rayls.com` hidup, blok terakhir saat dicek **24.793.989** (21 Nov 04:50:45 UTC). Vault yx tumbuh dari 803 log / 204 tx (baseline 15 Nov) menjadi **2.128 log / 511 tx**; registry yx dari 143 log / 76 tx menjadi **405 log / 207 tx** dengan **131 username baru** (16–21 Nov). Aktivitas terakhir: registry 21 Nov 00:39 UTC, vault 21 Nov 03:25:55 UTC.
2. **Tidak ada auditor baru.** Tetap 7 `AuditorAdded`, 4 `AuditorKeyGiven`, 1 `AuditorPersonalKeySet` — semuanya dari 10 Nov 2026. Kesimpulan artikel sebelumnya — *selective auditing pada deployment Enygma Public yang diuji belum dapat diverifikasi secara independen* — **TETAP BERLAKU**; tidak ada bukti baru yang mengubahnya.
3. **Bundle demo di-build ulang, konfigurasi tidak berubah.** Halaman dan bundle utama berganti hash dan nama file (kini terpecah jadi banyak chunk), tetapi semua alamat kontrak dan file deployment (`7295799.json`, `br/7295799.json`, `11155111.json`) sama; flag `retired: "2026-11-10"` tetap.
4. **Temuan baru — implementasi live proxy bx tidak cocok dengan bundle.** Upgrade bx yang tercantum di bundle (via `ownerCalls`) tidak pernah dieksekusi di proxy: implementasi live registry bx (`0x66f87eaf23152bd5a155f96a85b7e5a64e3f6952`) dan vault bx (`0x8551f451a5e7dc39d82ed08195eeda16abfe60a1`) tidak ada di bundle. Implementasi live yx cocok dengan bundle. **Perlu konteks tim via ticket** sebelum kesimpulan publik apa pun tentang bx.
5. **Ketiga aksi dapat dipisahkan dari kombinasi event per tx (reconstruction):** shielding 272 tx, shielded transfer 188 tx, unshielding 41 tx (dari 511 tx vault yx). **Unshielding sepenuhnya publik** — 41 payout, jumlah `PartialWithdrawal` dan `PaidOut` cocok persis (0 mismatch), total ≈ 752,58 token dalam pembacaan 18 desimal, 33 recipient berbeda, 9 token berbeda. **Shielded transfer tidak menunjukkan siapa/berapa/token apa** — hanya hash `Commitment`/`Nullifier` dan ciphertext `EncryptedNote` 1.312 byte.
6. **Docs tidak berubah sejak 11–12 Nov.** Ketegangan wording soal scoped keys masih ada: blog mengklaim scoped viewing keys adalah model Enygma; doc Private Network menulis "There are no scoped view keys" dan "Audit access is network-wide"; doc Public menulis scope per deployment/negara. **Belum terselesaikan — perlu konteks tim via ticket.**
7. **Di GitHub, escrow auditor ternyata terimplementasi — tetapi di `enygma_retail_payments`, bukan di `enygma_payments`.** File `auditor.go` dan `UserRegistry.sol` (`mlKemAuditCt`/`aesAuditCt`) membuktikan ada kode escrow kunci auditor. Ini konteks baru yang penting, tetapi **bukan** bukti bahwa auditing selektif berjalan/terverifikasi pada deployment testnet yang live (tidak ada event audit/dekripsi on-chain yang ditemukan). Juga baru: binding ciphertext untuk DvP (`CiphertextHash.sol`, commit `6a6a23b1cffde9b4e3a37e27375ddff9ed397578`, 16 Nov). Tidak ada file `SharedVault` di repo; repo tidak memuat alamat testnet / chain ID 7295799 (konfigurasi default Hardhat 1337).
8. **Volume shielded tidak dapat diukur secara utuh.** Yang terukur pasti: jumlah registrasi, jumlah dan nominal unshielding, jumlah tx per tipe (reconstruction). Yang tidak terukur: nominal dan pihak dalam shielded transfer, serta total volume shielded. Double counting harus dihindari: `PartialWithdrawal` + `PaidOut` adalah satu peristiwa ekonomi yang sama; `Commitment` muncul di shielding maupun transfer.
9. **Selisih fee 0,0001 RLS masih UNRESOLVED** — jangan pernah menyebutnya rounding. Angka proof-time berbeda-beda menurut sumber (408 ms vs ~2,2 dtk vs ~3 dtk vs "under 4 s") — belum diuji.

---

## A. Ringkasan kondisi workspace dan materi yang tersedia

### A.1 Workspace

- Workspace: `/home/hatch/workspace` — 37 repo git (angka ini dari brief penugasan yang sudah diverifikasi Anara; audit ini tidak menghitung ulang).
- Folder penelitian Enygma sebelumnya: `/home/hatch/workspace/rayls-enygma-research` — **folder biasa, BUKAN repo git lokal** (verified fact — diperiksa langsung 21 Nov 2026; tidak ada direktori `.git` di dalamnya). Isinya (20 file):
  - `README.md`
  - `ama/ama-notes.md`
  - `audit/audit-status.md`
  - `demo-testing/screenshots/1-fee-register.png`, `2-fee-shield.png`, `3-confirm-onchain.png`, `4-wallet-akhir.png`, `5-send-48-user.png`, `demo-testing/test-report.md`, `demo-testing/user-flow.md`
  - `findings/observations.md`, `findings/official-claims.md`, `findings/unknowns.md`, `findings/verified-facts.md`
  - `research/open-questions.md`, `research/research-plan.md`, `research/technical-overview.md`
  - `sources/source-register.md`
  - `technical-evidence/technical-evidence.md`
- Repo GitHub cerminan riset sebelumnya: `github.com/akira01111/rayls-enygma-research` (public sejak 16 Nov 2026, head `ab523db`, 4 commits — dari brief; tidak di-clone ulang dalam audit ini karena folder lokal sudah diperiksa).
- Repo referensi standar kualitas: `/home/hatch/workspace/rayls-mainnet-block-research-check` — repo git lokal (2 commits: `4ef462f` "Add audited historical block comparisons", `a514353` "Add reproducible Rayls mainnet block analysis"). Strukturnya dipelajari sebagai pola dokumentasi: README (research question, network, tabel hasil, method, perintah reproduce, interpretasi + batasan, referensi resmi, snapshot source dengan commit hash), CSV dataset + raw JSON + metadata JSON per window (chain_id, rpc, metode sampling, start/end block, total, elapsed, observed_tps, retrieved_at_utc), script verifikasi (`verify_dataset.py`, `reproduce_fixed_600.py`), perbandingan multi-window di `windows/`, `audit_report.json`. Standar ini dipakai sebagai acuan bagian H.

### A.2 Materi dan kesimpulan sebelumnya yang menjadi titik awal

- Artikel Enygma sebelumnya: "Can Rayls Enygma Make Private Payments Auditable?" (X, 16 Nov 2026, `status/2122127310585524690`). Salah satu kesimpulan utamanya — selective auditing pada deployment Enygma Public yang diuji **belum dapat diverifikasi secara independen** — **TETAP BERLAKU** kecuali ada bukti baru. Audit ini tidak menemukan bukti baru yang mengubah kesimpulan itu (lihat B.4 dan D.5).
- Artikel mainnet sebelumnya: "How Fast Is Rayls in Practice? I Audited 2,400 Mainnet Blocks" — skor **90/100**, **9/10 Rayls Points**, Approved, bonus +3 Discord points. Dijadikan standar kualitas dokumentasi: pengumpulan data on-chain independen, pemeriksaan kuantitatif reproducible, analisis source code, raw RPC responses, CSV datasets, metadata + checksums, audit scripts, penjelasan batasan. Feedback reviewer untuk riset selanjutnya yang diterapkan di sini: (1) perluas pengamatan ke lebih banyak tanggal/waktu atau monitoring kontinu; (2) eksperimen finality terpisah jika memungkinkan; (3) pertimbangkan controlled load test di lingkungan yang sesuai; (4) catat versi client dan block identifiers setiap pengumpulan data.
- Arahan moderator Rayls: pendekatan hands-on testnet disukai; artikel lama tidak perlu dihapus; konten pengujian langsung diharapkan terus dibuat; jika temuan utama belum dapat diverifikasi, **buka ticket dulu** agar tim memberi konteks (mod tidak keberatan menerima ticket walau balasannya butuh waktu); mod secara eksplisit **menyetujui** pembuatan konten Enygma Testnet berikutnya untuk Weekly Quest.
- Arahan resmi komunitas Rayls: konten harus membantu komunitas memahami apa yang dibangun, siapa penggunanya, mengapa penting, bagaimana produk/ekosistem bekerja. Hindari konten yang hanya menyoroti kekurangan data publik atau kesimpulan negatif tanpa konteks. Aktivitas Enygma Sovereign di jaringan privat institusi **tidak otomatis terlihat** lewat public explorer — jangan perlakukan ketiadaan data publik sebagai bukti. Tetap kritis tapi konstruktif; jangan FUD/ragebait/klaim tanpa bukti.
- Nama calon repo baru `rayls-enygma-public-testnet-research` masih **USULAN — belum disetujui** untuk dibuat/dipublikasikan. **Repo baru tidak dibuat dalam audit ini.** Bagian H hanya rekomendasi struktur.
- Baseline 15 Nov 2026 yang dipakai sebagai pembanding (dari riset sebelumnya): registry yx 143 log / 76 tx (63 registrasi, log terakhir 13 Nov 22:05:57 UTC); vault yx 803 log / 204 tx (log terakhir 15 Nov 14:41:04 UTC); registry bx 4 log; vault bx 10 log. Event saat itu: Commitment 334, EncryptedNote 321, Nullifier 107, PartialWithdrawal 13, PaidOut 13, AuditorAdded 7, AuditorKeyGiven 4, AuditorPersonalKeySet 1, Upgraded 7. Bundle 15 Nov: page SHA `b615fd73aa999fb72529d37553ba0943d754e2f2e0f50468a07fe2e8fcb636c5` (3.645 byte); bundle `index-BmNruHc0.js` SHA `c878b635cab69d9c529f4cd9e6fcd8fb606c0e2a9a3bd42af39ea435f065ec81` (1.338.924 byte); deployment yx ditandai retired 2026-11-10.

### A.3 Metode audit ini

- **GitHub:** pemeriksaan repo `raylsnetwork/Enygma` (head, commit, file sumber, ABI/konfigurasi) oleh satu agen investigasi; hasilnya dirangkum di bagian B.
- **On-chain + bundle + docs:** pemeriksaan read-only via `curl` (RPC `https://testnet-rpc.rayls.com`, API explorer `https://testnet-explorer.rayls.com`, halaman dan bundle `https://enygma-testnet.rayls.com/`) oleh satu agen investigasi; hasilnya dirangkum di bagian C–F. Waktu pemeriksaan ~04:50–05:00 UTC, 21 Nov 2026.
- **Keterbatasan metode yang dicatat:** API explorer membatasi **maks. 1.000 hasil per panggilan** — panggilan naif `fromBlock=0&toBlock=latest` untuk vault yx mengembalikan tepat 1.000 log (terpotong); total penuh diperoleh dengan paginasi per rentang 200.000 blok. Satu kali HTTP 403 dari urllib tanpa User-Agent (teratasi dengan curl + User-Agent browser). Dua pemanggilan `exec` dalam investigasi on-chain mengembalikan exit code 1 (nonzero) — tidak ada data yang hilang dari laporan karena semua angka di atas diperoleh dari panggilan yang berhasil; kegagalan itu dicatat di sini sebagai batasan alat, bukan sebagai temuan.
- **Yang tidak dilakukan:** tidak ada eksperimen di testnet, tidak ada penulisan artikel, tidak ada pembuatan repo, tidak ada transaksi, tidak ada koneksi akun.

---

## B. Repository GitHub dan source code relevan

### B.1 Repo utama: `raylsnetwork/Enygma`

- **Head saat diperiksa:** `0b1945ae6c827745d1ad48eddcec39df4b20277a` (19 Nov 2026, 22:48 UTC) — verified fact (commit hash dari pemeriksaan GitHub).
- **Posisi relatif terhadap baseline riset sebelumnya:** 71 commit di depan `3c61be782cbd31b108eacbda662d3a0a9219f6ae` — verified fact.
- **Cabang:** 183 branch; organisasi Rayls memiliki 25 repo publik — direct observation.
- **`protocol_description.md` tidak berubah byte-for-byte** sejak baseline: blob `61b9447217a881dd3e47f7ade3fcc8d5e4df9a0f`, 37.302 byte — verified fact. Artinya deskripsi protokol di repo tidak merevisi klaim apa pun sejak artikel sebelumnya.

### B.2 Yang terimplementasi di kode vs yang hanya didokumentasikan

| Fitur | Status | Bukti |
|---|---|---|
| Escrow kunci auditor (ML-KEM + AES view-key) | **Terimplementasi — di `enygma_retail_payments`** | `auditor.go`; `UserRegistry.sol` (`mlKemAuditCt` / `aesAuditCt`) — verified fact (file dan identifier diperiksa di repo) |
| "Tidak ada peran auditor" | **Hanya berlaku untuk `enygma_payments`** | Klaim "no auditor role" ternyata berskop modul itu saja, bukan seluruh Enygma — koreksi penting terhadap pembacaan sebelumnya |
| Binding ciphertext untuk DvP | **Terimplementasi (baru)** | `CiphertextHash.sol` + test + perubahan salt, commit `6a6a23b1cffde9b4e3a37e27375ddff9ed397578`, 16 Nov 2026 — verified fact |
| `SharedVault` | **Tidak ada file bernama itu di repo** | Tidak ditemukan file `SharedVault` — direct observation; kontrak vault yang live di testnet tidak dapat dicocokkan ke file repo ini |
| Alamat testnet / chain ID 7295799 | **Tidak ada di repo** | Konfigurasi default Hardhat 1337; tidak ada deployment config testnet — direct observation |
| `enygma_demo` | Tidak berubah sejak 29 Okt 2026 | direct observation |
| `address.json` berisi `0xd908BaeE382191D15E479589D9661A9E9b55b827` | **Provenance unknown** | Alamat ini ditemukan di repo tetapi asal/tujuannya tidak diketahui — unknown; jangan dipakai sebagai alamat deployment tanpa verifikasi |

**Koreksi terhadap inferensi yang salah:** chain ID testnet **7.295.799 bukan typo dari 72.957** (mainnet). Chain ID 7.295.799 terverifikasi langsung dari RPC (`eth_chainId` → `0x6f5337`); repo hanya tidak memuat konfigurasi deployment testnet. Jangan menulis bahwa keduanya tertukar.

### B.3 Repo `akira01111` terkait

- `github.com/akira01111/rayls-enygma-research` (public, head `ab523db`, 4 commits) — repo riset sebelumnya; salinan lokalnya diperiksa di A.1. Tidak ada perubahan yang dibuat padanya dalam audit ini.

### B.4 Apa yang kode GitHub buktikan dan tidak buktikan

- **Yang dibuktikan:** ada kode escrow kunci auditor di modul retail payments; ada binding ciphertext DvP yang baru; deskripsi protokol tidak berubah.
- **Yang TIDAK dibuktikan:** bahwa auditing selektif benar-benar berjalan atau dapat diverifikasi pada deployment testnet yang live. Tidak ada event on-chain yang menunjukkan dekripsi/audit oleh auditor (lihat D.5), dan kontrak vault live tidak tercocokkan ke file repo. Maka kesimpulan artikel sebelumnya tetap berlaku — **inference yang didukung bukti negatif yang konsisten, bukan fakta positif**.
- **Implikasi untuk artikel:** kode escrow adalah konteks baru yang layak dijelaskan (menunjukkan mekanisme auditing memang dirancang dan diimplementasikan di salah satu modul), tetapi artikel harus tetap membedakan "kode ada" dari "auditing live terverifikasi".

---

## C. Arsitektur dan konfigurasi Enygma Public Testnet

### C.1 Konfigurasi jaringan — diverifikasi ulang terhadap deployment aktif

| Item | Nilai | Status |
|---|---|---|
| Chain ID | **7.295.799** (`eth_chainId` → `0x6f5337`) | verified fact — sama dengan baseline; **bukan** 72.957 (itu mainnet) |
| RPC | `https://testnet-rpc.rayls.com` | verified fact — hidup, tidak ada RPC yang gagal saat dicek |
| Explorer | `https://testnet-explorer.rayls.com` | verified fact — API logs dipakai untuk seluruh hitungan bagian D |
| Demo | `https://enygma-testnet.rayls.com/` | verified fact — halaman + bundle diunduh dan di-hash |
| Blok terakhir saat dicek | **24.793.989**, timestamp **2026-11-21 04:50:45 UTC** | direct observation (`eth_blockNumber` → `0x17a5385`) |
| Pertumbuhan sejak baseline | +847.658 blok dari 23.946.331 (15 Nov 14:40 UTC) | reconstruction (selisih dua pembacaan) |
| RLS token (Ethereum mainnet, BUKAN testnet) | `0xb5f7b021a78f470d31d762c1dda05ea549904fbd` | verified fact (dari riset sebelumnya; tidak diverifikasi ulang di sini) |

### C.2 Peta kontrak (testnet 7295799) — semua alamat lengkap, ukuran bytecode dari `eth_getCode`

**Deployment yx (aktif):**

| Kontrak | Alamat | Bytecode (byte) |
|---|---|---|
| RLS token (proxy) | `0x07e17E17e17E17e17e17e17E17E17E17E17e17EA` | 122 |
| RlsGasForwarder | `0x753cc3Abe9A1c49536ee74F1f424fCF693AAB5DD` | 4.394 |
| UserRegistry proxy | `0xA473291FFb33e2276F364fAE169f03c4406719e9` | 170 |
| SharedVaultProxy | `0x9C5Ad5e5Ea5b5910E7fD1E1CC7b70ce0e4bF06c2` | 170 |
| UsdrVault | `0x1edb224cf8637f92efadaf47ef9e70c044d75584` | 20.224 |
| RlsVault | `0x97b5d78dbe06d8c8c843f87b5aa2d8587b890795` | 20.224 |
| Verifier | `0xfa3a53ec650bfd4ca3e8461abce243382a1037af` | 4.652 |
| GenericGroth16Verifier | `0xc12f06f883b757c91069f9d94065a4c673ef356a` | 2.916 |
| Poseidon T3 | `0xc29f02220d8aed5c731de4aee9d7d8d24c94ef15` | 9.743 |
| Poseidon T5 | `0x078c99bbbbf9dcf827ff085c9a4634213b18018b` | 16.276 |
| Poseidon Wrapper | `0x0bc72bf5dd894164f7cc8f8b92c78eb7d2156f3f` | 687 |
| OwnerMultisig | `0xBf099175a241194C38E977735D59CCb22596d775` | 4.373 |
| UserRegistryRetired | `0xD1d92f1B183B84Ea528211302B1eCB881EeF2770` | (tidak diukur; flag `retired: "2026-11-10"` tidak berubah) |

**Deployment bx (tidak aktif sejak 3 Nov — lihat D.2):**

| Kontrak | Alamat | Bytecode (byte) |
|---|---|---|
| RlsGasForwarder | `0x2ef592329B8e01320170f8f8d759d9bcA94d1066` | 4.394 |
| UserRegistry proxy | `0x3E9435c1fe8432e21E80D7A8ab81EBfc8eC708E3` | 170 |
| UserRegistryImplementation (di bundle) | `0xB23124D2eE339d1E8175B9ec10D20217CE015c1C` | 14.492 |
| SharedVaultProxy | `0x94dafa3bf372cad68143ac535f845e74751d75ef` | 170 |
| TokenFactory | `0x7416094FFC5A1D0C2659DA0D5b81CeCc18f1BdAc` | 7.274 |

**Kontrak lain:**

| Kontrak | Alamat | Keterangan |
|---|---|---|
| Auditor | `0x71AF09966CBED4434ccA97c40Fa38B8083548B95` | 0 byte code = EOA (verified fact) |
| Relayer (alamat pengirim semua tx vault/registry) | `0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8` | Username terdaftar `rayls-relayer` (lihat D.4) |
| Multicall3 | `0xca11bde05977b3631167028862be2a173976ca11` | Dipakai relayer untuk pengiriman shielded payment |
| Forwarder "next" (yx) | `0x12B6640048DEB2e8fFDa4Bc10Bb2a640B70eCA6d` | Tercantum di bundle (blok 23395717); sudah dipakai registrasi terbaru (lihat D.4) |
| EnygmaDvp | `0x7ec57a8f97b636a4b54633df826b2a4311018996` | Muncul di bundle baru; baseline tidak mencatatnya — unknown apakah baru atau hanya tidak tercatat dulu |

**Jebakan yang sudah diketahui — ditegaskan kembali:** `0x753cc3Abe9A1c49536ee74F1f424fCF693AAB5DD` adalah **RlsGasForwarder, BUKAN token RLS**. Token RLS testnet adalah `0x07e17E17e17E17e17e17e17E17E17E17E17e17EA` (proxy, 122 byte).

### C.3 Slot implementasi EIP-1967 — temuan utama

Slot `0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc` dibaca via `eth_getStorageAt`:

| Proxy | Implementasi live | Cocok dengan bundle? |
|---|---|---|
| Registry yx | `0x9686a3d5a9Fd2101d15888c6a09a64faFA7EE349` | **Ya** — sama dengan `UserRegistryImplementation` di bundle (upgrade sudah dieksekusi) |
| Vault yx | `0xAd9667049f14D1757D147F652c41Dc241C57091C` | **Ya** — sama dengan `SharedVaultImplementation` di bundle |
| Registry bx | `0x66f87eaf23152bd5a155f96a85b7e5a64e3f6952` (14.440 byte) | **TIDAK** — bundle mencantumkan `0xB23124D2eE339d1E8175B9ec10D20217CE015c1C` (14.492 byte); alamat live ini **tidak muncul sama sekali** di bundle saat ini |
| Vault bx | `0x8551f451a5e7dc39d82ed08195eeda16abfe60a1` (23.641 byte) | **TIDAK** — bundle mencantumkan `0xe023791669A54EC41Ef1affA2c1B44460C1943CD` |

- Beacon slot EIP-1967 (`0xa3f0ad74…`) = 0 untuk ketiga proxy yang dicek → bukan beacon proxy (direct observation).
- **Bukti upgrade (event `Upgraded`):** registry yx naik ke `0x9686a3d5a9Fd2101d15888c6a09a64faFA7EE349` di blok 23.400.006, 11 Nov 21:25:18 UTC, tx `0x908fdae3efbee9b058da2088eaf73f7f0031257df79953974fb87b1c5ac96fe8`; vault yx naik ke `0xAd9667049f14D1757D147F652c41Dc241C57091C` di blok 23.399.976, 11 Nov 21:25:01 UTC, tx `0xc841126f7cf05d937967743f7db5cb80d04cf32ed1dca929aac23d952e97f3c4`. Registry/vault bx **hanya punya 1 log `Upgraded` masing-masing, dari deployment 3 Nov** (ke `0x66f87eaf23152bd5a155f96a85b7e5a64e3f6952` / `0x8551f451a5e7dc39d82ed08195eeda16abfe60a1`) — upgrade `ownerCalls` di bundle untuk bx (blok ~23.395.9xx) **tidak pernah dieksekusi** di proxy.
- **Inference:** entri `Implementation` + `next` + `ownerCalls` di bundle adalah rencana/pending upgrade; untuk yx sudah live, untuk bx belum. **Perlu konteks tim via ticket** — jangan simpulkan di publik bahwa bx "rusak" atau "ditinggalkan"; yang terbukti hanya ketidaksesuaian antara bundle dan state live.
- **Anomali lain (unknown):** slot implementasi token RLS berisi alamatnya sendiri (`0x07e17e17e17E17e17e17e17E17E17E17E17e17EA`) — bukan pola proxy EIP-1967 biasa; artinya **unknown**, tidak diverifikasi lebih jauh.

### C.4 Bundle demo — build baru, konfigurasi sama

- Halaman `https://enygma-testnet.rayls.com/`: **3.872 byte, SHA-256 `d709dc0639a80d71b127681fbd56ae7f6f9a9f83c38bf4b7f42239b4b961a28e`** (baseline 3.645 byte / `b615fd73aa999fb72529d37553ba0943d754e2f2e0f50468a07fe2e8fcb636c5`) — **berubah** (verified fact).
- Bundle utama kini **`assets/index-Dlv-HYaZ.js`, 1.422.052 byte, SHA-256 `7530bbc2d7a301c50e28923529cb9315f88145a9a25a7c71db8a1f34afd9ca68`** (baseline `index-BmNruHc0.js`, 1.338.924 byte / `c878b635cab69d9c529f4cd9e6fcd8fb606c0e2a9a3bd42af39ea435f065ec81`) — **build baru** (verified fact). Build kini terpecah jadi banyak chunk (`rolldown-runtime-DLMaRju-.js`, `utils-62W0Csdc.js`, `sha3-Dlq0T7vU.js`, dst.) — sebelumnya satu bundle.
- Konfigurasi deployment di dalam bundle (di-bundle saat build, bukan di-fetch runtime — `GET /contracts/deployments/7295799.json` dan `/br/7295799.json` mengembalikan **HTTP 404 "Not found"**): masih **3 file: `7295799.json`, `br/7295799.json`, `11155111.json` (Sepolia)** — **tidak ada deployment baru** (verified fact).
- Semua alamat kontrak baseline masih ada di bundle dan **tidak berubah** (verified fact).
- Auditor di bundle: `0x71AF09966CBED4434ccA97c40Fa38B8083548B95` (8 kemunculan) — tidak berubah. `auditorPublicKeyHash` registry yx: `0x4151c50e9250f5818a53f9e48e734bd4209407d19f966ede4f7988dd4af863e5` — sama seperti baseline.
- Relayer URL di bundle: `7295799=https://enygma-relayer-aafjr.ondigitalocean.app/rayls`, `11155111=https://enygma-relayer-aafjr.ondigitalocean.app/sepolia` (baseline tidak mencatat nilai ini — tidak bisa dibandingkan).
- Detail yx lain yang terverifikasi dari bundle: `UserRegistryImplementation` `0x9686a3d5a9Fd2101d15888c6a09a64faFA7EE349` (tx `0xe029bde6…` — hash tercatat terpotong di catatan pemeriksaan, full hash **unknown** — blok 23395761), `SharedVaultImplementation` `0xAd9667049f14D1757D147F652c41Dc241C57091C` (blok 23395769).

### C.5 Mekanisme shielding / unshielding / shielded transfer (dari docs + log)

**Official claim (docs `how-enygma-public-works`, `rayls-high-level-architecture`):**
- "Shielding and unshielding are public: the chain shows the address, the token and the amount moving in or out."
- "A send between shielded balances shows only that a send happened, the relayer that submitted it and its gas fee."
- "In the shared vault, a payment doesn't show which token it moved."
- Groth16 membutuhkan trusted setup; "The testnet's proving and verifying keys come from a single-party setup, which is suitable for testing only."
- Biaya relayer 15% ke Rayls Foundation; unshield/shield USDr +0,25%.
- Pilot blog (12 Nov): kriptografi AES-256-GCM + ML-KEM + HKDF untuk Public pilot; shield/unshield bersifat publik; ada invite-flow; usage policy (semua fee dalam $RLS); roadmap (WalletConnect custody, shielded swaps, DvP, sealed-bid auctions); faucet 1×/jam.

**Yang terverifikasi dari log (bagian D):** unshielding memang publik penuh (alamat, token, jumlah di log); shielded transfer memang tidak menunjukkan pihak/jumlah/token; registrasi memang publik (alamat + username). **Yang belum diverifikasi dari log dalam audit ini:** sisi transfer token ERC-20 pada shielding (apakah jumlah shielding terlihat lewat log token) — klaim docs soal itu dicatat sebagai official claim, bukan verified fact.

**Angka proof-time berbeda menurut sumber (official claim, saling tidak konsisten — belum diuji):** 408 ms (rayls.com) vs ~2,2 dtk (AMA) vs ~3 dtk (pilot blog) vs "under 4 s". Jangan kutip satu angka sebagai fakta tanpa pengujian sendiri.

### C.6 Docs — tanggal dan wording (verified fact)

| Halaman | Updated | Wording kunci (verbatim) |
|---|---|---|
| `docs.rayls.com/docs/enygma-privacy-and-auditing` | 2026-11-11T15:26:41.000Z | **Tidak berubah:** "Audit access is network-wide" dan "There are no scoped view keys" masih tertulis verbatim. Catatan: halaman ini membahas model **Private Network (Besu Hub)**, bukan Public testnet. |
| `docs.rayls.com/docs/enygma-public` | 2026-11-11T21:36:24.000Z | Model Public: "An auditor for every deployment… A deployment can be set up per country, so that each auditor reads only its own country's activity." |
| `docs.rayls.com/docs/enygma-public-who-sees-what` | 2026-11-11T21:36:27.000Z | "One auditor per deployment. An auditor reads only its own deployment, for example its own country's." + "The auditor… Every shielded transaction, decrypted: who paid whom, the amount and the token" + "It can't freeze… Nobody can ask to be an auditor. An existing auditor adds new ones." |
| `docs.rayls.com/docs/how-enygma-public-works` | 2026-11-11T15:27:18.000Z | "In the shared vault, a payment doesn't show which token it moved." + Groth16 single-party setup, testing only. |
| `docs.rayls.com/docs/rayls-high-level-architecture` | 2026-11-11T21:37:02.000Z | Shielding/unshielding publik (alamat, token, jumlah); shielded send hanya menunjukkan bahwa pengiriman terjadi, relayer, dan gas fee; fee relayer 15% ke Rayls Foundation; unshield/shield USDr +0,25%. |
| Blog `rayls.com/blog/auditability-without-surveillance-…` | Published 2026-09-12, Updated 2026-11-12 | Mengklaim scoped viewing keys **adalah** model Enygma ("keys that can be scoped to particular subsets of data… mathematically enforced") — **bertentangan secara wording** dengan doc Private Network ("There are no scoped view keys"). |
| Blog "controlled visibility" | Updated 15 Nov 2026 | Mengulangi klaim scoped-auditor — lebih baru daripada halaman docs (11 Nov). |

**Konflik scope auditor-access BELUM TERSELESAIKAN (official claims yang saling tegang):** blog = model Enygma umum/Sovereign (scoped keys); doc privacy-and-auditing = operator Private Network melihat network-wide; doc Public = scope per deployment/negara. Ketiganya tidak berubah sejak baseline (semua updated 11–12 Nov, kecuali blog "controlled visibility" 15 Nov). Laporan ini menyajikan ketiga sisi tanpa memutuskan. **Perlu konteks tim via ticket.**

**Sumber baru (belum ada di riset sebelumnya):** makalah IACR ePrint **2025/1638** (Rayls II) dan **2025/1639** (Rayls) — official claim (publikasi kriptografi Rayls); isinya belum ditelaah dalam audit ini, dicatat sebagai bahan bacaan lanjutan.

---

## D. Aktivitas on-chain yang dapat diamati

Semua angka di bagian ini adalah **direct observation** dari API log explorer (`https://testnet-explorer.rayls.com/api?module=logs&action=getLogs`), dipaginasi per rentang 200.000 blok karena cap 1.000 hasil per panggilan. Waktu pemeriksaan ~04:50–05:00 UTC, 21 Nov 2026. Blok acuan saat itu: 24.793.989.

### D.1 Registry yx — `0xA473291FFb33e2276F364fAE169f03c4406719e9`

- **405 log / 207 tx unik** (baseline 143 / 76 → **+262 log / +131 tx**). Blok 23.212.003–24.766.266.
- Log pertama 10 Nov 13:57:50 UTC; **log terakhir 21 Nov 00:39:06 UTC**, tx `0x0c7419d5d3d334dae29f5e87bdde78481ed61b6ae2907429044b4e56903beb0a` (username `rq3faucet26`).
- **Registry yx masih aktif setelah 13 Nov 22:05 UTC — ya, sangat aktif.**
- Per event: UserRegistered 194, UsernameSet 194, AuditorAdded 7, AuditorKeyGiven 4, Upgraded 2, Initialized 1, ImportClosed 1, OwnershipTransferred 1, AuditorPersonalKeySet 1.
- Baru sejak 15 Nov 14:41:04 UTC: **262 log / 131 tx — semuanya UserRegistered (131) + UsernameSet (131)**. Tidak ada event auditor baru.

### D.2 Registry bx — `0x3E9435c1fe8432e21E80D7A8ab81EBfc8eC708E3`

- **4 log / 3 tx, TIDAK BERUBAH** dari baseline. Blok 22.210.868–22.211.254, 3 Nov 12:32:40–12:36:33 UTC. Upgraded 1, Initialized 1, ImportClosed 1, OwnershipTransferred 1.

### D.3 SharedVault yx — `0x9C5Ad5e5Ea5b5910E7fD1E1CC7b70ce0e4bF06c2`

- **2.128 log / 511 tx unik** (baseline 803 / 204 → **+1.325 log / +307 tx**). Blok 21.568.375–24.784.630.
- Log pertama 30 Okt 00:04:35 UTC; **log terakhir 21 Nov 03:25:55 UTC**, tx `0x7f72b00105ab01cb600461487dad6ff7932bdb302c6a85d00a01b67df3117dd1` (`PaidOut`).
- **Vault yx masih aktif setelah 15 Nov 14:41 UTC — ya.**
- Per event: Commitment 888, EncryptedNote 847, Nullifier 296, PartialWithdrawal 41, PaidOut 41, RoleGranted 5, CoinLocked 5, Upgraded 3, Initialized 2.
- Baru sejak 15 Nov 14:41:04 UTC: **1.325 log / 307 tx** — Commitment 554, EncryptedNote 526, Nullifier 189, PartialWithdrawal 28, PaidOut 28.

### D.4 SharedVault bx — `0x94dafa3bf372cad68143ac535f845e74751d75ef`

- **10 log / 6 tx, TIDAK BERUBAH** dari baseline. Blok 22.211.086–22.211.236, 3 Nov 12:34:50–12:36:23 UTC. RoleGranted 6, RoleRevoked 2, Upgraded 1, Initialized 1.

### D.5 Auditor — tidak ada yang baru (verified fact)

`AuditorAdded` tetap **7**, semua 10 Nov 2026, semua oleh `0x08fbf5b9c2faeb669b9cbdcfe685ff9afc444dae` (3 pertama) atau auditor `0x71af09966cbed4434cca97c40fa38b8083548b95` (4 terakhir):

| # | Alamat auditor | Blok | Waktu (UTC) | Tx hash |
|---|---|---|---|---|
| 1 | `0x71af09966cbed4434cca97c40fa38b8083548b95` | 23212015 | 10 Nov 13:57:57 | `0xf1b398d51a3d5f507c1fa13016361b499fefabd37e0777697e82bc60a4ca53dd` |
| 2 | `0x3bffb10f6f17f15164fbc0416f1bc42c56b2c191` | 23212021 | 10 Nov 13:58:00 | `0x0ef89d3739e3a24a15daf14377fc46bfea48d36e48a86213603d027e3d4d635e` |
| 3 | `0xd04004a3715f8428674a01ffde2069c181d4b0fd` | 23212029 | 10 Nov 13:58:05 | `0xe2d442f5550172fa1b4235b7e6f84afeaaa951ffceea55a053feed942b23c428` |
| 4 | `0x23c5a5138ad66ff376a7a20248ec47a64d7b3fc9` | 23222870 | 10 Nov 15:48:10 | `0xc6261618d2cc6dd250f9b30504f27a16a0378e16b2a4e927f13a933e2eca1aef` |
| 5 | `0x67359d4ed15116fc5d15c96d0f0b049bae34688f` | 23225307 | 10 Nov 16:12:56 | `0x61874cfb2277bd640ae20e8ed08bafb68449c08f6484a7377c3ca3f16a9833d6` |
| 6 | `0x7dd26477c7f86a1d4cdfaeb73741577def7905ef` | 23225360 | 10 Nov 16:13:28 | `0xa90caaf3cdc40a5c5f0b6a52bdf2a4fc8887a62d7418a0b0c62d8ae222480073` |
| 7 | `0xf52b7eba863ee3378cc9dd60efd62df1bb08f567` | 23225410 | 10 Nov 16:13:58 | `0x8075169c584b0b616874fa91513f017fd45fe7eae30e5a1568825a803c6f6dc9` |

- `AuditorKeyGiven` tetap **4** (3 pertama di atas + `0x23c5a5138ad66ff376a7a20248ec47a64d7b3fc9`, blok 23224952, 10 Nov 16:09:19 UTC, tx `0x6d7df5de9919f9d52b1b7f9dd100141c8def1063a1df25f1bad7409548a1690c`).
- `AuditorPersonalKeySet` tetap **1**: `0x23c5a5138ad66ff376a7a20248ec47a64d7b3fc9`, blok 23223818, 10 Nov 15:57:51 UTC, tx `0x787bbe3cd3369aa325fdfbebf8b41e7554270c8867ca82505acd5f1e0edaf9a5`.
- **Jadi: 7 auditor terdaftar, hanya 4 yang punya `AuditorKeyGiven` — sama seperti baseline, tidak ada penambahan.** Jangan pernah menulis "7 auditor menerima kunci" — itu salah; yang benar 7 terdaftar, 4 berkunci.
- **Tidak ada event on-chain yang menunjukkan dekripsi/audit oleh auditor** (tidak ada event audit di log vault/registry). Ini konsisten dengan kesimpulan artikel sebelumnya yang tetap berlaku (A.2).

### D.6 Username baru — 131 sejak 15 Nov (verified fact)

Total **194 username, semua unik, 1:1 dengan 194 alamat terdaftar**. Username pertama tetap `rayls-relayer` (`0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8`, 10 Nov 13:58 UTC). Daftar 131 username baru (urutan kronologis, 16–21 Nov):

deepsync, testing, api_1, api_2, notyourbunnyy, testingg, 9ytshade, qa-test, aashy, monarch321, momonen, lotosbi, jil, wallet_101, fujiyama, andro, freeboy_dev, compi, richar, yuno, zolas, rayls_guest_2026, solcops-test, alanxft, vol, eddi, pavel, tomas, romunas, mantas, kristof, max, oleg, stasis, heismellow, vasiliy, sergey, yuriy, gerda, polina, qa-fb7k3a, qa-fb7k3b, metalawyerdemo, qa-dn7k2, qa-leo-dn7k, permit_after_e2e, permit_before_e2e, tenant-a-45x8d8, tenant-b-b2fg4a, tenant_a, tenant_b, tenant_01, tenant_02, testing0890, shakthi, tenant_03, eric, amulu, tenant_04, niceguy, swimfanimfan, lavanya, ralys, nishu, 9874, 0764, subbu, selvam, sathya, 7542, 9078, tenant_g1, tenant_g2, 0xstauf, qual-a-3adeae04, qual-b-3adeae04, mb-piloto-dev, rls-333, yetu891, horizontev-dev, r20-cofre-dev, coinlayer, bosqu99, dino, oshadha44, sooody, windut39, demo22, cahusil65, lazarus, ghostwalker, footprinta, meta, demo111, niloy34, theobullish, jianeth, rizkymahreza, cryptoram89, cryptoram3669, 0xwysi, cryptoram01, ikihin, kobe, tiny91511, tinyb48213, mr_aniqul, hanbongdubong, ted, tupro, maxwellifeanyi, hanbongdubong2, maxoil, blazetorc, railfeetrace1, railfeetrace2, immortal, 798879, bankiakun, fengzheng, tesgin123456789, fengzheng2, swapspeedtest1120, smsms, testing099789, testging9876, falcongr, god, rq3dev26, devil, rq3faucet26.

Pemetaan lengkap alamat + tx hash per nama terverifikasi dari log. Contoh pertama: `deepsync` = `0x98de6a698d5dc11173e82ba71da701645b606db5`, 16 Nov 12:50 UTC, blok 24082221, tx `0x67e579e18c80d6f4690fd51b3b0e3d11a8d00b49244d9725fd18aa9f266168e7`. Terakhir: `rq3faucet26` = `0xe1136dcf839c4ad2704094241928fa2896a118c5`, 21 Nov 00:39 UTC, blok 24766266, tx `0x0c7419d5d3d334dae29f5e87bdde78481ed61b6ae2907429044b4e56903beb0a`.

**Catatan pola (inference, bukan fakta identitas):** banyak nama bertema pengujian/QA (`qa-test`, `qa-fb7k3a`, `permit_after_e2e`, `tenant_*`, `testing*`, `demo*`, `swapspeedtest1120`) — aktivitas ini tampak didominasi pengujian internal/pengembang, bukan pengguna akhir organik. Jangan klaim identitas di balik nama-nama ini tanpa bukti.

### D.7 Klasifikasi tipe transaksi dari kombinasi event (reconstruction)

Ketiga aksi **dapat diidentifikasi secara terpisah** dari kombinasi event per tx (511 tx vault yx). Aturan klasifikasi yang dipakai (eksplisit, dapat direproduksi):

| Tipe | Aturan (event dalam satu tx) | Jumlah tx |
|---|---|---|
| Shielding (masuk) | Hanya `Commitment` + `EncryptedNote`, tanpa `Nullifier`/payout | **272** |
| Shielded transfer (spend tanpa keluar) | `Commitment` + `EncryptedNote` + `Nullifier`, tanpa `PaidOut`/`PartialWithdrawal` | **188** |
| Unshielding (keluar) | `Commitment` + `Nullifier` + `PaidOut` + `PartialWithdrawal` (35 tx; 6 tx tambahan juga membawa `EncryptedNote`, yaitu change note) | **41** |
| CoinLocked saja | Hanya `CoinLocked` (lock nullifier, 30 Okt–3 Nov) | 5 |
| Admin | `RoleGranted`/`Upgraded`/`Initialized` | 3 |
| **Total** | | **511** |

Status label: **reconstruction** — klasifikasi ini dibuat dari pola event, bukan label dari protokol. Aturannya eksplisit sehingga dapat dicek ulang, tetapi interpretasi "shielding" vs "transfer" mengikuti semantik event, bukan konfirmasi dari tim.

### D.8 Unshielding — sepenuhnya publik (verified fact)

- **41 unshielding**, jumlah per tx **cocok persis** antara `PartialWithdrawal` dan `PaidOut` (**0 mismatch**).
- `PartialWithdrawal(vaultId, recipient, amount, changeCommitment)` — amount ada di `data` plaintext; `PaidOut(vaultId, token, recipient, amount)` — token + recipient di topics, amount di `data`.
- Total ≈ **752,58 token** (pembacaan 18 desimal):
  - RLS `0x07e17e17e17E17e17e17e17E17E17E17E17e17EA` — 196,6795808 (14x)
  - USDr `0x0000000000000000000000000000000000000400` — 20,7 (16x)
  - `0x3ab29f9e8ef3a730731eda5e88eaf986ff824b4d` — 10,0 (1x)
  - `0xc66cb3ce397e70888e69d6e7e75474046c6617e4` — 500,0 (1x)
  - `0x076e2256c36196fce6e4cb7537f1edeb27d3a6b3` — 20,0 (1x)
  - `0x68660d8de06045f80c749400abc347081073ff5f` — 5,2 (2x)
  - Dust: `0xf4cf04f4173fbff71a8718517199e57e11b20af0` — 2 wei (2x); `0xe50ab75c55db6a98d6e2d89496e54e4f5a391523` — 500.000 wei (1x); `0xc81b66f670124d345b1a60165192508e31d39150` — 1.500.000 wei (3x)
- Rentang amount 1 wei–500 token. **33 recipient berbeda, 9 token berbeda.** Semua `vaultId = 2` (shared vault).
- **Caveat (penting):** desimal token non-RLS/USDr **unknown**, jadi total gabungan hanya bermakna dalam pembacaan 18 desimal — jangan sajikan "752,58 token" sebagai satu angka volume tanpa caveat ini.

### D.9 Apa yang terlihat dan tidak terlihat dari log (verified fact)

**Terlihat publik:**
- Unshielding: alamat penerima, token, jumlah (D.8).
- Registrasi: alamat + username plaintext (`UsernameSet`), plus `UserRegistered` dengan `data` tetap **5.186 byte** (ciphertext ML-KEM + AES view-key escrow, per ABI bundle) — isinya terenkripsi, tetapi keberadaan + ukuran + alamatnya publik.
- Relayer menyerahkan semua tx: dari 4 tx yang dicek via `eth_getTransactionByHash`, `from` selalu **`0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8`** (username `rayls-relayer`). Contoh: shielded transfer `0xee8b31ad3d0f00437ce36d4058af16f08af5c4103a60c896da34ad0bbf359211` (`to` = vault yx); unshield `0x282db91e109533bfd1e89ddde65021ec36ef38d54b721a64ed368855dbf19110` (`to` = forwarder yx lama); registrasi `0x0c7419d5d3d334dae29f5e87bdde78481ed61b6ae2907429044b4e56903beb0a` (`to` = forwarder **baru** `0x12B6640048DEB2e8fFDa4Bc10Bb2a640B70eCA6d`); vault tx terakhir `0x7f72b00105ab01cb600461487dad6ff7932bdb302c6a85d00a01b67df3117dd1` (`to` = Multicall3 `0xca11bde05977b3631167028862be2a173976ca11`) — konsisten dengan klaim docs bahwa shielded payment dikirim via Multicall3 oleh relayer.

**Tidak terlihat (shielded payment):**
- `Commitment` — `data` kosong (`0x`), hanya hash di topic.
- `Nullifier` — `data` kosong, hanya hash.
- `EncryptedNote` — `data` selalu **1.312 byte** ciphertext (847 log, ukuran identik).
- Tidak ada amount, alamat pengirim/penerima, atau token di log-log ini.

**Unknown dari pemeriksaan ini:**
- Nilai indexed `topics[2]`/`topics[3]` pada `UserRegistered` — explorer API mengembalikan `null` untuk keduanya di semua 194 log (quirk API, bukan data kosong); arti field tersebut tidak bisa dipastikan dari log ini.
- Apakah ada aktivitas shielding yang jumlahnya terlihat lewat log token ERC-20 (tidak diambil dalam tugas ini).

### D.10 Ringkasan perubahan vs baseline 15 Nov (verified fact)

1. **Aktivitas melonjak, bukan mati:** registry yx +131 user baru (total 194), vault yx +307 tx (total 511 tx / 2.128 log). Aktivitas terakhir: registry 21 Nov 00:39 UTC, vault 21 Nov 03:25:55 UTC.
2. **Tidak ada auditor baru** — tetap 7 terdaftar / 4 berkunci, semua dari 10 Nov.
3. **Bundle di-build ulang** (hash + nama file berubah, chunking baru), tetapi **alamat kontrak dan konfigurasi deployment tidak berubah**; `retired: 2026-11-10` tetap.
4. **Docs tidak berubah** sejak 11–12 Nov; ketegangan wording soal scoped keys (blog vs doc Private Network) masih ada.
5. **Temuan baru:** implementasi live proxy **bx tidak cocok dengan bundle** (upgrade bx tidak pernah dieksekusi; bundle menampilkan implementasi "next" yang tidak aktif). Implementasi live yx cocok dengan bundle.
6. **Tidak ada RPC yang gagal**; satu-satunya hambatan adalah cap 1.000 hasil API explorer dan satu HTTP 403 dari urllib tanpa User-Agent (teratasi dengan curl+UA).

---

## E. Kelayakan pengukuran volume transaksi dan token

### E.1 Tiga kategori volume — harus dibedakan secara eksplisit

| Kategori | Definisi | Status untuk testnet ini |
|---|---|---|
| **Observed volume** | Angka yang terbaca langsung dari log (jumlah log/tx, nominal unshielding, jumlah registrasi) | **Terukur pasti** — lihat E.2 |
| **Reconstructed volume** | Angka hasil olahan dengan aturan eksplisit (klasifikasi tipe tx D.7; hitungan per hari) | **Terukur dengan caveat** — aturannya harus dicantumkan; bukan label protokol |
| **Estimated volume** | Perkiraan atas yang tidak teramati (mis. total nilai shielded transfer) | **Tidak dapat dibuat secara bertanggung jawab** — tidak ada basis estimasi dari data publik |
| **Unobservable activity** | Aktivitas yang secara desain tidak terlihat (nominal/pihak/token shielded transfer; aktivitas Sovereign di jaringan privat) | **Tidak terukur dari public explorer** — jangan perlakukan ketiadaannya sebagai bukti |

### E.2 Yang benar-benar dapat diukur

- **Registrasi:** jumlah pasti (194 username / 194 alamat), daftar lengkap, waktu dan blok per registrasi, pemetaan alamat ↔ username (D.1, D.6). Semua ini direct observation.
- **Unshielding:** jumlah tx (41), nominal per tx dan total per token (D.8), recipient (33 berbeda), token (9 berbeda). Jumlah `PartialWithdrawal` vs `PaidOut` cocok persis — verifikasi silang internal yang kuat.
- **Jumlah tx per tipe:** 272 shielding / 188 shielded transfer / 41 unshielding / 5 lock / 3 admin (D.7) — reconstruction dengan aturan eksplisit.
- **Aktivitas per waktu:** jumlah log/tx per hari dapat dihitung dari timestamp blok; pertumbuhan sejak baseline terukur (+131 user, +307 tx vault dalam 6 hari).
- **Pengiriman relayer:** `from` selalu `0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8` pada sampel yang dicek; pola ini dapat diuji pada semua 511 tx (pekerjaan lanjutan, belum dilakukan).
- **Upgrade kontrak:** event `Upgraded` + slot EIP-1967 memberikan riwayat implementasi yang dapat diverifikasi (C.3).

### E.3 Yang tidak dapat diukur

- **Total volume shielded (nominal transfer antar shielded balance):** tidak ada amount di log `Commitment`/`Nullifier`/`EncryptedNote`. Tidak ada cara publik untuk menjumlahkannya.
- **Volume shielding masuk (nominal):** jumlah shielding tidak terlihat dari log vault; sisi transfer token ERC-20-nya belum diambil dalam audit ini (unknown — lihat G.2).
- **Total volume gabungan semua token:** angka "≈752,58 token" hanya bermakna dalam pembacaan 18 desimal dan mencampur token berbeda dengan desimal yang sebagian unknown (D.8). Jangan sajikan sebagai satu angka volume tanpa caveat.
- **Jumlah pengguna aktif yang sebenarnya:** 194 alamat terdaftar ≠ 194 manusia — banyak username tampak seperti akun pengujian/QA (D.6). Jumlah pengguna unik tidak dapat disimpulkan dari jumlah alamat.
- **Nilai ekonomi (USD):** tidak ada harga pasar untuk token testnet; jangan konversi ke USD.

### E.4 Double counting — jebakan yang harus dihindari

1. **`PartialWithdrawal` + `PaidOut` = satu peristiwa.** Keduanya mencatat payout yang sama; menjumlahkan keduanya menggandakan volume unshielding. Hitung satu kali (41 payout, bukan 82).
2. **`Commitment` ≠ pembayaran.** Commitment muncul di shielding (272 tx) maupun transfer (188 tx); total 888 log Commitment bukan 888 pembayaran.
3. **Satu tx dapat menghasilkan banyak log.** Unit hitung yang benar adalah **tx unik per tipe** (D.7), bukan jumlah log mentah (2.128 log vault ≠ 2.128 transaksi; yang benar 511 tx).
4. **Shielding vs transfer vs unshielding adalah tiga peristiwa ekonomi berbeda** — jangan dijumlahkan menjadi "total transaksi Enygma" tanpa menjelaskan komposisinya.
5. **Log `EncryptedNote` 847 vs `Commitment` 888:** selisih 41 = jumlah unshielding (yang tidak membuat note baru, kecuali 6 tx change note). Konsistensi internal ini mendukung aturan klasifikasi D.7 — reconstruction yang koheren, bukan kebetulan.

### E.5 Metode pengumpulan data yang reproducible

Mengikuti standar repo mainnet (A.1) dan feedback reviewer:

1. **Perintah RPC (pola umum):**
   - `curl -s -X POST https://testnet-rpc.rayls.com -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"eth_chainId","params":[]}'`
   - `eth_blockNumber`, `eth_getCode`, `eth_getStorageAt` (slot EIP-1967 `0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`), `eth_getTransactionByHash` — pola yang sama.
2. **Perintah log explorer (paginasi wajib):**
   - `curl -s -A 'Mozilla/5.0' 'https://testnet-explorer.rayls.com/api?module=logs&action=getLogs&address=<addr>&fromBlock=<n>&toBlock=<n>'` — rentang maks. 200.000 blok per panggilan (cap 1.000 hasil). Tanpa User-Agent, urllib sempat kena HTTP 403 sekali; gunakan curl + UA.
3. **Bundle:** unduh halaman + `assets/index-Dlv-HYaZ.js`, catat ukuran byte dan SHA-256 (C.4).
4. **Yang harus dicatat setiap pengumpulan data (feedback reviewer):** versi client yang dipakai (di sini: curl + API explorer, bukan node sendiri), block identifiers (start/end block setiap window), timestamp UTC pengambilan, dan checksum dataset. Repo penelitian nantinya harus menyimpan raw JSON + CSV + metadata JSON + script verifikasi, mengikuti pola repo mainnet (lihat H).
5. **Verifikasi silang yang sudah dilakukan:** `PartialWithdrawal` vs `PaidOut` (0 mismatch); slot EIP-1967 vs bundle; hash bundle vs baseline; hitungan log vs tx unik.

### E.6 Hal yang masih unresolved (jangan diselesaikan dengan asumsi)

- **Selisih fee 0,0001 RLS: UNRESOLVED.** Jangan pernah menyebutnya rounding. Perlu pengujian fee sendiri (G.3) dan/atau konteks tim via ticket.
- **Angka proof-time** (408 ms / ~2,2 dtk / ~3 dtk / "under 4 s") saling berbeda antar sumber resmi — belum diuji (G.4).

---

## F. Keterbatasan data akibat mekanisme privasi

### F.1 Yang bocor ke publik secara desain (inference dari fakta + official claim)

1. **Shielding/unshielding membocorkan alamat + token + jumlah secara publik** — untuk unshielding terbukti dari log vault (D.8); untuk shielding, klaim ini berasal dari docs dan **belum diverifikasi dari log token** dalam audit ini (hanya dari log vault + klaim docs).
2. **Registrasi membocorkan pemetaan alamat ↔ username untuk semua 194 akun** (D.6) — ini data publik penuh, termasuk untuk akun yang tampaknya milik tim/penguji.
3. **Pola aktivitas terlihat:** jumlah shielding vs transfer vs unshielding per hari, dan frekuensi per vault — tetapi **tidak** siapa membayar siapa atau berapa dalam shielded transfer.
4. **Relayer teridentifikasi penuh** (`0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8`, username `rayls-relayer`) — semua tx vault/registry yang dicek dikirim olehnya.

### F.2 Yang tersembunyi secara desain

- Shielded transfer: tidak ada pengirim, penerima, jumlah, atau token di log (D.9). Inilah inti privasi Enygma Public — dan sekaligus batas pengukuran volume (E.3).
- Isi `UserRegistered` (5.186 byte) dan `EncryptedNote` (1.312 byte) adalah ciphertext; ukuran dan keberadaannya publik, isinya tidak.

### F.3 Auditor — yang diklaim vs yang terbukti

- **Official claim (docs `who-sees-what`):** "The auditor… Every shielded transaction, decrypted: who paid whom, the amount and the token." Auditor memegang kunci untuk mendekripsi semuanya — ini by design, bukan kebocoran ke publik.
- **Verified fact:** 7 auditor terdaftar, 4 berkunci, tidak ada perubahan sejak 10 Nov; tidak ada event on-chain yang menunjukkan dekripsi/audit.
- **Yang belum terbukti:** apakah auditing selektif benar-benar dilakukan/diuji pada deployment ini, dan apakah scope-nya per deployment (doc Public), network-wide (doc Private Network), atau scoped keys (blog). **Kesimpulan artikel sebelumnya tetap berlaku.** Ketiga wording resmi yang bertentangan disajikan di C.6 — perlu konteks tim via ticket sebelum artikel menyimpulkan soal scope auditor.
- **Konteks baru dari GitHub (B.2):** kode escrow kunci auditor ada di `enygma_retail_payments`. Ini memperkuat bahwa mekanisme auditing dirancang/diimplementasikan di salah satu modul — tetapi tetap bukan bukti verifikasi live.

### F.4 Batasan lain yang bukan soal privasi

- **Aktivitas Enygma Sovereign di jaringan privat institusi tidak terlihat lewat public explorer.** Ketiadaan data publik tentang Sovereign bukan bukti ketiadaan aktivitas. Artikel harus menjelaskan pemisahan ini secara eksplisit.
- **Deployment bx diam sejak 3 Nov** (4 + 10 log, tidak berubah) — ini fakta log, bukan bukti bahwa bx "mati"; status dan rencana bx **unknown, perlu konteks tim**.
- **Data `topics[2]`/`topics[3]` `UserRegistered` bernilai `null` di API explorer** — quirk API, bukan data kosong; arti field tidak dapat dipastikan dari sumber ini.
- **Anomali slot implementasi token RLS** (C.3) — unknown, tidak diverifikasi lebih jauh.

---

## G. Peluang eksperimen baru

**Rekomendasi saja — tidak ada yang dieksekusi dalam audit ini.** Semua eksperimen di bawah ini memerlukan persetujuan Anara sebelum dijalankan, dan hasilnya harus dicocokkan dengan tx/RPC/kontrak/event log/ABI/source GitHub mengikuti struktur artikel yang direncanakan (perkenalan → arsitektur → aktivitas historis → volume terverifikasi → eksperimen → pencocokan → kesimpulan teramati vs belum dapat dipastikan).

### G.1 Eksperimen inti: alur lengkap shield → transfer → unshield

- Buat wallet testnet baru, minta faucet (1×/jam, per pilot blog), lalu lakukan registrasi → shielding → shielded transfer ke alamat kedua → unshielding, masing-masing dalam jumlah kecil dan berbeda agar dapat dilacak.
- Untuk setiap langkah, catat: tx hash, blok, event log yang muncul, dan bandingkan dengan klasifikasi D.7 (apakah pola event eksperimen cocok dengan aturan reconstruction?). Ini menguji langsung apakah ketiga aksi memang terpisah seperti yang diklasifikasikan.
- Uji apakah shielding memunculkan log token ERC-20 yang memperlihatkan jumlah (menutup gap F.1 poin 1).

### G.2 Uji visibilitas shielding lewat log token ERC-20

- Ambil log `Transfer` token RLS testnet (`0x07e17E17e17E17e17e17e17E17E17E17E17e17EA`) dan USDr (`0x0000000000000000000000000000000000000400`) pada rentang blok yang sama dengan vault yx, lalu cocokkan dengan tx shielding (272 tx). Pertanyaan: apakah jumlah shielding terlihat publik lewat log token meskipun log vault tidak menunjukkannya?

### G.3 Uji fee dan selisih 0,0001 RLS

- Ukur fee aktual per aksi (registrasi, shielding, transfer, unshielding) dari receipt tx eksperimen; bandingkan dengan klaim docs (relayer 15% ke Rayls Foundation; USDr +0,25%) dan selidiki asal selisih 0,0001 RLS yang masih unresolved. **Jangan sebut selisih itu rounding sebelum ada bukti.**

### G.4 Uji proof-time

- Ukur waktu proving secara lokal (atau catat waktu dari UI demo) dan bandingkan dengan empat angka resmi yang saling berbeda (408 ms / ~2,2 dtk / ~3 dtk / "under 4 s"). Catat perangkat, ukuran input, dan kondisi jaringan — angka tanpa konteks tidak bermakna.

### G.5 Uji deployment bx dan forwarder "next"

- Coba demo dengan konfigurasi bx: apakah bx masih dapat dipakai, atau memang hanya deployment awal yang tidak dilanjutkan? Konfirmasi lewat ticket dulu (C.3) sebelum menyimpulkan apa pun di publik.
- Amati apakah registrasi baru terus memakai forwarder `0x12B6640048DEB2e8fFDa4Bc10Bb2a640B70eCA6d` (sudah terlihat pada registrasi terakhir, D.9) — ini menguji apakah rotasi forwarder sedang berjalan.

### G.6 Monitoring kontinu dan finality (feedback reviewer)

- Perluas pengamatan ke lebih banyak tanggal/waktu atau monitoring kontinu (bukan dua snapshot 15 Nov dan 21 Nov saja) — misalnya pencatatan harian jumlah tx per tipe selama seminggu.
- Eksperimen finality terpisah jika memungkinkan (waktu hingga tx dianggap final menurut RPC/explorer).
- Controlled load test hanya di lingkungan yang sesuai — bukan dengan membanjiri public testnet tanpa pertimbangan.

### G.7 Bahan bacaan dan konteks sebelum eksperimen

- Telaah makalah IACR ePrint **2025/1638** (Rayls II) dan **2025/1639** (Rayls) — sumber baru yang belum ada di riset sebelumnya.
- Baca ulang `protocol_description.md` (blob `61b9447217a881dd3e47f7ade3fcc8d5e4df9a0f`) dan kode `enygma_retail_payments` (`auditor.go`, `UserRegistry.sol`) untuk menjelaskan mekanisme escrow auditor secara akurat di artikel.
- **Ticket-first (arahan moderator):** sebelum memublikasikan kesimpulan tentang (a) ketidaksesuaian proxy bx vs bundle, (b) scope auditor-access, (c) selisih fee 0,0001 RLS, (d) anomali slot token RLS — buka ticket agar tim memberi konteks. Mod tidak keberatan menerima ticket walau balasannya butuh waktu.

### G.8 Yang TIDAK direkomendasikan

- Jangan mencoba menjadi auditor (docs: "Nobody can ask to be an auditor. An existing auditor adds new ones.").
- Jangan menyimpulkan apa pun tentang Enygma Sovereign dari ketiadaan data publik.
- Jangan menyajikan angka "volume" yang mencampur token berbeda tanpa caveat desimal (E.3).

---

## H. Rekomendasi struktur repository penelitian

**Hanya rekomendasi. Repo baru TIDAK dibuat dalam audit ini.** Nama usulan `rayls-enygma-public-testnet-research` belum disetujui untuk dibuat/dipublikasikan; buat dan publikasikan hanya setelah persetujuan Anara. Struktur di bawah ini meniru pola repo mainnet (A.1) yang sudah terbukti lolos review (90/100):

```
rayls-enygma-public-testnet-research/
├── README.md                    # research question, network, method, hasil terverifikasi,
│                                # interpretasi + batasan, referensi resmi, snapshot source (commit hash)
├── data/
│   ├── raw/                     # raw RPC + raw API explorer responses (JSON, apa adanya)
│   ├── csv/                     # dataset olahan: registrations.csv, unshielding.csv,
│   │                            # vault-tx-classification.csv, daily-activity.csv
│   ├── metadata.json            # chain_id, rpc, metode, start/end block, retrieved_at_utc,
│   │                            # client/version, SHA-256 tiap dataset (pola repo mainnet)
│   └── checksums.sha256         # checksum semua dataset
├── scripts/
│   ├── fetch_logs.py            # paginasi 200.000 blok (cap API 1.000 hasil)
│   ├── classify_tx.py           # aturan klasifikasi D.7 (eksplisit, dapat dicek ulang)
│   ├── verify_dataset.py        # verifikasi CSV vs raw + PartialWithdrawal vs PaidOut
│   └── reproduce.py             # re-fetch rentang blok tetap
├── contracts/
│   ├── addresses.md             # peta kontrak C.2 + slot EIP-1967 C.3
│   └── abis/                    # ABI dari bundle demo (bila tersedia)
├── bundle/
│   ├── bundle-hashes.md         # ukuran + SHA-256 halaman dan bundle per tanggal (C.4)
│   └── deployments-7295799.md   # isi 7295799.json / br/7295799.json / 11155111.json
├── docs-review/
│   └── docs-wording.md          # tanggal update + kutipan verbatim tiap halaman docs/blog (C.6)
├── experiments/
│   ├── plan.md                  # rencana eksperimen G.1–G.6 (belum dieksekusi)
│   └── results/                 # hasil eksperimen + tx hash + receipt (setelah disetujui & dijalankan)
├── findings/
│   ├── verified-facts.md
│   ├── official-claims.md
│   ├── reconstructions.md       # aturan + hasil olahan, dipisah dari fakta
│   ├── unknowns.md              # daftar unknown + ticket yang dibuka
│   └── tickets.md               # log ticket ke tim Rayls (tanggal, isi, jawaban)
└── audit_report.json            # ringkasan mesin-terbaca (pola repo mainnet)
```

**Prinsip dokumentasi yang harus dipertahankan:** (1) raw data selalu disimpan apa adanya + checksum; (2) olahan (reconstruction) dipisah dari fakta dan aturannya ditulis eksplisit; (3) setiap pengumpulan data mencatat client/version + block identifiers + timestamp; (4) batasan dijelaskan di README, bukan disembunyikan; (5) observed vs reconstructed/estimated vs unobservable dibedakan di setiap angka volume; (6) tidak ada hash/alamat yang dikarang — unknown ditulis unknown.

---

## I. Daftar sumber, commit hash, contract address, transaction hash, dan file path yang benar-benar ditemukan

### I.1 Jaringan dan endpoint (verified fact)

- Chain ID testnet: **7.295.799** (`0x6f5337`); mainnet: 72.957
- RPC: `https://testnet-rpc.rayls.com`
- Explorer: `https://testnet-explorer.rayls.com`
- Demo: `https://enygma-testnet.rayls.com/`
- Relayer: `https://enygma-relayer-aafjr.ondigitalocean.app/rayls` (7295799), `https://enygma-relayer-aafjr.ondigitalocean.app/sepolia` (11155111)

### I.2 Kontrak (semua alamat lengkap — dari C.2/C.3)

- RLS token testnet (proxy): `0x07e17E17e17E17e17e17e17E17E17E17E17e17EA`
- RLS token Ethereum mainnet: `0xb5f7b021a78f470d31d762c1dda05ea549904fbd`
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
- UserRegistryImplementation (bx, di bundle): `0xB23124D2eE339d1E8175B9ec10D20217CE015c1C`
- SharedVaultProxy (bx): `0x94dafa3bf372cad68143ac535f845e74751d75ef`
- TokenFactory (bx): `0x7416094FFC5A1D0C2659DA0D5b81CeCc18f1BdAc`
- Auditor (EOA): `0x71AF09966CBED4434ccA97c40Fa38B8083548B95`
- Relayer: `0xa5f0c684eb49866a9f62f901cd85f98a19da0ac8`
- Multicall3: `0xca11bde05977b3631167028862be2a173976ca11`
- Forwarder "next" (yx): `0x12B6640048DEB2e8fFDa4Bc10Bb2a640B70eCA6d`
- EnygmaDvp: `0x7ec57a8f97b636a4b54633df826b2a4311018996`
- Implementasi live registry yx: `0x9686a3d5a9Fd2101d15888c6a09a64faFA7EE349`
- Implementasi live vault yx: `0xAd9667049f14D1757D147F652c41Dc241C57091C`
- Implementasi live registry bx: `0x66f87eaf23152bd5a155f96a85b7e5a64e3f6952`
- Implementasi live vault bx: `0x8551f451a5e7dc39d82ed08195eeda16abfe60a1`
- SharedVaultImplementation bx (di bundle): `0xe023791669A54EC41Ef1affA2c1B44460C1943CD`
- `auditorPublicKeyHash` registry yx: `0x4151c50e9250f5818a53f9e48e734bd4209407d19f966ede4f7988dd4af863e5`
- USDr: `0x0000000000000000000000000000000000000400`
- Token unshielding lain: `0x3ab29f9e8ef3a730731eda5e88eaf986ff824b4d`, `0xc66cb3ce397e70888e69d6e7e75474046c6617e4`, `0x076e2256c36196fce6e4cb7537f1edeb27d3a6b3`, `0x68660d8de06045f80c749400abc347081073ff5f`, `0xf4cf04f4173fbff71a8718517199e57e11b20af0`, `0xe50ab75c55db6a98d6e2d89496e54e4f5a391523`, `0xc81b66f670124d345b1a60165192508e31d39150`
- Alamat dengan provenance unknown: `0xd908BaeE382191D15E479589D9661A9E9b55b827` (dari `address.json` di repo)

### I.3 Transaction hash yang benar-benar ditemukan

- Upgrade registry yx: `0x908fdae3efbee9b058da2088eaf73f7f0031257df79953974fb87b1c5ac96fe8` (blok 23.400.006, 11 Nov 21:25:18 UTC)
- Upgrade vault yx: `0xc841126f7cf05d937967743f7db5cb80d04cf32ed1dca929aac23d952e97f3c4` (blok 23.399.976, 11 Nov 21:25:01 UTC)
- Registrasi terakhir (registry yx): `0x0c7419d5d3d334dae29f5e87bdde78481ed61b6ae2907429044b4e56903beb0a` (blok 24766266, 21 Nov 00:39 UTC, username `rq3faucet26`)
- Vault tx terakhir: `0x7f72b00105ab01cb600461487dad6ff7932bdb302c6a85d00a01b67df3117dd1` (21 Nov 03:25:55 UTC, `PaidOut`)
- Registrasi pertama yang dicatat dalam daftar baru: `0x67e579e18c80d6f4690fd51b3b0e3d11a8d00b49244d9725fd18aa9f266168e7` (`deepsync`, blok 24082221, 16 Nov 12:50 UTC)
- Shielded transfer (contoh): `0xee8b31ad3d0f00437ce36d4058af16f08af5c4103a60c896da34ad0bbf359211`
- Unshield (contoh): `0x282db91e109533bfd1e89ddde65021ec36ef38d54b721a64ed368855dbf19110`
- Tujuh tx `AuditorAdded`: tercantum lengkap di D.5
- Tx `AuditorKeyGiven` ke-4: `0x6d7df5de9919f9d52b1b7f9dd100141c8def1063a1df25f1bad7409548a1690c`
- Tx `AuditorPersonalKeySet`: `0x787bbe3cd3369aa325fdfbebf8b41e7554270c8867ca82505acd5f1e0edaf9a5`
- Tx implementasi registry yx di bundle: `0xe029bde6…` — **tercatat terpotong, full hash unknown** (blok 23395761)

### I.4 Commit hash dan file GitHub

- `raylsnetwork/Enygma` head: `0b1945ae6c827745d1ad48eddcec39df4b20277a` (19 Nov 2026, 22:48 UTC)
- Baseline pembanding: `3c61be782cbd31b108eacbda662d3a0a9219f6ae` (71 commit di belakang head)
- `protocol_description.md` blob: `61b9447217a881dd3e47f7ade3fcc8d5e4df9a0f` (37.302 byte, tidak berubah)
- Ciphertext binding DvP: commit `6a6a23b1cffde9b4e3a37e27375ddff9ed397578` (16 Nov 2026) — `CiphertextHash.sol` + test + perubahan salt
- File relevan: `enygma_retail_payments` (`auditor.go`, `UserRegistry.sol` — `mlKemAuditCt`/`aesAuditCt`); `enygma_payments` (tanpa peran auditor); `enygma_demo` (tidak berubah sejak 29 Okt 2026)
- Repo riset sebelumnya: `github.com/akira01111/rayls-enygma-research`, head `ab523db`, 4 commits
- Repo mainnet (referensi standar): `/home/hatch/workspace/rayls-mainnet-block-research-check`, commit `4ef462f` dan `a514353`

### I.5 Hash bundle dan halaman

- Halaman demo 21 Nov: 3.872 byte, SHA-256 `d709dc0639a80d71b127681fbd56ae7f6f9a9f83c38bf4b7f42239b4b961a28e` (baseline: 3.645 byte, `b615fd73aa999fb72529d37553ba0943d754e2f2e0f50468a07fe2e8fcb636c5`)
- Bundle utama 21 Nov: `assets/index-Dlv-HYaZ.js`, 1.422.052 byte, SHA-256 `7530bbc2d7a301c50e28923529cb9315f88145a9a25a7c71db8a1f34afd9ca68` (baseline: `index-BmNruHc0.js`, 1.338.924 byte, `c878b635cab69d9c529f4cd9e6fcd8fb606c0e2a9a3bd42af39ea435f065ec81`)

### I.6 Docs dan publikasi (tanggal + tautan)

- `docs.rayls.com/docs/enygma-privacy-and-auditing` — updated 2026-11-11T15:26:41.000Z
- `docs.rayls.com/docs/enygma-public` — updated 2026-11-11T21:36:24.000Z
- `docs.rayls.com/docs/enygma-public-who-sees-what` — updated 2026-11-11T21:36:27.000Z
- `docs.rayls.com/docs/how-enygma-public-works` — updated 2026-11-11T15:27:18.000Z
- `docs.rayls.com/docs/rayls-high-level-architecture` — updated 2026-11-11T21:37:02.000Z
- Blog `rayls.com/blog/auditability-without-surveillance-…` — published 2026-09-12, updated 2026-11-12
- Blog "controlled visibility" — updated 15 Nov 2026
- Pilot blog Rayls — 12 Nov 2026 (AES-256-GCM + ML-KEM + HKDF; faucet 1×/jam; roadmap) — URL persis tidak tercatat dalam audit ini (unknown)
- IACR ePrint **2025/1638** (Rayls II) dan **2025/1639** (Rayls)
- Artikel sebelumnya: X `status/2122127310585524690` (16 Nov 2026)

### I.7 File path lokal

- Laporan ini: `~/workspace/rayls-enygma-audit/ENYGMA-TESTNET-AUDIT-REPORT.md`
- Folder riset sebelumnya: `~/workspace/rayls-enygma-research/` (README.md, ama/ama-notes.md, audit/audit-status.md, demo-testing/, findings/, research/, sources/source-register.md, technical-evidence/technical-evidence.md)
- Repo referensi standar kualitas: `~/workspace/rayls-mainnet-block-research-check/` (README.md, rayls_blocks.csv, recent_600_blocks.csv, recent_600_metadata.json, recent_600_raw.json, reproduce_fixed_600.py, verify_dataset.py, windows/, audit_report.json)

### I.8 Yang sengaja tidak ada di daftar ini

Tidak ada hash/alamat/hasil pengujian yang dikarang. Semua yang tidak ditemukan ditandai **unknown** di bagiannya masing-masing (antara lain: full hash tx implementasi registry yx di bundle; arti slot implementasi token RLS; desimal token non-RLS/USDr; arti `topics[2]`/`topics[3]` `UserRegistered`; URL persis pilot blog; asal alamat `0xd908BaeE382191D15E479589D9661A9E9b55b827`).

---

## Penutup — status audit

Audit awal ini **selesai** sesuai brief: laporan A–I di atas adalah satu-satunya output. Tidak ada eksperimen yang dijalankan, tidak ada repo yang dibuat, tidak ada artikel yang ditulis, tidak ada publikasi, tidak ada transaksi.

**Langkah berikutnya yang memerlukan keputusan/persetujuan Anara:**
1. Tinjau laporan ini; putuskan apakah ticket-first ke tim Rayls dibuka untuk temuan bx, scope auditor, fee 0,0001 RLS, dan anomali slot token RLS.
2. Setujui/tolak pembuatan repo `rayls-enygma-public-testnet-research` (struktur di H hanya usulan).
3. Setujui/tolak eksperimen G.1–G.6 (masing-masing butuh persetujuan sebelum dijalankan).
4. Setelah itu barulah penulisan artikel dapat dimulai — dengan kesimpulan artikel sebelumnya yang tetap berlaku kecuali ada bukti baru dari eksperimen/ticket.
