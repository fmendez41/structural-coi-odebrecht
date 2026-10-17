"""
coi_lib.py — Shared library for the COI–Odebrecht analysis.

Implements the metrics of the three-stage framework described in
"Quantifying Conflict of Interest as a Precursor of Corruption"
(Méndez-Arenas, submitted to Journal of Complex Networks).

All functions operate on the released GEXF files; node attributes used:
  tipo   : persona / institucion / empresa / vehiculo / objeto / evento
  esfera : publico / privado / instrumental / dual / objeto
  bloque : Estado / Aval / Odebrecht / NHMN / Politicos / Intermediarios /
           Offshore / Proyecto / Solarte / Contexto
"""
import math
import os

import networkx as nx
import numpy as np

# ----------------------------------------------------------------------
# Paths (relative to the repository root: src/ sits next to data/)
# ----------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEXF = os.path.join(ROOT, "data", "networks")

PATHS = {
    # documentary baseline (v1 = clean v3 entity resolution)
    "pre-2010":        os.path.join(GEXF, "clean", "Gch1_clean.gexf"),
    "2010-14":         os.path.join(GEXF, "clean", "Gch2_clean.gexf"),
    "2014-16":         os.path.join(GEXF, "clean", "Gch3_clean.gexf"),
    "2016-19+":        os.path.join(GEXF, "clean", "Gch4_clean.gexf"),
    "satellite":       os.path.join(GEXF, "clean", "Gch2OttoB_clean.gexf"),
    # institutionally enriched (v2): adds Terna2016, DemandaNulidad2019 + 7 edges
    "2014-16 v2":      os.path.join(GEXF, "enriched", "Gch3_v2.gexf"),
    "2016-19+ v2":     os.path.join(GEXF, "enriched", "Gch4_v2.gexf"),
}

# Four period networks, headline (v2) versions
PERIODS_V2 = ["pre-2010", "2010-14", "2014-16 v2", "2016-19+ v2"]
PERIODS_V1 = ["pre-2010", "2010-14", "2014-16", "2016-19+"]

# Analytical blocs
SRC_BLOC = {"Aval", "Odebrecht"}          # private blocs (sources)
TGT_BLOC = {"Estado"}                     # State bloc (targets)

# Facilitator ego-cluster: focal individual + four sequential firms + son
NHMN_EGO = {"NHMN", "M&MACLtda", "MNA", "EstudioJuridicoMNALtda",
            "NHMAbogados", "NCMH"}

# Constitutive public contacts (P4 sphere split, pre-registered)
CONSTITUTIVE = {"CSJ", "FGN", "FGNAdhoc"}


def load(name):
    """Load one of the released networks by its period name."""
    return nx.read_gexf(PATHS[name])


def load_all(v2=True):
    """Load the four period networks as an ordered dict {name: Graph}."""
    names = PERIODS_V2 if v2 else PERIODS_V1
    return {n: load(n) for n in names}


# ----------------------------------------------------------------------
# Stage 1 — detection: dual-exposure COI index
# ----------------------------------------------------------------------
def coi_index(G, node):
    """COI(v) = sqrt(E_pub(v) * E_priv(v)), counted over v's neighbors."""
    if node not in G:
        return None
    e_pub = sum(1 for nb in G.neighbors(node)
                if G.nodes[nb].get("esfera") == "publico")
    e_priv = sum(1 for nb in G.neighbors(node)
                 if G.nodes[nb].get("esfera") == "privado")
    return math.sqrt(e_pub * e_priv), e_pub, e_priv


def coi_ranking(G):
    """COI index for every person node; returns sorted [(coi, node, e_pub, e_priv)]."""
    rows = []
    for n, d in G.nodes(data=True):
        if d.get("tipo") != "persona":
            continue
        coi, ep, epr = coi_index(G, n)
        rows.append((coi, n, ep, epr))
    return sorted(rows, reverse=True)


# ----------------------------------------------------------------------
# Stage 2 — characterization
# ----------------------------------------------------------------------
def betweenness_profile(G, node):
    """Normalized betweenness, percentile within the whole network,
    and rank among person nodes."""
    bc = nx.betweenness_centrality(G)
    vals = sorted(bc.values())
    # Paper convention: share of nodes with value <= the node's own
    # (the node counts itself), i.e. (strictly below + 1) / n.
    pct = 100 * (sum(1 for v in vals if v < bc[node]) + 1) / len(vals)
    persons = [n for n in G.nodes() if G.nodes[n].get("tipo") == "persona"]
    rank = sorted(persons, key=lambda n: bc[n], reverse=True).index(node) + 1
    return bc[node], pct, rank, len(persons)


def participation_coefficient(G, node, partition=None):
    """Guimerà–Amaral participation coefficient over a Louvain partition."""
    if partition is None:
        from networkx.algorithms.community import louvain_communities
        comms = louvain_communities(G, seed=42)
        partition = {n: i for i, c in enumerate(comms) for n in c}
    k = G.degree(node)
    if k == 0:
        return 0.0
    counts = {}
    for nb in G.neighbors(node):
        s = partition[nb]
        counts[s] = counts.get(s, 0) + 1
    return 1 - sum((c / k) ** 2 for c in counts.values())


