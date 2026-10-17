# Structural COI - Odebrecht

Reproducibility materials for **“Quantifying Structural Conflict-of-Interest Risk in Corruption Networks: A Temporal Network Analysis of the Odebrecht Case in Colombia.”**

Author: Andres Felipe Mendez-Arenas  
ORCID: [0009-0002-4183-6472](https://orcid.org/0009-0002-4183-6472)

## Scope

This repository reorganizes the files supplied in `COI_Odebrecht_reproducibility.zip`. It contains the GEXF networks, node-classification CSVs, analysis code, and deposited outputs used for the article. No scientific formulas, parameters, or reported results were changed. The only code changes are repository-relative input and output paths.

The networks reconstruct documented relations from public judicial, arbitral, administrative, oversight, and journalistic sources. An edge represents a documented relation, not its intensity. The article treats the results as structural findings and not as independent proof of intention or legal responsibility.

## Repository layout

```text
data/
  networks/
    original/       original Gephi-exported GEXF files
    clean/          entity-resolved documentary baseline (v1)
    enriched/       institutionally enriched later-period networks (v2)
  classification/   v1 and v2 node classification tables
  provenance/       provenance gap note; no edge-level provenance file was supplied
src/                Python analysis and figure-generation scripts
notebooks/          no notebooks were supplied
outputs/
  figures/          deposited PNG/PDF figures and regenerated figures
  tables/           deposited sensitivity CSV and text logs from reproduction
supplementary/
  original-package/ exact ZIP supplied for this repository
docs/               methodology, data dictionary, and reproduction guide
```

## Quick reproduction

Python 3.10 or later is recommended by the supplied package.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
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

The supplied code provides a complete route to re-run the stated network metrics and regenerate the deposited figures from the released GEXF files. The package itself records two qualifications:

- Table 10 group-dependence values may differ by less than one percentage point because of shortest-path tie enumeration.
- Deep-tail Resource Allocation ranks among zero-score ties may vary with tie order.
- For the v2 knockout distance, the released implementation applies one common convention and reports `+13.3%` for NHMN alone, while the paper reports `+11.4%` from the original computation; the package documents the convention difference.
- Louvain community detection is seeded with `42`; second-decimal variation may still occur across NetworkX versions.

See [docs/reproduction.md](docs/reproduction.md) for the script-to-output map and verification notes.

## Data and provenance limitations

The ZIP did not include an edge-level provenance table connecting every relationship to a specific source document, page, date, or reference. No such metadata has been invented. The supplied materials do identify the two v2 event nodes and seven added institutional edges as anchored in the 2019 electoral-nullity petition, but do not provide a complete provenance record for all edges.

The manuscript PDF and third-party source documents are not redistributed here. The repository contains only the supplied analytical data, code, outputs, and the original reproducibility ZIP.

## License

The MIT license in this repository applies to the software and repository documentation. It does not relicense third-party source documents or imply ownership of underlying public records. A separate data license was not supplied, so no data license has been asserted.

