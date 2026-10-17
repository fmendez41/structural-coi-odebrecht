# Methodology represented in the released code

This note summarizes the methods implemented by the supplied Python files and described in the manuscript. It does not add analytical claims.

## Network construction and versions

The case is represented as static, undirected, unweighted networks for four periods plus one satellite network:

| Period/network | Clean v1 nodes | Edges | Enriched v2 |
|---|---:|---:|---|
| pre-2010 | 73 | 128 | not applicable |
| 2010-2014 | 130 | 243 | not applicable |
| 2014-2016 | 108 | 221 | 109 nodes / 225 edges |
| 2016-2019+ | 114 | 276 | 116 nodes / 283 edges |
| Otto Bula satellite | 32 | 31 | not applicable |

The supplied documentation states that entity resolution reduced 169 raw labels to 155 canonical nodes through 13 merges and one exclusion. The v2 files add `Terna2016` and `DemandaNulidad2019` plus seven institutional edges, yielding a 157-node classification. Headline analyses use v2 for the two later periods; the link-prediction comparison uses v1 because the v2 additions are institutional facts known ex post.

## Three-stage framework

### Stage 1 - detection

For each person node, the code calculates a dual-exposure index:

`COI(v) = sqrt(E_public(v) * E_private(v))`

where the two terms count public- and private-sphere neighbors. Institutions and vehicles remain in the topology but are excluded from this ranking.

### Stage 2 - characterization

The code calculates or compares:

- normalized betweenness centrality and period percentile;
- Louvain modularity and the Guimera-Amaral participation coefficient (`seed=42`);
- knockout changes in private-bloc-to-State mean geodesic distance and global efficiency;
- group-restricted betweenness for paths from the Aval/Odebrecht blocs to the State;
- sphere-split Jaccard stability of the focal ego network;
- degree and clientele retention for the supplied corporate-vehicle set.

The constitutive public set used by the released code is `{CSJ, FGN, FGNAdhoc}`. The facilitator ego-cluster is `{NHMN, M&MACLtda, MNA, EstudioJuridicoMNALtda, NHMAbogados, NCMH}`.

### Stage 3 - materialization

The group path-dependence calculation reports the share of source-target pairs for which every shortest path traverses the specified group and the share of shortest-path instances that traverse it. Resource Allocation is calculated for every unconnected dyad and ranked as unrealized structural pressure.

## Scope stated in the manuscript

An edge records a documented relation such as contract, payment, representation, appointment, kinship, or investigation; it does not encode intensity. The underlying sources are described as public judicial decisions, arbitral awards, oversight-agency resolutions, an investigative account, and an electoral-nullity petition. The manuscript states that the findings measure structural position and consequences, not intention or legal responsibility.

## Implementation notes

- Networks are read with NetworkX from the released GEXF files.
- Global-efficiency and geodesic calculations use the undirected graphs as stored.
- Louvain detection is seeded with `42`.
- Figure layouts use NetworkX spring layout with `seed=42`.
- The code does not read the classification CSVs during metric computation because the clean/enriched GEXF files already carry `tipo`, `esfera`, and `bloque` node attributes.