def mean_interbloc_distance(G, src=SRC_BLOC, tgt=TGT_BLOC):
    """Mean geodesic distance over directed source–target instances
    (unreachable pairs are skipped)."""
    sources = [n for n in G.nodes() if G.nodes[n].get("bloque") in src]
    targets = [n for n in G.nodes() if G.nodes[n].get("bloque") in tgt]
    dists = []
    for s in sources:
        sp = nx.single_source_shortest_path_length(G, s)
        dists.extend(sp[t] for t in targets if t in sp and t != s)
    return float(np.mean(dists)) if dists else float("inf")


def knockout(G, removed, src=SRC_BLOC, tgt=TGT_BLOC):
    """P2: % change in mean inter-bloc distance and in global efficiency
    after removing `removed` (list of node ids)."""
    base_d = mean_interbloc_distance(G, src, tgt)
    base_e = nx.global_efficiency(G)
    H = G.copy()
    H.remove_nodes_from([n for n in removed if n in H])
    after_d = mean_interbloc_distance(H, src, tgt)
    after_e = nx.global_efficiency(H)
    dd = 100 * (after_d - base_d) / base_d if base_d else float("nan")
    de = 100 * (after_e - base_e) / base_e if base_e else float("nan")
    return dd, de, nx.number_connected_components(H)


def group_restricted_betweenness(G, actor, src=SRC_BLOC, tgt=TGT_BLOC):
    """P3: share of all shortest-path instances between the private blocs
    and the State that pass through `actor` (as an interior node)."""
    if actor not in G:
        return None
    sources = [n for n in G.nodes()
               if G.nodes[n].get("bloque") in src and n != actor]
    targets = [n for n in G.nodes()
               if G.nodes[n].get("bloque") in tgt and n != actor]
    total = through = 0
    for s in sources:
        for t in targets:
            if s == t:
                continue
            try:
                paths = list(nx.all_shortest_paths(G, s, t))
            except nx.NetworkXNoPath:
                continue
            total += len(paths)
            through += sum(1 for p in paths if actor in p[1:-1])
    return through / total if total else 0.0


def ego_jaccard_split(G_a, G_b, node, constitutive=CONSTITUTIVE):
    """P4: Jaccard stability of `node`'s ego network between two periods,
    split into private / public-transactional / public-constitutive.
    Paper convention: raw neighborhoods (no restriction to common nodes) —
    a neighbor absent from the later network counts as a lost tie."""

    def nbrs(G):
        out = {"priv": set(), "trans": set(), "const": set()}
        for nb in G.neighbors(node):
            esf = G.nodes[nb].get("esfera")
            if esf == "privado":
                out["priv"].add(nb)
            elif esf == "publico":
                out["const" if nb in constitutive else "trans"].add(nb)
        return out

    a, b = nbrs(G_a), nbrs(G_b)
    res = {}
    for k in a:
        union = a[k] | b[k]
        res[k] = (len(a[k] & b[k]) / len(union)) if union else None
    return res


# ----------------------------------------------------------------------
# Stage 3 — materialization
# ----------------------------------------------------------------------
def group_path_dependence(G, group, src=SRC_BLOC, tgt=TGT_BLOC):
    """P2b: (share of s–t pairs whose EVERY shortest path traverses the
    group, share of shortest-path INSTANCES that traverse it).
    Group members are excluded from the endpoint sets."""
    gset = set(group)
    sources = [n for n in G.nodes()
               if G.nodes[n].get("bloque") in src and n not in gset]
    targets = [n for n in G.nodes()
               if G.nodes[n].get("bloque") in tgt and n not in gset]
    pairs = pairs_dep = inst = inst_dep = 0
    for s in sources:
        for t in targets:
            if s == t:
                continue
            try:
                paths = list(nx.all_shortest_paths(G, s, t))
            except nx.NetworkXNoPath:
                continue
            pairs += 1
            inst += len(paths)
            hits = sum(1 for p in paths if gset & set(p[1:-1]))
            inst_dep += hits
            if hits == len(paths):
                pairs_dep += 1
    return (100 * pairs_dep / pairs if pairs else 0.0,
            100 * inst_dep / inst if inst else 0.0)


def resource_allocation_ranking(G):
    """P6: Resource Allocation score for every unconnected dyad,
    ranked by unrealized structural pressure (descending)."""
    nodes = list(G.nodes())
    rows = []
    for i, u in enumerate(nodes):
        for v in nodes[i + 1:]:
            if G.has_edge(u, v):
                continue
            cn = set(G.neighbors(u)) & set(G.neighbors(v))
            ra = sum(1 / G.degree(w) for w in cn)
            rows.append((ra, u, v, len(cn)))
    rows.sort(key=lambda r: (-r[0], r[1], r[2]))
    return rows


def degree_entropy(G):
    """Shannon entropy of the degree distribution (bits)."""
    from collections import Counter
    degs = Counter(dict(G.degree()).values())
    n = G.number_of_nodes()
    return -sum((c / n) * math.log2(c / n) for c in degs.values())


def modularity_louvain(G, seed=42):
    from networkx.algorithms.community import louvain_communities, modularity
    comms = louvain_communities(G, seed=seed)
    return modularity(G, comms), comms
