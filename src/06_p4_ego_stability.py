"""Table 7 + Figure 12 (fig08_ego_stability) — P4 persistence with the
pre-registered sphere split: Jaccard stability of NHMN's ego network
between consecutive periods (private / public-transactional / public-constitutive)."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from coi_lib import ROOT, load, ego_jaccard_split

TRANSITIONS = [
    ("pre-2010 → 2010-14",   "pre-2010",   "2010-14"),
    ("2010-14 → 2014-16",    "2010-14",    "2014-16 v2"),
    ("2014-16 → 2016-19+",   "2014-16 v2", "2016-19+ v2"),
]

if __name__ == "__main__":
    series = {"priv": [], "trans": [], "const": []}
    print(f"{'Transition':<22}{'J priv':>8}{'J trans':>9}{'J const':>9}")
    for label, a, b in TRANSITIONS:
        res = ego_jaccard_split(load(a), load(b), "NHMN")
        fmt = lambda v: f"{v:.2f}" if v is not None else "  — "
        print(f"{label:<22}{fmt(res['priv']):>8}{fmt(res['trans']):>9}"
              f"{fmt(res['const']):>9}")
        for k in series:
            series[k].append(res[k] if res[k] is not None else float("nan"))

    labels = [t[0] for t in TRANSITIONS]
    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    ax.plot(range(3), series["priv"], "o-", color="#D6191C", lw=2.2, ms=8,
            label="private sphere")
    ax.plot(range(3), series["trans"], "s-", color="#2166AC", lw=2.2, ms=8,
            label="public — transactional")
    ax.plot(range(3), series["const"], "^--", color="#1A9641", lw=2.2, ms=8,
            label="public — constitutive (CSJ, FGN, FGNAdhoc)")
    ax.set_xticks(range(3)); ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Jaccard stability of ego neighborhood")
    ax.set_ylim(-0.05, 1.08)
    ax.set_title("P4 — sphere-split ego stability of the facilitator (v2)",
                 fontsize=11)
    ax.legend(fontsize=9); ax.grid(alpha=0.25)
    plt.tight_layout()
    out = os.path.join(ROOT, "outputs", "figures", "fig08_ego_stability.png")
    plt.savefig(out, dpi=280, bbox_inches="tight", facecolor="white")
    print(f"\n✓ {out}")
