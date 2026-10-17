"""Figures 1–9 + Appendix A1–A5 — network diagrams and ego views.

Hierarchical labelling convention (uniform across all plots):
  - NHMN: large gold box, black border; node 35% larger.
  - Rest of the NHMN ego-cluster (firms + son): smaller gold boxes.
  - OttoB: pink box.
  - Curated key actors + top-12 betweenness: plain label with white halo.
  - Peripheral nodes: unlabeled in main-text figures; ALL nodes are
    labeled in the full-page appendix versions (figA01–figA05).
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D

from coi_lib import ROOT, PATHS, NHMN_EGO

FIGDIR = os.path.join(ROOT, "outputs", "figures")

BLOC_COLORS = {"Estado": "#2166AC", "Aval": "#D6191C", "Odebrecht": "#1A9641",
               "NHMN": "#B8860B", "Politicos": "#7B3294",
               "Intermediarios": "#8C510A", "Offshore": "#C51B7D",
               "Proyecto": "#878787", "Solarte": "#808000",
               "Contexto": "#018571"}
TYPE_MARKERS = {"persona": "o", "institucion": "s", "empresa": "^",
                "vehiculo": "v", "objeto": "D", "evento": "D"}
GOLD, PINK = "#FFE9A8", "#F3D1E5"

CURATED = {"NHMN", "OttoB", "LCSA", "LCSG", "GAVAL", "CFC", "FGN", "FGNAdhoc",
           "CSJ", "Odebrecht", "ConstODB", "ConsRS", "Episol",
           "GabrielGarciaM", "JEPizano", "MNA", "M&MACLtda",
           "EstudioJuridicoMNALtda", "NHMAbogados", "ANI", "INCO",
           "Presidencia", "MinTransporte", "JMSantos", "RobertoPrieto",
           "FedericoGaviria", "LuizBueno", "MODB", "C-NVLN", "Terna2016",
           "DemandaNulidad2019", "Lurion", "JEliasMelo", "GNC", "Fiduciaria"}


def label_node(ax, n, xy, full=False):
    if n == "NHMN":
        ax.annotate("NHMN", xy, fontsize=17, fontweight="bold", ha="center",
                    va="center", zorder=7, xytext=(0, 16),
                    textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.32", facecolor=GOLD,
                              edgecolor="black", linewidth=1.6, alpha=0.98))
    elif n in NHMN_EGO:
        ax.annotate(n, xy, fontsize=9.5, fontweight="bold", ha="center",
                    va="center", zorder=6, xytext=(0, 11),
                    textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor=GOLD,
                              edgecolor="black", linewidth=1.1, alpha=0.96))
    elif n == "OttoB":
        ax.annotate("OttoB", xy, fontsize=12, fontweight="bold", ha="center",
                    va="center", zorder=6, xytext=(0, 13),
                    textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor=PINK,
                              edgecolor="#C51B7D", linewidth=1.2, alpha=0.96))
    else:
        fs = 5.6 if full else 8.5
        ax.annotate(n, xy, fontsize=fs, ha="center", va="center", zorder=4,
                    xytext=(0, 6 if full else 8), textcoords="offset points",
                    path_effects=[pe.withStroke(linewidth=2.8,
                                                foreground="white")])


def draw_network(G, title, subtitle, outpath, full_labels=False,
                 max_labels=20):
    bc = nx.betweenness_centrality(G)
    pos = nx.spring_layout(G, k=2.2 / np.sqrt(len(G)), seed=42,
                           iterations=200)
    fig, ax = plt.subplots(figsize=(16.5, 11.7) if full_labels
                           else (15.9, 11.9))
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#BBBBBB", width=0.55,
                           alpha=0.6)
    bvals = np.array(list(bc.values()))
    bmin, bmax = bvals.min(), max(bvals.max(), 1e-9)

    def size_of(n):
        s = 60 + 1400 * (bc[n] - bmin) / (bmax - bmin)
        return s * (1.35 if n == "NHMN" else 1.0)

    for tipo, marker in TYPE_MARKERS.items():
        nn = [n for n, d in G.nodes(data=True) if d.get("tipo") == tipo]
        if not nn:
            continue
        ax.scatter([pos[n][0] for n in nn], [pos[n][1] for n in nn],
                   s=[size_of(n) for n in nn],
                   c=[BLOC_COLORS.get(G.nodes[n].get("bloque"), "#555")
                      for n in nn],
                   marker=marker,
                   edgecolors=["black" if n in NHMN_EGO else "white"
                               for n in nn],
                   linewidths=[2.6 if n in NHMN_EGO else 0.7 for n in nn],
                   zorder=3, alpha=0.92)

    forced = (NHMN_EGO | {"OttoB"}) & set(G.nodes())
    if full_labels:
        to_label = set(G.nodes())
    else:
        top = sorted(G.nodes(), key=lambda n: bc[n], reverse=True)[:12]
        pool = (CURATED & set(G.nodes())) | set(top)
        to_label = set(sorted(pool, key=lambda n: bc[n],
                              reverse=True)[:max_labels]) | forced
    for n in to_label:
        label_node(ax, n, pos[n], full_labels)

    blocs = sorted({G.nodes[n].get("bloque") for n in G.nodes()} - {None})
    leg1 = ax.legend(handles=[Line2D([0], [0], marker="o", color="w",
                                     markerfacecolor=BLOC_COLORS.get(b, "#555"),
                                     markersize=9, label=b) for b in blocs],
                     loc="upper left", fontsize=8.5, title="Bloque (color)",
                     title_fontsize=9, framealpha=0.9)
    ax.add_artist(leg1)
    tipos = sorted({G.nodes[n].get("tipo") for n in G.nodes()} - {None})
    ax.legend(handles=[Line2D([0], [0], marker=TYPE_MARKERS.get(t, "o"),
                              color="w", markerfacecolor="#888", markersize=9,
                              label=t) for t in tipos],
              loc="lower left", fontsize=8.5, title="Tipo (forma)",
              title_fontsize=9, framealpha=0.9)
    ax.set_title(f"{title}\n", fontsize=15, fontweight="bold")
    ax.text(0.5, 1.005, subtitle, transform=ax.transAxes, ha="center",
            fontsize=10.5, style="italic", color="#444")
    note = (f"Node size = betweenness centrality · Gold boxes = NHMN "
            f"ego-cluster · Pink box = OttoB · n = {G.number_of_nodes()}, "
            f"m = {G.number_of_edges()}")
    if not full_labels:
        note += (" · peripheral nodes unlabeled for legibility "
                 "(full-label plots in Appendix)")
    ax.text(0.99, 0.005, note, transform=ax.transAxes, ha="right",
            fontsize=7, color="#666")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(outpath, dpi=280, bbox_inches="tight", facecolor="white")
    plt.savefig(outpath.replace(".png", ".pdf"), bbox_inches="tight",
                facecolor="white")
    plt.close()
    print(f"  ✓ {os.path.basename(outpath)}")


def draw_ego(gexf_key, seeds, title, subtitle, outpath):
    """Ego view: seeds + neighbors; NHMN ego-cluster always included."""
    G = nx.read_gexf(PATHS[gexf_key])
    bc = nx.betweenness_centrality(G)
    nodes = set()
    for s in seeds:
        if s in G:
            nodes.add(s)
            nodes.update(G.neighbors(s))
    nodes |= NHMN_EGO & set(G.nodes())
    H = G.subgraph(nodes).copy()
    pos = nx.spring_layout(H, k=2.6 / np.sqrt(len(H)), seed=42,
                           iterations=250)
    fig, ax = plt.subplots(figsize=(14.2, 10.1))
    se = [(u, v) for u, v in H.edges() if u in seeds or v in seeds]
    oe = [(u, v) for u, v in H.edges() if not (u in seeds or v in seeds)]
    nx.draw_networkx_edges(H, pos, ax=ax, edgelist=oe, edge_color="#CCCCCC",
                           width=0.5, alpha=0.55)
    nx.draw_networkx_edges(H, pos, ax=ax, edgelist=se, edge_color="#888888",
                           width=1.2, alpha=0.8)
    bvals = np.array([bc[n] for n in H.nodes()])
    bmin, bmax = bvals.min(), max(bvals.max(), 1e-9)
    for tipo, marker in TYPE_MARKERS.items():
        nn = [n for n in H.nodes() if H.nodes[n].get("tipo") == tipo]
        if not nn:
            continue
        ax.scatter([pos[n][0] for n in nn], [pos[n][1] for n in nn],
                   s=[(90 + 1500 * (bc[n] - bmin) / (bmax - bmin))
                      * (1.35 if n == "NHMN" else 1.0) for n in nn],
                   c=[BLOC_COLORS.get(H.nodes[n].get("bloque"), "#555")
                      for n in nn],
                   marker=marker,
                   edgecolors=["black" if n in NHMN_EGO else "white"
                               for n in nn],
                   linewidths=[2.6 if n in NHMN_EGO else 0.7 for n in nn],
                   zorder=3, alpha=0.92)
    for n in H.nodes():
        label_node(ax, n, pos[n])
    blocs = sorted({H.nodes[n].get("bloque") for n in H.nodes()} - {None})
    ax.legend(handles=[Line2D([0], [0], marker="o", color="w",
                              markerfacecolor=BLOC_COLORS.get(b, "#555"),
                              markersize=9, label=b) for b in blocs],
              loc="upper left", fontsize=8.5, title="Bloque",
              title_fontsize=9, framealpha=0.9)
    ax.set_title(f"{title}\n", fontsize=14, fontweight="bold")
    ax.text(0.5, 1.005, subtitle, transform=ax.transAxes, ha="center",
            fontsize=10, style="italic", color="#444")
    ax.text(0.99, 0.005, f"Gold boxes = NHMN ego-cluster · Pink box = OttoB "
            f"· n = {len(H)}, m = {H.number_of_edges()}",
            transform=ax.transAxes, ha="right", fontsize=7, color="#666")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(outpath, dpi=280, bbox_inches="tight", facecolor="white")
    plt.savefig(outpath.replace(".png", ".pdf"), bbox_inches="tight",
                facecolor="white")
    plt.close()
    print(f"  ✓ {os.path.basename(outpath)}")


NETS = [("pre-2010", "pre-2010 (Uribe era)",
         "adjudication of Ruta del Sol II", "fig01_network_Gch1"),
        ("2010-14", "2010–2014 (Santos I)",
         "legal-stability contract and Ocaña–Gamarra addition",
         "fig02_network_Gch2"),
        ("satellite", "2010–14 satellite",
         "Otto Bula offshore laundering circuit", "fig03_network_Gch2OttoB"),
        ("2014-16 v2", "2014–2016 (Santos II, v2)",
         "transaction, Navelena, and the crossing into office",
         "fig04_network_Gch3"),
        ("2016-19+ v2", "2016–2019+ (judicialization, v2)",
         "the facilitator as Attorney General", "fig05_network_Gch4")]

if __name__ == "__main__":
    print("Main-text network figures (selective labels):")
    for key, title, sub, fname in NETS:
        G = nx.read_gexf(PATHS[key])
        draw_network(G, title, sub, os.path.join(FIGDIR, fname + ".png"))

    print("\nEgo views:")
    draw_ego("2014-16 v2", ["Odebrecht", "ConstODB"],
             "2014–2016 — Odebrecht ego view",
             "seeds: Odebrecht, ConstODB; NHMN ego-cluster shown for reference",
             os.path.join(FIGDIR, "fig04a_ego_ODB_Gch3.png"))
    draw_ego("2014-16 v2", sorted(NHMN_EGO),
             "2014–2016 — NHMN ego-cluster view",
             "the shortlist and the Court enter the public side (v2)",
             os.path.join(FIGDIR, "fig04b_ego_NHMN_Gch3.png"))
    draw_ego("2016-19+ v2", sorted(NHMN_EGO),
             "2016–2019+ — NHMN ego-cluster view",
             "constitutive anchoring: CSJ, FGN, FGNAdhoc, nullity petition (v2)",
             os.path.join(FIGDIR, "fig05a_ego_NHMN_Gch4.png"))
    draw_ego("2016-19+ v2", ["Odebrecht", "ConstODB"],
             "2016–2019+ — Odebrecht ego view",
             "judicialization period; NHMN ego-cluster shown for reference",
             os.path.join(FIGDIR, "fig05b_ego_ODB_Gch4.png"))

    print("\nFull-label appendix plots (A1–A5):")
    for i, (key, title, sub, fname) in enumerate(NETS, 1):
        G = nx.read_gexf(PATHS[key])
        code = fname.split("_")[-1]
        draw_network(G, title + " — full labels", sub,
                     os.path.join(FIGDIR, f"figA{i:02d}_full_{code}.png"),
                     full_labels=True)
