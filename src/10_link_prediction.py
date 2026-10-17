"""Table 12 — the negative result: precision@K of Jaccard, Resource
Allocation and Preferential Attachment across the three transitions,
computed on the documentary baseline (v1), as in the paper."""
import networkx as nx

from coi_lib import load

TRANSITIONS = [
    ("pre-2010 → 2010-14",  "pre-2010", "2010-14"),
    ("2010-14 → 2014-16",   "2010-14",  "2014-16"),
    ("2014-16 → 2016-19+",  "2014-16",  "2016-19+"),
]


def precision_at_k(G_a, G_b, scorer):
    """Predict links among nodes common to both periods; K = number of
    realized new edges among common nodes."""
    common = sorted(set(G_a.nodes()) & set(G_b.nodes()))
    S = G_a.subgraph(common)
    new_edges = {frozenset(e) for e in G_b.subgraph(common).edges()
                 if not S.has_edge(*e)}
    K = len(new_edges)
    if K == 0:
        return 0, 0.0, 0.0
    cands = [(u, v) for i, u in enumerate(common) for v in common[i + 1:]
             if not S.has_edge(u, v)]
    scores = sorted(((scorer(S, u, v), u, v) for u, v in cands), reverse=True)
    hits = sum(1 for s, u, v in scores[:K] if frozenset((u, v)) in new_edges)
    baseline = K / len(cands)
    return K, hits / K, baseline


def jaccard(S, u, v):
    a, b = set(S.neighbors(u)), set(S.neighbors(v))
    return len(a & b) / len(a | b) if (a | b) else 0.0


def resource_allocation(S, u, v):
    return sum(1 / S.degree(w) for w in set(S.neighbors(u)) & set(S.neighbors(v)))


def preferential_attachment(S, u, v):
    return S.degree(u) * S.degree(v)


if __name__ == "__main__":
    print(f"{'Transition':<22}{'K':>4}{'Jaccard':>9}{'RA':>7}{'PA':>7}{'baseline':>10}")
    for label, a, b in TRANSITIONS:
        G_a, G_b = load(a), load(b)
        K, pj, base = precision_at_k(G_a, G_b, jaccard)
        _, pr, _ = precision_at_k(G_a, G_b, resource_allocation)
        _, pp, _ = precision_at_k(G_a, G_b, preferential_attachment)
        print(f"{label:<22}{K:>4}{pj:>9.3f}{pr:>7.3f}{pp:>7.3f}{base:>10.4f}")
