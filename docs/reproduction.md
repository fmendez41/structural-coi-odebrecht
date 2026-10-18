# Reproduction guide

## Environment

The supplied package specifies Python 3.10 or later with NetworkX 3.0 or later, NumPy, and Matplotlib.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## One-command route

From the repository root:

```bash
python reproduce.py
```

The wrapper executes the original scripts in filename order. It does not reimplement any metric. Standard output from each script is saved under `outputs/tables/`; figures are written by the original scripts to `outputs/figures/`.

## Script-to-article map

| Script | Article output |
|---|---|
| `01_overview_metrics.py` | Table 2 - network overview and temporal dynamics |
| `02_detection_coi.py` | Table 3 - unsupervised COI detection |
| `03_p1_trajectory.py` | Table 4 and trajectory figure |
| `04_p2_knockout.py` | Table 5 and knockout figure; also v1 comparison described by the package |
| `05_p3_group_betweenness.py` | Table 6 - group-restricted betweenness |
| `06_p4_ego_stability.py` | Table 7 and ego-stability figure |
| `07_p5_vehicle_accretion.py` | Table 8 and vehicle-accretion figure |
| `11_conduit_facilitator.py` | Table 9 and conduit/facilitator figure |
| `08_p2b_group_dependence.py` | Table 10 and group-dependence figure |
| `09_p6_suppression.py` | Table 11 and suppression figure |
| `10_link_prediction.py` | Table 12 - negative link-prediction result |
| `12_network_figures.py` | Main network figures, ego views, and appendix full-label figures |

## Expected qualifications from the supplied package

The package's original README reports exact reproduction for the principal metrics except for explicitly documented conventions:

- Table 10 can vary by less than one percentage point because of path-enumeration ties.
- Table 11 headline ranks are exact; ordering among deep-tail zero-score ties can vary.
- The released v2 knockout implementation produces `+13.3%` for NHMN alone (`+14.9%` for the ego-cluster), whereas the paper's original computation reports `+11.4%` (`+13.1%`). The supplied package attributes this to the common distance convention used in the released scripts. The rankings, efficiency changes, and v1 comparison are stated to remain invariant or exact.
- Louvain-related values may change in the second decimal across NetworkX versions despite `seed=42`.

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

The full wrapper completed successfully on 2026-10-17 with Python 3.14.3, NetworkX 3.7, NumPy 2.5.4, and Matplotlib 3.11.2. All 12 scripts ran, all 35 deposited figure filenames were regenerated, and table output was captured in `outputs/tables/`.

The rerun reproduced the headline COI values, rankings, percentiles, knockout efficiency changes, sphere-split Jaccard values, link-prediction result, suppression ranks, and other values highlighted by the supplied package. It also reproduced the documented convention-dependent outcomes: v2 knockout distance of `+13.3%` for NHMN alone and group-path instance share of `56.6%`.

Two environment-sensitive observations should be retained:

- Under NetworkX 3.7, the participation coefficients printed for NHMN were `0.500`, `0.473`, `0.768`, and `0.655`. These differ from some values cited in the supplied package, consistent with its warning that Louvain partitions can vary by NetworkX version. The package did not provide the exact original dependency versions, so an exact environment lock cannot be reconstructed without additional information.
- Regenerated figure files were not byte-identical to the deposited figures under this environment. This is expected for NetworkX/Matplotlib layout and rendering changes. After verification, the repository copy of `outputs/figures/` was restored byte-for-byte from the supplied ZIP; the generated text logs were retained.

