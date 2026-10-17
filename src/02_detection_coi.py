"""Table 3 — Stage 1 unsupervised detection: dual-exposure COI index,
person nodes only, per period. Top-5 shown; NHMN highlighted."""
from coi_lib import load_all, coi_ranking

if __name__ == "__main__":
    for name, G in load_all(v2=True).items():
        print(f"\n=== {name} ===")
        ranking = coi_ranking(G)
        for rank, (coi, n, ep, epr) in enumerate(ranking[:5], 1):
            mark = "  ←" if n == "NHMN" else ""
            print(f"  {rank}. {n:<22} COI={coi:5.2f}  (E_pub={ep}, E_priv={epr}){mark}")
        # NHMN's rank if not in top-5
        for rank, (coi, n, ep, epr) in enumerate(ranking, 1):
            if n == "NHMN" and rank > 5:
                print(f"  …{rank}. NHMN COI={coi:.2f} (E_pub={ep}, E_priv={epr})")
        if len(ranking) >= 2 and ranking[0][1] == "NHMN":
            print(f"  margin over runner-up: {ranking[0][0]/ranking[1][0]:.1f}x")
