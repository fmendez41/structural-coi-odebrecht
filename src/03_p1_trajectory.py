"""Table 4 and trajectory figure — P1 structural broker position."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from coi_lib import (ROOT, load_all, betweenness_profile,
                     participation_coefficient, coi_ranking)

if __name__ == "__main__":
    rows = []
    for name, G in load_all(v2=True).items():
        bc, pct, rank, npers = betweenness_profile(G, "NHMN")
        p = participation_coefficient(G, "NHMN")
        ranking = coi_ranking(G)
        coi = next(c for c, n, _, _ in ranking if n == "NHMN")
        rank_first = 1 + sum(row[0] > coi for row in ranking)
        rank_last = sum(row[0] >= coi for row in ranking)
        rows.append((name, G.degree("NHMN"), bc, pct, p, coi,
                     rank_first, rank_last, npers))
        rank_label = (str(rank_first) if rank_first == rank_last
                      else f"{rank_first}–{rank_last} tie")
        print(f"{name:<14} k={G.degree('NHMN'):>3}  C_B={bc:.4f}  "
              f"pct={pct:5.1f}  P={p:.3f}  exposure={coi:.2f} "
              f"(rank {rank_label}/{npers})")

    # Figure: two panels (COI trajectory; betweenness pct + participation)
    periods = [r[0].replace(" v2", "\n(v2)") for r in rows]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.2))
    ax = axes[0]
    ax.plot(range(4), [r[5] for r in rows], "o-", color="#B8860B", lw=2.2, ms=7)
    for i, r in enumerate(rows):
        label = (f"rank {r[6]}" if r[6] == r[7]
                 else f"tied {r[6]}–{r[7]}")
        ax.annotate(label, (i, r[5]), xytext=(0, 10),
                    textcoords="offset points", ha="center", fontsize=8.5)
    ax.set_xticks(range(4)); ax.set_xticklabels(periods, fontsize=9)
    ax.set_ylabel("Dual-exposure structural COI-risk score")
    ax.set_title("(a) Stage 1 — target-agnostic exposure ranking", fontsize=10.5)
    ax.grid(alpha=0.25)

    ax = axes[1]
    ax.plot(range(4), [r[3] for r in rows], "o-", color="#E07B00", lw=2.2,
            ms=7, label="betweenness percentile")
    ax.set_ylabel("Betweenness percentile", color="#E07B00")
    ax2 = ax.twinx()
    ax2.plot(range(4), [r[4] for r in rows], "s--", color="#2166AC", lw=2.2,
             ms=7, label="participation coefficient")
    ax2.set_ylabel("Participation coefficient", color="#2166AC")
    ax.set_xticks(range(4)); ax.set_xticklabels(periods, fontsize=9)
    ax.set_title("(b) Stage 2 — structural broker position (P1)", fontsize=10.5)
    ax.grid(alpha=0.25)
    plt.tight_layout()
    out = os.path.join(ROOT, "outputs", "figures", "fig06_nhmn_trajectory.png")
    plt.savefig(out, dpi=280, bbox_inches="tight", facecolor="white")
    print(f"\n✓ {out}")
