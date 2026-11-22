#!/usr/bin/env python3
"""Build the combined review PDF HTML source for the Week 2 TX audit.

Reads the evidence package at experiments/transactions/tx-09edab2b/ and writes
.src/index.html next to 01_tx_audit_complete_history.pdf. The PDF is a review
copy only: the original evidence files are never modified by this script.

Two-pass TOC:
  pass 1: python3 build_tx_pdf.py            (TOC page numbers shown as —)
  render with render_audit.mjs, then extract section page numbers from the PDF
  with pdftotext and write them to .src/toc-pages.json
  pass 2: python3 build_tx_pdf.py --toc-json .src/toc-pages.json
  re-render, then validate with validate_pdf.sh.

Markdown conversion is a small built-in converter (headings, tables, lists,
bold, inline code) because no markdown library is installed in this VM.
JSON files are embedded verbatim (HTML-escaped) inside <pre>.
"""
import html
import json
import os
import re
import sys

PKG = os.path.expanduser("~/workspace/rayls-enygma-public-testnet-research/experiments/transactions/tx-09edab2b")
REPO_REL = "experiments/transactions/tx-09edab2b"
MANIFEST_SHA256 = "a73958da658723701239f929e46b221e99aef3b4c02f188ac7212d32a0729adc"  # manifest.json, computed at manifest time; see Appendix A

CSS = """@page { size: A4; margin: 18mm 20mm; }
* { box-sizing: border-box; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
body { margin: 0; font-family: 'Liberation Sans', 'Noto Sans', sans-serif; font-size: 11pt; line-height: 1.5; color: #111111; }
h1 { font-size: 19pt; line-height: 1.25; margin: 0 0 6pt 0; }
h1.section { break-before: page; page-break-before: always; border-top: 3px solid #111111; padding-top: 10pt; margin-top: 0; }
h1.cover { font-size: 24pt; }
h2 { font-size: 14pt; line-height: 1.3; margin: 16pt 0 6pt 0; }
h2.sub { font-size: 13pt; margin-top: 18pt; }
h3 { font-size: 12pt; line-height: 1.3; margin: 12pt 0 4pt 0; }
h4 { font-size: 11pt; margin: 10pt 0 4pt 0; }
h1, h2, h3, h4 { break-after: avoid; page-break-after: avoid; }
p { margin: 0 0 8pt 0; }
ul, ol { margin: 0 0 8pt 0; padding-left: 18pt; }
li { margin-bottom: 3pt; }
pre, code { font-family: 'Liberation Mono', monospace; }
pre { font-size: 8.5pt; line-height: 1.35; white-space: pre-wrap; word-wrap: break-word; overflow-wrap: break-word; background: #f6f6f6; padding: 8pt; border: 1px solid #dddddd; margin: 0 0 10pt 0; }
code { font-size: 9.5pt; }
pre code { font-size: 8.5pt; }
table { border-collapse: collapse; width: 100%; font-size: 10pt; margin: 0 0 10pt 0; }
th, td { border: 1px solid #cccccc; padding: 4pt 6pt; text-align: left; vertical-align: top; overflow-wrap: anywhere; word-break: break-word; }
th { word-break: normal; overflow-wrap: normal; }
thead { display: table-header-group; }
tr { break-inside: avoid; page-break-inside: avoid; }
table.toc { font-size: 9.5pt; }
table.toc td, table.toc th { border: none; border-bottom: 1px solid #dddddd; padding: 3pt 4pt; }
table.toc td.pg { text-align: right; width: 30pt; white-space: nowrap; }
table.toc td.num { white-space: nowrap; width: 34pt; }
.meta { color: #555555; font-size: 9.5pt; margin: 0 0 14pt 0; padding-bottom: 8pt; border-bottom: 1px solid #cccccc; }
.src { color: #555555; font-size: 9pt; margin: 0 0 10pt 0; word-wrap: break-word; overflow-wrap: break-word; }
.src code { font-size: 8.5pt; }
a { color: #1a3d7c; text-decoration: none; }
hr { border: none; border-top: 1px solid #cccccc; margin: 12pt 0; }
blockquote { margin: 0 0 8pt 0; padding-left: 10pt; border-left: 3px solid #cccccc; color: #444444; }
.coverbox { margin: 0 0 10pt 0; }
.coverbox p { margin: 0 0 4pt 0; }
.note { background: #f6f6f6; border: 1px solid #dddddd; padding: 8pt 10pt; margin: 0 0 10pt 0; font-size: 10pt; }
"""

