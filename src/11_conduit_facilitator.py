"""Table 9 and comparison figure — Otto Bula (conduit) versus NHMN
(persistent structural broker) on exposure trajectory, inter-bloc path share,
node-removal effects, and neighbor composition."""
import os
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from coi_lib import (ROOT, load_all, coi_index, betweenness_profile,
                     group_restricted_betweenness, knockout)

if __name__ == "__main__":
    nets = load_all(v2=True)
    coi = {"NHMN": [], "OttoB": []}
    grb = {"NHMN": [], "OttoB": []}

    for name, G in nets.items():
        print(f"\n=== {name} ===")
        for a in ("OttoB", "NHMN"):
            c, ep, epr = coi_index(G, a)
            coi[a].append(c)
            bc, pct, rank, npers = betweenness_profile(G, a)
            share = group_restricted_betweenness(G, a)
            grb[a].append(100 * share)
            dd, de, _ = knockout(G, [a])
            print(f"  {a:<7} exposure={c:5.2f} (pub={ep},priv={epr})  "
                  f"bc pct={pct:5.1f} (rank {rank}/{npers})  "
                  f"inter-bloc share={100*share:5.1f}%  knockout Δdist={dd:+.1f}%")

    # Neighbor composition of OttoB at his peak (2010-14)
    G2 = nets["2010-14"]
    blocs = Counter(G2.nodes[n].get("bloque") for n in G2.neighbors("OttoB"))
    print(f"\nOttoB neighbors in 2010-14 by bloc: {dict(blocs)}")

    # Figure: two panels
    periods = ["pre-2010", "2010–14", "2014–16\n(v2)", "2016–19+\n(v2)"]
    GOLD, PURPLE = "#B8860B", "#7B2D8E"
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.2))
    ax = axes[0]
    ax.plot(range(4), coi["NHMN"], "o-", color=GOLD, lw=2.2, ms=7,
            label="NHMN (structural broker)")
    ax.plot(range(4), coi["OttoB"], "s--", color=PURPLE, lw=2.2, ms=7,
            label="OttoB (conduit)")
    ax.set_xticks(range(4)); ax.set_xticklabels(periods, fontsize=9)
    ax.set_ylabel("Dual-exposure structural COI-risk score")
    ax.set_title("(a) Exposure trajectory: peak-and-decay vs. monotonic ascent",
                 fontsize=10.5)
    ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.25)

    ax = axes[1]
    ax.plot(range(4), grb["NHMN"], "o-", color=GOLD, lw=2.2, ms=7, label="NHMN")
    ax.plot(range(4), grb["OttoB"], "s--", color=PURPLE, lw=2.2, ms=7,
            label="OttoB")
    ax.set_xticks(range(4)); ax.set_xticklabels(periods, fontsize=9)
    ax.set_ylabel("Share of Aval+ODB → Estado\nshortest paths mediated (%)")
    ax.set_title("(b) Inter-bloc brokerage (group-restricted betweenness)",
                 fontsize=10.5)
    ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.25)
    plt.tight_layout()
    out = os.path.join(ROOT, "outputs", "figures", "fig12_conduit_facilitator.png")
    plt.savefig(out, dpi=280, bbox_inches="tight", facecolor="white")
    print(f"\n✓ {out}")
