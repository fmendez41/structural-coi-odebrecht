# Provenance reconstruction

This directory records a conservative, machine-auditable reconstruction from the 16 supplied network-construction notebooks and the inventory of `N1Ref.zip`. It does not treat a filename similarity as proof and it does not invent page locators or bibliographic metadata.

## Files

- `edges_provenance.csv`: one row for every edge occurrence in each deposited original GEXF. A match means that the same unordered node pair appears in an active `add_edge` statement in at least one supplied notebook.
- `notebook_edge_statements.csv`: every active, statically readable notebook edge statement, with notebook, cell, line, adjacent comments, and explicit reference tokens.
- `notebook_reconstruction_audit.csv`: comparison between each graph composition declared by the latest master notebook and its declared GEXF output, when that output is present in the repository.
- `source_archive_inventory.csv`: complete file inventory and SHA-256 hashes for `N1Ref.zip`; third-party source documents are listed but not redistributed.
- `provenance_extraction_summary.json`: counts by notebook and deposited network.

## Current coverage

Across the five original deposited networks there are 916 network-edge occurrences. Of these, 804 match an active notebook edge statement and 112 do not. Counts are per network, so an edge repeated in several periods is counted once in each period.

| Network | Edges | Matched | Unmatched |
|---|---:|---:|---:|
| `Gch1.gexf` | 130 | 127 | 3 |
| `Gch2.gexf` | 246 | 179 | 67 |
| `Gch2OttoB.gexf` | 31 | 13 | 18 |
| `Gch3.gexf` | 225 | 214 | 11 |
| `Gch4.gexf` | 284 | 271 | 13 |

The `candidate_source_documents` column is populated only by a conservative fuzzy comparison between explicit notebook reference tokens and archive filenames. Every such value is labelled `unverified_title_match`; it is a review aid, not a verified citation. Blank source-document or locator fields remain blank.

## Interpretation limits

- The extraction reads active Python syntax. It excludes commented-out code and code inside triple-quoted strings.
- Notebook cell and line references identify the supplied notebook statement; they are not documentary page locators.
- The latest master notebook declares compositions and GEXF writes, but its active edge statements do not reproduce every deposited GEXF exactly. The differences are preserved in `notebook_reconstruction_audit.csv` rather than silently corrected.
- The largest unresolved cluster concerns the Otto Bula/offshore satellite and related edges in `Gch2.gexf`; several entity names in those GEXFs do not occur in the supplied notebook source.

Regenerate these tables with `src/extract_notebook_provenance.py`. Regenerate the source inventory with `src/inventory_source_archive.py` against a local copy of the archive.