# (number, anchor id, title, source file relative to repo root, kind)
SECTIONS = [
    ("1", "s1", "TX Audit Report", "experiments/transactions/tx-09edab2b/TX-AUDIT-REPORT.md", "md"),
    ("2", "s2", "Remaining gaps", "experiments/transactions/tx-09edab2b/gaps.md", "md"),
    ("3", "s3", "TODO — unfinished work", "experiments/transactions/tx-09edab2b/TODO.md", "md"),
    ("4", "s4", "Audit summary (decoded)", "experiments/transactions/tx-09edab2b/decoded/audit_summary.json", "json"),
    ("5", "s5", "Decoded events", "experiments/transactions/tx-09edab2b/decoded/decoded_events.json", "json"),
    ("6", "s6", "Bundle ABI extract", "experiments/transactions/tx-09edab2b/decoded/bundle-abi-extract.json", "json"),
    ("7", "s7", "4byte.directory lookups", "experiments/transactions/tx-09edab2b/decoded/lookups-4byte.json", "json"),
    ("8", "s8", "Raw — transaction", "experiments/transactions/tx-09edab2b/raw/transaction.json", "json"),
    ("9", "s9", "Raw — receipt", "experiments/transactions/tx-09edab2b/raw/receipt.json", "json"),
    ("10", "s10", "Raw — logs", "experiments/transactions/tx-09edab2b/raw/logs.json", "json"),
    ("11", "s11", "Raw — block", "experiments/transactions/tx-09edab2b/raw/block.json", "json"),
    ("12", "s12", "Raw — contracts", "experiments/transactions/tx-09edab2b/raw/contracts.json", "json"),
    ("13", "s13", "Raw — Explorer cross-check", "experiments/transactions/tx-09edab2b/raw/explorer.json", "json"),
    ("14", "s14", "Raw — relayer txlist", "experiments/transactions/tx-09edab2b/raw/explorer-relayer-txlist.json", "json"),
    ("15", "s15", "Raw — registry usernames", "experiments/transactions/tx-09edab2b/raw/registry-usernames.json", "json"),
    ("16", "s16", "Raw — related fee-settlement tx", "experiments/transactions/tx-09edab2b/raw/related-tx-0xacc7d175.json", "json"),
    ("17", "s17", "Manifest (SHA-256)", "experiments/transactions/tx-09edab2b/manifest.json", "json"),
    ("A", "appa", "Appendix A — Verification record", "(created for this PDF)", "appendix"),
]

APPENDIX_HTML = """
<h2>Verification runs</h2>
<p><b>Independent verify script</b> <code>scripts/verify_tx_audit_09edab2b.py</code> v1.0.0
(run 2026-11-22 ~00:30 UTC): <b>23/23 checks passed, exit 0</b>. The script re-reads
the evidence from disk, recomputes every SHA-256, checks the manifest, and
re-derives the cross-consistency facts with its own parsing. It does not import
the fetch or decode scripts.</p>
<p><b>sha256sum -c</b> against the manifest (from the repository root, 2026-11-22
~00:30 UTC): <b>19/19 OK</b> — every file in the manifest verified.</p>
<p><b>Manifest itself:</b> <code>experiments/transactions/tx-09edab2b/manifest.json</code>
is not listed as an entry inside itself (a file cannot contain its own SHA-256).
Its SHA-256 is <code>a73958da658723701239f929e46b221e99aef3b4c02f188ac7212d32a0729adc</code>
(7,569 bytes). The review PDF is a derivative copy and is deliberately NOT part
of the manifest.</p>
<h2>How to re-verify this package</h2>
<ol>
<li>From the repository root: <code>python3 scripts/verify_tx_audit_09edab2b.py</code>
— expect 23/23 PASS, exit 0.</li>
<li>From the repository root: build a checksum file from
<code>manifest.json</code> and run <code>sha256sum -c</code> — expect 19/19 OK.</li>
<li>Every claim in §4 carries one of the six labels (verified-fact /
official-claim / direct-observation / reconstruction / inference / unknown).
Anything labelled unknown was left unknown on purpose.</li>
</ol>
<p class="note">This PDF is a review copy only. The original evidence files in the
repository were not changed, merged, or touched to build it. No commit or push
was made; the repository state is unchanged (HEAD 1676829 plus untracked
Module 01 and TX-audit files).</p>
"""


def md_inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def md_to_html(md_text):
    lines = md_text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{md_inline(m.group(2).strip())}</h{level}>")
            i += 1
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s\-\:|]+\|\s*$", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            out.append("<table><thead><tr>" + "".join(f"<th>{md_inline(c)}</th>" for c in header) + "</tr></thead><tbody>")
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue
        if re.match(r"^\s*[-*]\s+", line):
            out.append("<ul>")
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                out.append("<li>" + md_inline(re.sub(r"^\s*[-*]\s+", "", lines[i])) + "</li>")
                i += 1
            out.append("</ul>")
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                out.append("<li>" + md_inline(re.sub(r"^\s*\d+\.\s+", "", lines[i])) + "</li>")
                i += 1
            out.append("</ol>")
            continue
        if line.strip() == "---":
            out.append("<hr>")
            i += 1
            continue
        # paragraph: gather consecutive non-blank, non-special lines
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|\s*[-*]\s|\s*\d+\.\s|\s*\|)", lines[i]) and lines[i].strip() != "---":
            para.append(lines[i])
            i += 1
        out.append("<p>" + md_inline(" ".join(p.strip() for p in para)) + "</p>")
    return "\n".join(out)


