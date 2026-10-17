"""Table 6 — P3 group-restricted betweenness (Aval ∪ Odebrecht → Estado):
share of inter-bloc shortest-path instances mediated by each actor, per period.
Also used for the conduit/facilitator contrast (NHMN vs OttoB)."""
from coi_lib import load_all, group_restricted_betweenness

ACTORS = ["NHMN", "OttoB", "GabrielGarciaM", "FGN", "RS-SII"]

if __name__ == "__main__":
    for name, G in load_all(v2=True).items():
        print(f"\n=== {name} ===")
        for a in ACTORS:
            if a not in G:
                continue
            share = group_restricted_betweenness(G, a)
            print(f"  {a:<16} {100*share:5.1f}% of Aval+ODB → Estado shortest paths")
