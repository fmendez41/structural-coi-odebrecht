"""Table 2 — Period networks: nodes, edges, density, entropies, clustering, modularity."""
import networkx as nx
from coi_lib import load_all, degree_entropy, modularity_louvain
import math
import numpy as np


def centrality_entropy(G, bins=10):
    bc = list(nx.betweenness_centrality(G).values())
    hist, _ = np.histogram(bc, bins=bins)
    n = sum(hist)
    return -sum((c / n) * math.log2(c / n) for c in hist if c)


if __name__ == "__main__":
    print(f"{'Network':<14}{'n':>5}{'m':>6}{'density':>9}{'H_deg':>7}"
          f"{'H_cent':>8}{'<C>':>7}{'Q':>7}")
    for name, G in load_all(v2=True).items():
        q, _ = modularity_louvain(G)
        print(f"{name:<14}{G.number_of_nodes():>5}{G.number_of_edges():>6}"
              f"{nx.density(G):>9.4f}{degree_entropy(G):>7.3f}"
              f"{centrality_entropy(G):>8.3f}"
              f"{nx.average_clustering(G):>7.3f}{q:>7.3f}")
