# Structural COI - Odebrecht

Reproducibility materials for **“Quantifying Structural Conflict-of-Interest Risk in Corruption Networks: A Temporal Network Analysis of the Odebrecht Case in Colombia.”**

Author: Andrés Felipe Méndez-Arenas

ORCID: [0009-0002-4183-6472](https://orcid.org/0009-0002-4183-6472)

## Scope

This repository contains the GEXF networks, node-classification CSVs, analysis code, and deposited outputs used for the article. The released code documents the source--target endpoint convention used in P2, P2b, and P3, reports tied ranks explicitly, and compares the raw period clienteles for P5. These implementation details align the scripts with the article's reported results; no network observation is changed.

The networks reconstruct documented relations from public judicial, arbitral, administrative, oversight, and journalistic sources. An edge represents a documented relation, not its intensity. The article treats the results as structural findings and not as independent proof of intention or legal responsibility.

## Repository layout

```text
data/
  networks/
    original/       original Gephi-exported GEXF files
    clean/          entity-resolved documentary baseline (v1)
    enriched/       institutionally enriched later-period networks (v2)
  classification/   v1 and v2 node classification tables
  provenance/       reconstructed edge/notebook provenance and source inventory
src/                Python analysis and figure-generation scripts
notebooks/          original network-construction notebooks from N1Ref.zip
outputs/
  figures/          deposited PNG/PDF figures and regenerated figures
  tables/           deposited sensitivity CSV and text logs from reproduction
supplementary/
  original-package/ exact ZIP supplied for this repository
docs/               methodology, data dictionary, and reproduction guide
```

## Quick reproduction

Python 3.12 or later is recommended for the locked environment.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python verify_results.py
python reproduce.py
```

Each original script remains independently executable, for example:

```bash
python src/02_detection_coi.py
python src/04_p2_knockout.py
python src/12_network_figures.py
```

The scripts print the article tables. `reproduce.py` preserves that output as UTF-8 text files in `outputs/tables/`. Figure-producing scripts write to `outputs/figures/`.

## Reproducibility status

The code provides a complete route to rerun the network metrics and regenerate the deposited figures from the released GEXF files. `verify_results.py` checks the numerical values highlighted in the manuscript before the full figure-generation run.

Three conventions are fixed explicitly:

- Event and object nodes remain in the topology and may lie on shortest paths, but they are excluded as source/target endpoints in P2, P2b, and P3. This reproduces the manuscript's knockout, subset-betweenness, and group-dependence values.
- P5 Jaccard uses the raw union of firm clienteles in adjacent periods; new or disappearing nodes remain in the denominator.
- Resource Allocation ties are reported as rank ranges. A zero-score dyad is not assigned a substantively meaningful ordinal position within the zero-score tail.

The dependency versions are locked in `requirements.txt`. In particular, NetworkX 3.4.2 reproduces the seeded Louvain modularity and participation values reported in the manuscript; NetworkX 3.7 changed those seeded partitions.

See [docs/reproduction.md](docs/reproduction.md) for the script-to-output map and verification notes.

## Data and provenance status

The supplementary `N1Ref.zip` contains 16 historical construction notebooks and a documentary-source collection. Static analysis of active notebook statements matches 804 of 916 edge occurrences in the five original GEXF files. The resulting edge table preserves notebook/cell/line locations, adjacent comments, and explicit reference tokens. It also retains 112 unmatched edge occurrences instead of filling them speculatively. Those 112 occurrences correspond to 75 unique undirected pairs.

A separate public-source audit of those 75 pairs is stored in `data/provenance/external_edge_audit.csv`, with normalized source metadata in `external_source_catalog.csv`. It identifies 60 directly supported candidates, 8 contextual-only relations, 2 period mismatches, and 5 relations not supported by the evidence reviewed. The decision rules and cautions are documented in `docs/external_provenance_audit.md`; the audit does not modify any original network or scientific result.

The newest master notebook declares the period compositions and GEXF writes, but its active statements are not byte-for-byte or edge-for-edge equivalent to every deposited GEXF. These differences are quantified in `data/provenance/notebook_reconstruction_audit.csv`. Candidate document filenames are explicitly marked as unverified title matches; they are not treated as confirmed citations or page locators.

The full source archive is identified by SHA-256 `28541C6BF17D501CD493C8197DA806D4B975C2FBFB1CC04958355FD828595EC1`. Its complete file inventory and per-file hashes are included, but third-party PDFs, books, downloaded web pages, and scans are not redistributed because their rights status has not been verified. The manuscript PDF is likewise not redistributed.

## License

Code and documentation are MIT licensed. The author-created network compilations, classification tables, and provenance tables are licensed CC BY 4.0. Neither license applies to underlying third-party records or works. See [LICENSES.md](LICENSES.md).

