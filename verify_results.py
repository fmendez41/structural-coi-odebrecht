"""Check the manuscript's headline numerical results against released data."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from coi_lib import (  # noqa: E402
    NHMN_EGO,
    coi_ranking,
    ego_jaccard_split,
    group_path_dependence,
    jaccard_retention,
    knockout,
    load,
    load_all,
    modularity_louvain,
    participation_coefficient,
    resource_allocation_ranking,
    subset_betweenness_profile,
    unified_firm_clientele,
)


failures: list[str] = []


def check(label: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{label}: expected {expected!r}, got {actual!r}")


check("NetworkX version", nx.__version__, "3.4.2")

nets = load_all(v2=True)
check("period sizes", [(g.number_of_nodes(), g.number_of_edges()) for g in nets.values()],
      [(73, 128), (130, 243), (109, 225), (116, 283)])

q_2014, _ = modularity_louvain(nets["2014-16 v2"])
check("2014-16 modularity", round(q_2014, 3), 0.505)
check("2014-16 participation", round(participation_coefficient(
    nets["2014-16 v2"], "NHMN"), 3), 0.720)

ranking_2014 = coi_ranking(nets["2014-16 v2"])
ranking_2016 = coi_ranking(nets["2016-19+ v2"])
check("2014-16 exposure leader", ranking_2014[0][1], "NHMN")
check("2014-16 exposure score", round(ranking_2014[0][0], 2), 6.00)
check("2014-16 exposure margin", round(ranking_2014[0][0] / ranking_2014[1][0], 1), 2.1)
check("2016-19 exposure score", round(ranking_2016[0][0], 2), 7.35)

g_2014 = nets["2014-16 v2"]
dd_actor, de_actor, _ = knockout(g_2014, ["NHMN"])
dd_cluster, de_cluster, _ = knockout(g_2014, sorted(NHMN_EGO))
check("P2 NHMN distance", round(dd_actor, 1), 11.4)
check("P2 cluster distance", round(dd_cluster, 1), 13.1)
check("P2 NHMN efficiency", round(de_actor, 2), -4.01)
check("P2 cluster efficiency", round(de_cluster, 2), -4.67)

expected_subset = {
    "pre-2010": 0.0059,
    "2010-14": 0.0085,
    "2014-16 v2": 0.0224,
    "2016-19+ v2": 0.0187,
}
for period, expected in expected_subset.items():
    value, _, _, _ = subset_betweenness_profile(nets[period], "NHMN")
    check(f"P3 subset betweenness {period}", round(value, 4), expected)

expected_p4 = [(0.60, 0.00, None), (0.90, 0.00, 0.00), (1.00, 0.40, 0.50)]
period_names = list(nets)
actual_p4 = []
for earlier, later in zip(period_names, period_names[1:]):
    row = ego_jaccard_split(nets[earlier], nets[later], "NHMN")
    actual_p4.append(tuple(None if row[key] is None else round(row[key], 2)
                           for key in ("priv", "trans", "const")))
check("P4 sphere-split Jaccard", actual_p4, expected_p4)

clienteles = [unified_firm_clientele(g) for g in nets.values()]
p5_jaccard = [round(jaccard_retention(a, b)[0], 3)
              for a, b in zip(clienteles, clienteles[1:])]
check("P5 clientele Jaccard", p5_jaccard, [0.286, 0.778, 1.000])

g_2016 = nets["2016-19+ v2"]
joint = set(NHMN_EGO) | {"FGN"}
pairs, instances = group_path_dependence(g_2016, joint)
check("P2b fully dependent pairs", round(pairs, 1), 37.8)
check("P2b path instances", round(instances, 1), 56.2)

ra_rows = resource_allocation_ranking(g_2016)
ra_index = {frozenset((u, v)): (rank, ra, common)
            for rank, (ra, u, v, common) in enumerate(ra_rows, 1)}
check("P6 FGN-CFC rank", ra_index[frozenset(("FGN", "CFC"))][0], 8)
check("P6 non-edge count", len(ra_rows), 6387)
check("P6 FGN-LCSG RA", ra_index[frozenset(("FGN", "LCSG"))][1], 0)
check("P6 FGN-LCSG common neighbors",
      ra_index[frozenset(("FGN", "LCSG"))][2], 0)
check("P6 FGN-LCSG distance", nx.shortest_path_length(g_2016, "FGN", "LCSG"), 3)

if failures:
    print("Verification failed:")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("All headline numerical checks passed.")
