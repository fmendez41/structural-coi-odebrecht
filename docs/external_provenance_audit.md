# External-source audit of unmatched edges

Audit date: 2026-10-18.

This review covers the GEXF edge occurrences that were not located as active `add_edge` statements in the 16 supplied notebooks. It supplements the notebook reconstruction; it does not alter the deposited networks, scientific measurements, or results.

## Unit of analysis and result

There are 112 unmatched edge occurrences across the five deposited period networks. Because the same undirected pair can occur in more than one period, these correspond to 75 unique pairs.

| Audit status | Unique pairs | Interpretation |
|---|---:|---|
| `direct_support` | 60 | A reviewed source explicitly establishes the bilateral relation or the stated payment/corporate/institutional link. |
| `context_only` | 8 | The endpoints occur in the same episode, but the reviewed evidence does not establish a sufficiently specific bilateral link or the edge semantics are unclear. |
| `period_mismatch` | 2 | Evidence exists for a different period than the node label states. |
| `not_supported` | 5 | No adequate support was found, or the reviewed evidence points to a different actor or payment circuit. |

The row-level decisions are in `data/provenance/external_edge_audit.csv`; source metadata and URLs are in `data/provenance/external_source_catalog.csv`.

## Decision rules

- Corporate officer, shareholder, representative, employment, appointment, ownership, contractual, and documented transfer relations can qualify as direct support when the source names both endpoints.
- An allegation or investigative finding is described as such; it is not silently converted into an adjudicated fact.
- Co-occurrence in an investigation or news article is not enough to support a bilateral edge.
- A source about the 2014 re-election campaign does not support a node explicitly labelled as the 2010 presidential campaign.
- A payment vehicle used in the Gabriel Garcia circuit is not reassigned to the Otto Bula circuit without explicit evidence.
- Ambiguous or apparently misspelled identifiers are preserved in the audit table and flagged for correction rather than normalized silently.

## Material cautions

- `HPalaciosMejia` appears to refer to **Hugo** Palacios Mejia, not Hernando Palacios Mejia. The reviewed official decision documents a legal opinion but does not support a bribe edge.
- `DiogenesArosema` appears in the cited corporate reporting as **Diogenes Arosemena**.
- The evidence located for David Portilla and Esteban Moreno concerns the 2014 campaign; the GEXF endpoint says `CampanaPresJMSC2010`.
- The reviewed sources associate Oil & Gas Logistics and Pacific Infrastructure with the Gabriel Garcia/Lurion circuit, not with the payment attributed to Otto Bula.
- `MiguelElias` is described in the supplied classification only as part of Bernardo Miguel Elias's family or circle; that is insufficient for a bribe attribution.
- `PresidenciaAUV-RS-SII` is temporally true at government-period level, but the formal 2009 award was made by INCO. Its retention depends on whether edges encode direct acts or broader institutional context.

## Reproducibility and legal care

The catalog records URLs and source descriptions only. No press PDF, book, court compilation, or other third-party document was copied into the repository. Future reviewers should preserve the date accessed and add page or paragraph locators when a stable official copy is available. If an edge is corrected after review, the original GEXF should remain preserved and the change should be made in a separately versioned derived network with a documented rationale.
