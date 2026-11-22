# findings

Findings sorted by evidence label. Nothing here is a conclusion without
evidence — each entry cites the `raw-data/` it rests on.

- `verified-facts/` — facts verified from primary evidence: live RPC
  responses, explorer data, or source code that was actually read. Each
  entry states what was checked, where the evidence came from, and what
  it proves — and what it does not prove.
- `official-claims/` — claims from official Rayls sources:
  documentation, blog posts, and team statements. A claim stays a claim
  until it is independently checked. Each entry records the exact source
  and date, and whether it has been verified, contradicted, or is still
  untested.
- `reconstructions/` — results rebuilt by combining observable data —
  for example, classifying transactions from the events they emit. Each
  entry states the method, the data used, and the assumptions made. A
  reconstruction is not a direct observation, and reconstructed volume is
  never presented as observed volume.
- `inferences/` — inferences drawn from the evidence — reasonable
  interpretations, not verified facts. Each entry states what it rests
  on, what it concludes, and what evidence could prove it wrong. An
  inference is never written as if it were verified.
- `unknowns/` — questions that could not be answered with the evidence
  available. Each entry states the question, what was tried, and what
  blocks verification (missing source, unobservable shielded data, no
  public record, or a team answer still awaited). An unknown is never
  filled in with an assumption.

(The five subfolder READMEs that held these rules were removed in the
Phase 1 restructure, 22 Nov 2026; their rules were moved here verbatim
so nothing was lost. The subfolders themselves were empty — no finding
entries lived in them.)

Direct observations are recorded in `raw-data/` and referenced from the
finding they support.

## Current findings records

- Week 2 TX audit findings live in
  `experiments/transactions/tx-09edab2b/decoded/audit_summary.json`
  (labelled per question) and in `TX-AUDIT-REPORT.md` in the same package.
  They have not been copied into the folders above — the package is the
  canonical record, to avoid duplicate copies drifting apart.
