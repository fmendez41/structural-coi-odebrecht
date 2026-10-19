"""Table 3 — target-agnostic dual-exposure structural-risk ranking.

The score is computed for every person node. It measures documented
public/private exposure, not the presence of a legal conflict of interest.
"""
from coi_lib import load_all, coi_ranking

if __name__ == "__main__":
    for name, G in load_all(v2=True).items():
        print(f"\n=== {name} ===")
        ranking = coi_ranking(G)
        for rank, (coi, n, ep, epr) in enumerate(ranking[:5], 1):
            mark = "  ←" if n == "NHMN" else ""
            print(f"  {rank}. {n:<22} COI={coi:5.2f}  (E_pub={ep}, E_priv={epr}){mark}")
        # Report ties explicitly rather than resolving them by node order.
        for rank, (coi, n, ep, epr) in enumerate(ranking, 1):
            if n == "NHMN" and rank > 5:
                first = 1 + sum(row[0] > coi for row in ranking)
                last = sum(row[0] >= coi for row in ranking)
                tie = f"tied ranks {first}–{last}" if first != last else f"rank {first}"
                print(f"  …NHMN exposure={coi:.2f} ({tie}; E_pub={ep}, E_priv={epr})")
        if len(ranking) >= 2 and ranking[0][1] == "NHMN":
            print(f"  margin over runner-up: {ranking[0][0]/ranking[1][0]:.1f}x")
