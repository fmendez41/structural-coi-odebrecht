"""Table 10 + Figure 15 (fig09_group_dependence_Gch4) — P2b institutional
capture: group path dependence in the 2016-19+ (v2) network."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from coi_lib import ROOT, load, group_path_dependence, knockout, NHMN_EGO

GROUPS = [
    ("NHMN (alone)",            ["NHMN"]),
    ("NHMN ego-cluster (6)",    sorted(NHMN_EGO)),
    ("FGN (alone)",             ["FGN"]),
    ("NHMN + firms + FGN (7)",  sorted(NHMN_EGO) + ["FGN"]),
    ("Cúpula Aval (LCSA+GAVAL+CFC)", ["LCSA", "GAVAL", "CFC"]),
    ("ConsRS",                  ["ConsRS"]),
    ("Odebrecht (node)",        ["Odebrecht"]),
    ("GabrielGarciaM",          ["GabrielGarciaM"]),
    ("OttoB",                   ["OttoB"]),
]

if __name__ == "__main__":
    G = load("2016-19+ v2")
    results = []
    print(f"{'Group':<32}{'pairs fully dep.':>18}{'instances':>12}")
    for label, nodes in GROUPS:
        present = [n for n in nodes if n in G]
        pd_, inst = group_path_dependence(G, present)
        results.append((label, inst))
        print(f"{label:<32}{pd_:>16.1f}%{inst:>11.1f}%")

    # Joint-removal effect of the headline construct
    joint = sorted(NHMN_EGO) + ["FGN"]
    dd, de, _ = knockout(G, [n for n in joint if n in G])
    print(f"\nJoint removal {{NHMN+firms+FGN}}: Δ dist {dd:+.1f}%, Δ eff {de:+.1f}%")

    # Figure
    results.sort(key=lambda r: r[1])
    labels = [r[0] for r in results]
    vals = [r[1] for r in results]
    colors = ["#B8860B" if "NHMN" in l or "FGN" in l else "#7F8C8D"
              for l in labels]
    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    ax.barh(labels, vals, color=colors, alpha=0.9)
    for i, v in enumerate(vals):
        ax.text(v + 0.6, i, f"{v:.1f}%", va="center", fontsize=9)
    ax.set_xlabel("Share of Aval+ODB → Estado shortest-path instances traversed (%)")
    ax.set_title("P2b — institutional capture, 2016–19+ network (v2)", fontsize=11)
    ax.grid(axis="x", alpha=0.25)
    plt.tight_layout()
    out = os.path.join(ROOT, "outputs", "figures", "fig09_group_dependence_Gch4.png")
    plt.savefig(out, dpi=280, bbox_inches="tight", facecolor="white")
    print(f"\n✓ {out}")
