"""Table 8 + Figure 13 (fig11_vehicle_accretion) — P5 instrumental accretion:
degree of each corporate vehicle per period, and stability of the unified
clientele (union of the firms' neighborhoods)."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from coi_lib import (ROOT, load_all, NHMN_FIRMS, unified_firm_clientele,
                     jaccard_retention)

FIRMS = ["M&MACLtda", "MNA", "EstudioJuridicoMNALtda", "NHMAbogados"]
assert set(FIRMS) == NHMN_FIRMS

if __name__ == "__main__":
    nets = load_all(v2=True)
    names = list(nets)

    print(f"{'Entity':<24}" + "".join(f"{n:>14}" for n in names))
    matrix = []
    for f in FIRMS + ["NHMN"]:
        row = [nets[n].degree(f) if f in nets[n] else None for n in names]
        matrix.append(row)
        print(f"{f:<24}" + "".join(
            f"{(str(v) if v is not None else '—'):>14}" for v in row))

    # Unified clientele: raw union of firm neighborhoods in each period.
    # New or disappearing nodes count in the Jaccard union; restricting to
    # nodes common to adjacent networks would inflate stability.
    print("\nUnified clientele of the firms (union of neighborhoods):")
    prev = None
    for n in names:
        G = nets[n]
        cli = unified_firm_clientele(G)
        if prev is not None:
            j, retained, previous_total = jaccard_retention(prev, cli)
            ret = f"{retained}/{previous_total}" if previous_total else "—"
            print(f"  {n:<14} |clientele|={len(cli):>2}  retention={ret}  Jaccard={j:.3f}")
        else:
            print(f"  {n:<14} |clientele|={len(cli):>2}")
        prev = cli

    # Figure: heatmap of vehicle degrees
    data = np.array([[v if v is not None else 0 for v in row]
                     for row in matrix], dtype=float)
    fig, ax = plt.subplots(figsize=(8.6, 4.5))
    im = ax.imshow(data, cmap="YlOrBr", aspect="auto")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels([n.replace(" v2", "\n(v2)") for n in names], fontsize=9)
    ax.set_yticks(range(len(FIRMS) + 1))
    ax.set_yticklabels(FIRMS + ["NHMN (person)"], fontsize=9)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            v = matrix[i][j]
            ax.text(j, i, str(v) if v is not None else "—", ha="center",
                    va="center", fontsize=10,
                    color="white" if data[i, j] > data.max() * 0.6 else "black")
    ax.set_title("P5 — instrumental accretion: vehicle degree per period",
                 fontsize=11)
    fig.colorbar(im, ax=ax, label="degree")
    plt.tight_layout()
    out = os.path.join(ROOT, "outputs", "figures", "fig11_vehicle_accretion.png")
    plt.savefig(out, dpi=280, bbox_inches="tight", facecolor="white")
    print(f"\n✓ {out}")
