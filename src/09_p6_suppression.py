"""Table 11 and figure — P6 exploratory non-edge anomaly diagnostic.

Resource Allocation is evaluated over all unconnected dyads in the
2016-19+ (v2) network. Tied scores are reported as rank ranges because their
internal ordering carries no information about suppression or protection.
"""
import os
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import networkx as nx
import numpy as np

from coi_lib import ROOT, load, resource_allocation_ranking, NHMN_EGO

WATCH = [("FGN", "Odebrecht"), ("FGN", "CSJ"), ("FGN", "CFC"),
         ("FGN", "Episol"), ("FGN", "JEPizano"), ("FGN", "LCSA"),
         ("FGN", "LCSG"), ("OttoB", "Odebrecht")]

if __name__ == "__main__":
    G = load("2016-19+ v2")
    ranking = resource_allocation_ranking(G)
    print(f"Unconnected dyads: {len(ranking)}")
    score_counts = Counter(row[0] for row in ranking)
    score_ranges = {}
    first = 1
    for score in sorted(score_counts, reverse=True):
        last = first + score_counts[score] - 1
        score_ranges[score] = (first, last)
        first = last + 1
    index = {}
    for ra, u, v, cn in ranking:
        first, last = score_ranges[ra]
        index[frozenset((u, v))] = (first, last, ra, cn)

    print(f"\n{'Dyad':<24}{'rank / tie range':>20}{'RA':>8}{'common nbrs':>13}")
    for u, v in WATCH:
        key = frozenset((u, v))
        if key in index:
            first, last, ra, cn = index[key]
            rank_label = f"{first}" if first == last else f"{first}–{last}"
            print(f"{u+'—'+v:<24}{rank_label:>20}{ra:>8.3f}{cn:>13}")
        elif G.has_edge(u, v):
            print(f"{u+'—'+v:<24}   (edge exists)")

    # Distance FGN–LCSG
    try:
        d = nx.shortest_path_length(G, "FGN", "LCSG")
        print(f"\nFGN–LCSG distance: {d}")
    except nx.NetworkXNoPath:
        print("\nFGN–LCSG: no path")

    # Figure: FGN neighborhood with dashed unrealized dyads
    key_nodes = {"FGN", "CFC", "LCSA", "LCSG", "Episol", "JEPizano", "CSJ",
                 "NHMN", "GAVAL"}
    nodes = {"FGN"} | set(G.neighbors("FGN")) | (key_nodes & set(G.nodes()))
    H = G.subgraph(nodes).copy()
    pos = nx.spring_layout(H, k=2.8 / np.sqrt(len(H)), seed=7, iterations=300)
    bc = nx.betweenness_centrality(G)

    BLOC_COLORS = {"Estado": "#2166AC", "Aval": "#D6191C",
                   "Odebrecht": "#1A9641", "NHMN": "#B8860B",
                   "Politicos": "#7B3294", "Intermediarios": "#8C510A",
                   "Offshore": "#C51B7D", "Proyecto": "#878787",
                   "Solarte": "#808000", "Contexto": "#018571"}
    fig, ax = plt.subplots(figsize=(14.2, 10.6))
    nx.draw_networkx_edges(H, pos, ax=ax, edge_color="#AAAAAA",
                           width=0.8, alpha=0.65)
    for u, v in WATCH:
        key = frozenset((u, v))
        if u in pos and v in pos and key in index:
            first, last, ra, _ = index[key]
            x, y = [pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]]
            ax.plot(x, y, "r--", lw=1.6, alpha=0.75, zorder=2)
            rank_label = (f"rank {first:,}" if first == last
                          else ("RA=0 tie" if ra == 0
                                else f"tie {first:,}–{last:,}"))
            ax.annotate(rank_label, ((x[0]+x[1])/2, (y[0]+y[1])/2),
                        fontsize=8.5, color="#B00000", fontweight="bold",
                        ha="center", zorder=5,
                        path_effects=[pe.withStroke(linewidth=2.5,
                                                    foreground="white")])
    bvals = np.array([bc[n] for n in H.nodes()])
    bmin, bmax = bvals.min(), max(bvals.max(), 1e-9)
    ax.scatter([pos[n][0] for n in H.nodes()], [pos[n][1] for n in H.nodes()],
               s=[110 + 1300*(bc[n]-bmin)/(bmax-bmin) for n in H.nodes()],
               c=[BLOC_COLORS.get(H.nodes[n].get("bloque"), "#555")
                  for n in H.nodes()],
               edgecolors=["black" if n in NHMN_EGO else "white"
                           for n in H.nodes()],
               linewidths=[2.6 if n in NHMN_EGO else 0.7 for n in H.nodes()],
               zorder=3, alpha=0.92)
    for n in H.nodes():
        if n == "NHMN":
            ax.annotate("NHMN", pos[n], fontsize=16, fontweight="bold",
                        ha="center", zorder=7, xytext=(0, 15),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round,pad=0.32",
                                  facecolor="#FFE9A8", edgecolor="black",
                                  linewidth=1.6, alpha=0.98))
        else:
            ax.annotate(n, pos[n], fontsize=8.2, ha="center", zorder=4,
                        xytext=(0, 8), textcoords="offset points",
                        path_effects=[pe.withStroke(linewidth=2.8,
                                                    foreground="white")])
    ax.set_title("Exploratory non-edge anomalies — FGN neighborhood, 2016–2019+ (v2)\n",
                 fontsize=14, fontweight="bold")
    ax.axis("off")
    plt.tight_layout()
    out = os.path.join(ROOT, "outputs", "figures", "fig10_suppression_Gch4.png")
    plt.savefig(out, dpi=280, bbox_inches="tight", facecolor="white")
    print(f"\n✓ {out}")
