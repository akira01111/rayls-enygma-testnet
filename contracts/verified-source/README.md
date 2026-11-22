# verified-source

Source-code verification status for each contract in `../addresses/`:
verified on the explorer, unverified, or taken from a public repository.

Verification status is recorded as found — never assumed, and never upgraded
without a fresh check.

## Status (22 Nov 2026)

**No verified contract source exists for the deployed SharedVault
implementation** (`0xAd9667049f14D1757D147F652c41Dc241C57091C`, vault yx) or
for the deployed UserRegistry implementation
(`0x9686a3d5a9Fd2101d15888c6a09a64faFA7EE349`). The initial audit (§B) found
no `SharedVault` file in the public `raylsnetwork/Enygma` repositories and
no testnet addresses in them. The Week 2 TX audit confirmed the transferV2
selector and event signatures on-chain against the demo bundle's client-side
ABI — that proves the function/event signatures, NOT the internal contract
logic (proof verification, note handling, fee accounting). Do not claim
otherwise. If verified source appears, record its explorer link and
verification date here.
