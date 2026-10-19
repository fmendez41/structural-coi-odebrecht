# Reproduction guide

## Environment

The locked environment uses Python 3.12 or later, NetworkX 3.4.2, NumPy 2.5.4, and Matplotlib 3.11.2.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## One-command route

From the repository root:

```bash
python verify_results.py
python reproduce.py
```

The wrapper executes the original scripts in filename order. It does not reimplement any metric. Standard output from each script is saved under `outputs/tables/`; figures are written by the original scripts to `outputs/figures/`.

## Script-to-article map

| Script | Article output |
|---|---|
| `01_overview_metrics.py` | Table 2 - network overview and temporal dynamics |
| `02_detection_coi.py` | Table 3 - target-agnostic dual-exposure ranking |
| `03_p1_trajectory.py` | Table 4 and trajectory figure |
| `04_p2_knockout.py` | Table 5 and knockout figure; also v1 comparison described by the package |
| `05_p3_group_betweenness.py` | Table 6 - group-restricted betweenness |
| `06_p4_ego_stability.py` | Table 7 and ego-stability figure |
| `07_p5_vehicle_accretion.py` | Table 8 and vehicle-accretion figure |
| `11_conduit_facilitator.py` | Table 9 and conduit/structural-broker figure (legacy filename retained for compatibility) |
| `08_p2b_group_dependence.py` | Table 10 - institutionalized brokerage/group path dependence and figure |
| `09_p6_suppression.py` | Table 11 - exploratory non-edge anomaly diagnostic and figure (legacy filename retained for compatibility) |
| `10_link_prediction.py` | Table 12 - negative link-prediction result |
| `12_network_figures.py` | Main network figures, ego views, and appendix full-label figures |

## Fixed analytical conventions

- P2, P2b, and P3 use nodes in the Aval/Odebrecht and Estado blocs as endpoints, excluding nodes whose type is `evento` or `objeto`. Those nodes remain in the graph and may lie on a shortest path. This reproduces `+11.4%`/`+13.1%` in Table 5, `0.0224` in Table 6, and `37.8%`/`56.2%` in Table 10.
- P5 compares the raw clienteles in adjacent periods. It does not restrict the sets to nodes that happen to be present in both networks; the resulting Jaccard sequence is `0.286`, `0.778`, `1.000`.
- Resource Allocation score ties are represented as rank ranges. The stable headline result is FGN--CFC at rank 8 of 6,387; FGN--LCSG has RA = 0, zero common neighbors, and distance 3, but no unique rank inside the zero-score tail.
- Louvain uses `seed=42` and NetworkX 3.4.2. NetworkX 3.7 produces a different seeded partition, which is why the version is pinned rather than specified as an open lower bound.

## What cannot be regenerated from this repository alone

- The supplied notebooks document most original edges, but they do not exactly regenerate every deposited GEXF in their current active form.
- Of 916 edge occurrences across the original networks, 112 have no matching active `add_edge` statement in the supplied notebooks.
- Explicit notebook reference tokens do not consistently provide a verified source-document filename and page locator. Candidate filename matches remain unverified.
- The manuscript source and third-party documentary PDFs/books are not redistributed.

These gaps do not prevent rerunning the released network analyses from the deposited GEXF files, but they do limit independent reconstruction of the networks from primary documents.

## Rebuilding the provenance tables

The original notebooks are retained under `notebooks/provenance-construction/`. To reconstruct the audit tables without executing notebook code:

```bash
python src/extract_notebook_provenance.py \
  --notebook-dir notebooks/provenance-construction \
  --network-dir data/networks/original \
  --output-dir data/provenance \
  --source-inventory data/provenance/source_archive_inventory.csv
```

The archive inventory was created from a local copy of `N1Ref.zip` with:

```bash
python src/inventory_source_archive.py N1Ref.zip data/provenance/source_archive_inventory.csv
```

The archive itself is intentionally not required for the network-metric reproduction route.

## Verification performed for this repository

The full wrapper and `verify_results.py` completed successfully on 2026-10-19 with Python 3.14.3, NetworkX 3.4.2, NumPy 2.5.4, and Matplotlib 3.11.2. All 12 scripts ran, all 35 figure files were regenerated, and every headline numerical check passed. The figures deposited in `outputs/figures/` are the same files supplied to the final LaTeX package.

