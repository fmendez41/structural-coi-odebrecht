"""Table 6 — normalized P3 subset betweenness and network-wide rank."""
from coi_lib import load_all, subset_betweenness_profile

if __name__ == "__main__":
    for name, G in load_all(v2=True).items():
        value, rank, leader, leader_value = subset_betweenness_profile(G, "NHMN")
        shown = "below top-8" if rank > 8 else str(rank)
        print(
            f"{name:<14} NHMN C_B^S,T={value:.4f}  rank={shown:<11} "
            f"leader={leader} ({leader_value:.4f})"
        )
