"""Table 5 + Figure 11 (fig07_knockout_Gch3) — P2 comparative knockout
on the 2014-16 (v2) network: Δ inter-bloc distance and Δ efficiency
for NHMN, his ego-cluster, and a panel of comparable actors."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from coi_lib import ROOT, load, knockout, NHMN_EGO

CANDIDATES = [
    ("NHMN (alone)",          ["NHMN"]),
    ("NHMN ego-cluster (6)",  sorted(NHMN_EGO)),
    ("GabrielGarciaM",        ["GabrielGarciaM"]),
    ("BernardoNElias",        ["BernardoNElias"]),
    ("JEliasMelo",            ["JEliasMelo"]),
    ("LuizBueno",             ["LuizBueno"]),
    ("LCSA",                  ["LCSA"]),
    ("LuisFAndrade",          ["LuisFAndrade"]),
    ("OttoB",                 ["OttoB"]),
    ("RobertoPrieto",         ["RobertoPrieto"]),
]

if __name__ == "__main__":
    G = load("2014-16 v2")
    results = []
    print(f"{'Removed':<24}{'Δ dist':>9}{'Δ eff':>9}{'components':>12}")
    for label, nodes in CANDIDATES:
        present = [n for n in nodes if n in G]
        if not present:
            print(f"{label:<24}  (not in network)")
            continue
        dd, de, ncomp = knockout(G, present)
        results.append((label, dd))
        print(f"{label:<24}{dd:>+8.1f}%{de:>+8.2f}%{ncomp:>12}")

    # Figure: horizontal bar chart of Δ inter-bloc distance
    results.sort(key=lambda r: r[1])
    labels = [r[0] for r in results]
    vals = [r[1] for r in results]
    colors = ["#B8860B" if "NHMN" in l else
              "#C0392B" if l == "LCSA" else "#7F8C8D" for l in labels]
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    ax.barh(labels, vals, color=colors, alpha=0.9)
    for i, v in enumerate(vals):
        ax.text(v + 0.15, i, f"+{v:.1f}%", va="center", fontsize=9)
    ax.set_xlabel("Δ mean geodesic distance, Aval+ODB → Estado (%)")
    ax.set_title("Comparative knockout — 2014–16 network (v2)", fontsize=11)
    ax.grid(axis="x", alpha=0.25)
    plt.tight_layout()
    out = os.path.join(ROOT, "outputs", "figures", "fig07_knockout_Gch3.png")
    plt.savefig(out, dpi=280, bbox_inches="tight", facecolor="white")
    print(f"\n✓ {out}")