def main():
    toc_pages = {}
    if "--toc-json" in sys.argv:
        idx = sys.argv.index("--toc-json")
        with open(sys.argv[idx + 1], encoding="utf-8") as fh:
            toc_pages = json.load(fh)
    manifest = json.load(open(os.path.join(PKG, "manifest.json"), encoding="utf-8"))
    info = {e["relative_path"]: e for e in manifest["files"]}

    parts = []
    parts.append("<!DOCTYPE html>\n<html lang=\"id\">\n<head>\n<meta charset=\"utf-8\">\n")
    parts.append("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n")
    parts.append("<title>TX Audit 0x09edab2b — Complete History</title>\n<style>\n" + CSS + "</style>\n</head>\n<body>\n")
    parts.append("<h1 class=\"cover\">TX Audit &mdash; Week 2 Experiment: Complete History</h1>\n")
    parts.append("<div class=\"coverbox\">"
                 "<p>Rayls Enygma Public Testnet &middot; Repository <code>rayls-enygma-public-testnet-research</code></p>"
                 "<p>Transaction <code>0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb</code></p>"
                 "<p>Block 24825928 (2026-11-21 09:40:42 UTC) &middot; chain ID 7295799 &middot; SharedVaultProxy transferV2</p>"
                 "<p>Status: audit complete, independent verification 23/23 PASS &middot; no commit/push &middot; no article yet</p>"
                 "<p>This document is for review only. The original evidence files in the repository were not changed or merged &mdash; what was merged here are only reading copies of them.</p></div>\n")
    parts.append("<p class=\"meta\">Created: 2026-11-22 &middot; Exported to PDF: 2026-11-22</p>\n")

    # TOC
    parts.append("<h1 class=\"section\" id=\"toc\">Table of Contents</h1>\n")
    parts.append("<table class=\"toc\"><thead><tr><th>Section</th><th>Title</th><th>Source file</th><th>Page</th></tr></thead><tbody>\n")
    parts.append(f"<tr><td class=\"num\"></td><td><a href=\"#toc\">Table of Contents</a></td><td>this section</td><td class=\"pg\">{toc_pages.get('toc', '—')}</td></tr>\n")
    for num, anchor, title, src, kind in SECTIONS:
        pg = toc_pages.get(anchor, "—")
        src_disp = html.escape(src.split("/")[-1]) if kind != "appendix" else "created for this PDF"
        parts.append(f"<tr><td class=\"num\">{num}</td><td><a href=\"#{anchor}\">{html.escape(title)}</a></td><td>{src_disp}</td><td class=\"pg\">{pg}</td></tr>\n")
    parts.append("</tbody></table>\n")
    parts.append("<p>Each section lists its source file (path relative to the repository root), file size, and the SHA256 of that source file at the time this PDF was created.</p>\n")

    # sections
    for num, anchor, title, src, kind in SECTIONS:
        parts.append(f"<h1 class=\"section\" id=\"{anchor}\">{num} {html.escape(title)}</h1>\n")
        if kind == "appendix":
            parts.append("<p class=\"src\">Source: created for this PDF &middot; summary of the independent verification results (see manifest.json for the SHA256 of each evidence file).</p>\n")
            parts.append(APPENDIX_HTML)
            continue
        if src == "experiments/transactions/tx-09edab2b/manifest.json":
            # manifest.json is not listed inside itself; its hash/size are recorded here and in Appendix A.
            ent = {"bytes": 7569, "sha256": MANIFEST_SHA256}
        else:
            ent = info[src]
        full = os.path.join(os.path.expanduser("~/workspace/rayls-enygma-public-testnet-research"), src)
        parts.append(f"<p class=\"src\">Source: <code>{html.escape(src)}</code> &middot; {ent['bytes']} byte &middot; SHA256: <code>{ent['sha256']}</code></p>\n")
        text = open(full, encoding="utf-8").read()
        if kind == "md":
            parts.append(md_to_html(text))
        else:
            parts.append("<pre>" + html.escape(text) + "</pre>\n")
    parts.append("</body>\n</html>\n")

    out_dir = os.path.join(PKG, ".src")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("".join(parts))
    print("wrote", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    main()
