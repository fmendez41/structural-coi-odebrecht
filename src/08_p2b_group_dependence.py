"""Table 10 and figure — P2b institutionalized brokerage measured as
group path dependence in the 2016-19+ (v2) network."""
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
        results.append((label, pd_, inst))
        print(f"{label:<32}{pd_:>16.1f}%{inst:>11.1f}%")

    # Joint-removal effect of the headline construct
    joint = sorted(NHMN_EGO) + ["FGN"]
    dd, de, _ = knockout(G, [n for n in joint if n in G])
    print(f"\nJoint removal {{NHMN+firms+FGN}}: Δ dist {dd:+.1f}%, Δ eff {de:+.1f}%")

    # Figure
    results.sort(key=lambda r: r[2])
    labels = [r[0] for r in results]
    dep_vals = [r[1] for r in results]
    inst_vals = [r[2] for r in results]
    colors = ["#B8860B" if "NHMN" in l or "FGN" in l else "#7F8C8D"
              for l in labels]
    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    y = list(range(len(labels)))
    ax.barh([i + 0.18 for i in y], inst_vals, height=0.34,
            color=colors, alpha=0.9, label="shortest-path instances")
    ax.barh([i - 0.18 for i in y], dep_vals, height=0.34,
            color="#555555", alpha=0.75, label="pairs fully dependent")
    ax.set_yticks(y); ax.set_yticklabels(labels)
    for i, (dep, inst) in enumerate(zip(dep_vals, inst_vals)):
        ax.text(inst + 0.5, i + 0.18, f"{inst:.1f}%", va="center", fontsize=8.5)
        ax.text(dep + 0.5, i - 0.18, f"{dep:.1f}%", va="center", fontsize=8.5)
    ax.set_xlabel("Share of Aval+ODB → Estado shortest-path instances traversed (%)")
    ax.set_title("P2b — institutionalized brokerage (group path dependence)",
                 fontsize=11)
    ax.legend(loc="lower right", fontsize=8.5)
    ax.grid(axis="x", alpha=0.25)
    plt.tight_layout()
    out = os.path.join(ROOT, "outputs", "figures", "fig09_group_dependence_Gch4.png")
    plt.savefig(out, dpi=280, bbox_inches="tight", facecolor="white")
    print(f"\n✓ {out}")
