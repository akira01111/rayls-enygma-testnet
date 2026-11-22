# raw-data

Raw evidence exactly as captured: RPC responses, explorer exports, demo bundle
files, and screenshots.

Rules:

- Files in this folder must never be modified after they are added.
- A correction or a new capture goes in as a new file, never as an edit.
- Every file records its source (URL, RPC endpoint, or app) and capture time
  in its name or in a short note next to it.
- Nothing here is a conclusion. Conclusions live in `findings/`, with a
  reference back to the files used.

## Storage rules by kind

(The four subfolder READMEs that held these rules were removed in the
Phase 1 restructure, 22 Nov 2026; their rules were moved here verbatim
so nothing was lost.)

- **Explorer exports** — exports downloaded from the block explorer:
  transaction lists, event logs, and token transfer lists. Stored exactly
  as downloaded. Each export records the download date and the source URL.
  Nothing here is edited or re-formatted after download.
- **Original documents** — original documents as published: documentation
  pages saved as found, PDFs, and official posts. Stored unchanged. Each
  file records the source URL and the date it was accessed. A file here is
  a copy of the source — not a summary, and not a conclusion about what it
  says.
- **RPC responses** — raw RPC request and response pairs, stored exactly
  as returned. Each file records the endpoint, the method, the parameters,
  and the time of the call. Responses are never edited or trimmed.
- **Transaction receipts** — transaction receipts exactly as returned by
  the RPC endpoint or explorer. Each file records the transaction hash it
  belongs to. Receipts are never edited after they are saved.
