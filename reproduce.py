"""Run the released analysis scripts and preserve their printed tables.

This wrapper does not implement scientific calculations. It invokes each supplied
script in a clean subprocess and writes its standard output to outputs/tables/.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
TABLES = ROOT / "outputs" / "tables"

JOBS = [
    ("01_overview_metrics.py", "table02_network_overview.txt"),
    ("02_detection_coi.py", "table03_detection_coi.txt"),
    ("03_p1_trajectory.py", "table04_p1_trajectory.txt"),
    ("04_p2_knockout.py", "table05_p2_knockout.txt"),
    ("05_p3_group_betweenness.py", "table06_p3_group_betweenness.txt"),
    ("06_p4_ego_stability.py", "table07_p4_ego_stability.txt"),
    ("07_p5_vehicle_accretion.py", "table08_p5_vehicle_accretion.txt"),
    ("08_p2b_group_dependence.py", "table10_p2b_group_dependence.txt"),
    ("09_p6_suppression.py", "table11_p6_suppression.txt"),
    ("10_link_prediction.py", "table12_link_prediction.txt"),
    ("11_conduit_facilitator.py", "table09_conduit_facilitator.txt"),
    ("12_network_figures.py", "network_figures_generation.txt"),
]


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    child_env = os.environ.copy()
    child_env["PYTHONIOENCODING"] = "utf-8"
    child_env["PYTHONUTF8"] = "1"
    for script_name, log_name in JOBS:
        script = SRC / script_name
        print(f"Running {script_name} ...", flush=True)
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=child_env,
        )
        clean_stdout = result.stdout.replace(str(ROOT), ".")
        (TABLES / log_name).write_text(clean_stdout, encoding="utf-8")
        if result.stderr:
            sys.stderr.write(result.stderr)
    print("Reproduction completed successfully.")


if __name__ == "__main__":
    main()

