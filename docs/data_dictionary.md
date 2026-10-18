# Data dictionary

## Network files

All GEXF files are static, undirected graphs.

### `data/networks/original/`

These five files preserve the original Gephi exports supplied in the ZIP. They do not contain the normalized node-classification attributes present in the clean files.

| File | Nodes | Edges | Period or role |
|---|---:|---:|---|
| `Gch1.gexf` | 79 | 130 | pre-2010 |
| `Gch2.gexf` | 139 | 246 | 2010-2014 |
| `Gch2OttoB.gexf` | 32 | 31 | satellite/offshore circuit |
| `Gch3.gexf` | 120 | 225 | 2014-2016 |
| `Gch4.gexf` | 124 | 284 | 2016-2019+ |

### `data/networks/clean/`

Entity-resolved documentary baseline (v1). Every clean network node carries the attributes `tipo`, `esfera`, and `bloque`.

| File | Nodes | Edges |
|---|---:|---:|
| `Gch1_clean.gexf` | 73 | 128 |
| `Gch2_clean.gexf` | 130 | 243 |
| `Gch2OttoB_clean.gexf` | 32 | 31 |
| `Gch3_clean.gexf` | 108 | 221 |
| `Gch4_clean.gexf` | 114 | 276 |

### `data/networks/enriched/`

Institutionally enriched v2 networks for the two later periods.

| File | Nodes | Edges |
|---|---:|---:|
| `Gch3_v2.gexf` | 109 | 225 |
| `Gch4_v2.gexf` | 116 | 283 |

The supplied documentation states that v2 adds two event nodes and seven edges anchored in the 2019 electoral-nullity petition:

- `Terna2016-NHMN`
- `Terna2016-CSJ`
- `Terna2016-PresidenciaJMSC`
- `NHMN-CSJ`
- `DemandaNulidad2019-ConsejoEstado`
- `DemandaNulidad2019-NHMN`
- `DemandaNulidad2019-CSJ`

## Node attributes

| Field | Meaning | Values documented in the supplied package |
|---|---|---|
| `id` / node identifier | Stable identifier used by scripts and manuscript appendix | string |
| `label` | GEXF display label | string |
| `tipo` | Node type | `persona`, `institucion`, `empresa`, `vehiculo`, `objeto`, `evento` |
| `esfera` | Sphere | `publico`, `privado`, `instrumental`, `dual`, `objeto` |
| `bloque` | Coarser affiliation used in inter-bloc tests | `Estado`, `Aval`, `Odebrecht`, `NHMN`, `Politicos`, `Intermediarios`, `Offshore`, `Proyecto`, `Solarte`, `Contexto` |

The GEXF files do not declare edge attributes. The separate provenance reconstruction recovers notebook statements and comments where available, without inserting them into or otherwise changing the networks.

## Provenance tables

`data/provenance/edges_provenance.csv` contains one row per edge occurrence in each original deposited network:

| Column | Meaning |
|---|---|
| `network` | Original GEXF in which the edge occurs |
| `source`, `target` | Undirected edge endpoints, preserving the GEXF labels |
| `match_status` | Whether an active notebook `add_edge` statement was found |
| `notebook_files` | Supplied notebooks containing that node pair |
| `graph_components` | Notebook graph variables receiving that edge |
| `notebook_locations` | Notebook, cell, and source-line audit locators |
| `evidence_notes` | Adjacent notebook comments preserved verbatim |
| `reference_tokens` | Explicit reference-like tokens extracted from those comments |
| `candidate_source_documents` | Archive filenames suggested by conservative title matching |
| `candidate_status` | `unverified_title_match` when candidates exist |

`notebook_edge_statements.csv` is the statement-level source table. `notebook_reconstruction_audit.csv` compares declared notebook graph compositions with their declared outputs. `source_archive_inventory.csv` lists all archive members, byte sizes, SHA-256 hashes, content categories, and redistribution decisions.

## Classification CSVs

`clasificacion_nodos_v3.csv` has 155 rows; `clasificacion_nodos_v4.csv` has 157 rows. Both use these columns:

| Column | Meaning supported by the supplied files |
|---|---|
| `node` | Canonical node identifier and join key for GEXF nodes |
| `tipo` | Node type |
| `esfera` | Sphere classification |
| `bloque` | Bloc classification |
| `presencia` | Raw period-presence string |
| `persistente_4redes` | Indicator of presence in all four period networks |
| `nota` | Documentary referent or explanatory note supplied by the author |

## Sensitivity CSV

`outputs/tables/sensibilidad_v1_v2.csv` is preserved exactly as supplied. Its columns are `Gch3`, `Gch4`, `metrica`, `v1`, `v2`, and `valor`. The nine rows summarize selected v1/v2 comparisons; some rows place descriptive text in the first two columns rather than using a normalized long-table schema.

