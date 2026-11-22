"""Run the official evaluator once per configuration and save the evidence."""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    output = ROOT / "experiments"
    output.mkdir(exist_ok=True)
    for variant in sys.argv[1:] or ["B0", "V1", "V2", "V3", "V4"]:
        if variant not in {"B0", "V1", "V2", "V3", "V4"}:
            raise ValueError(variant)
        print("Running", variant, flush=True)
        target = output / (variant + ".csv")
        result = subprocess.run(
            [sys.executable, "-X", "utf8", "hw4.py", "--data-folder", "public_test", "--output", str(target)],
            cwd=ROOT, env={**os.environ, "HW4_VARIANT": variant}, capture_output=True,
            encoding="utf8", timeout=1800)
        (output / (variant + ".log")).write_text(result.stdout + result.stderr, encoding="utf8")
        result.check_returncode()
        if "Generator failed" in result.stdout or "Traceback" in result.stderr:
            raise RuntimeError(f"Inspect experiments/{variant}.log before using this result.")
        if variant == "V4":
            (ROOT / "results.csv").write_bytes(target.read_bytes())

if __name__ == "__main__":
    main()
