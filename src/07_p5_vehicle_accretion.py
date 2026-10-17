"""Table 8 + Figure 13 (fig11_vehicle_accretion) — P5 instrumental accretion:
degree of each corporate vehicle per period, and stability of the unified
clientele (union of the firms' neighborhoods)."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from coi_lib import ROOT, load_all

FIRMS = ["M&MACLtda", "MNA", "EstudioJuridicoMNALtda", "NHMAbogados"]

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

    # Unified clientele: union of firm neighborhoods, retention across periods
    print("\nUnified clientele of the firms (union of neighborhoods):")
    prev = None
    for n in names:
        G = nets[n]
        cli = set()
        for f in FIRMS:
            if f in G:
                cli |= set(G.neighbors(f))
        cli -= set(FIRMS) | {"NHMN", "NCMH"}
        if prev is not None:
            common = set(G.nodes()) & prev_nodes
            a, b = prev & common, cli & common
            j = len(a & b) / len(a | b) if (a | b) else float("nan")
            ret = f"{len(a & b)}/{len(a)}" if a else "—"
            print(f"  {n:<14} |clientele|={len(cli):>2}  retention={ret}  Jaccard={j:.3f}")
        else:
            print(f"  {n:<14} |clientele|={len(cli):>2}")
        prev, prev_nodes = cli, set(G.nodes())

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
