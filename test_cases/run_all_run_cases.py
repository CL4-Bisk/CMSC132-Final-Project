from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = ROOT / "test_cases" / "run_cases"
RUNNER = ROOT / "run.py"


def main() -> int:
    case_files = sorted(CASES_DIR.glob("*.mjg"))
    if not case_files:
        print("No run cases found.")
        return 1

    print(f"Running {len(case_files)} runtime test case(s)...")
    print()

    failed = []
    for case in case_files:
        if "interactive" in case.name.lower():
            print(f"- SKIP {case.name} (interactive)")
            continue

        print(f"- RUN  {case.name}")
        result = subprocess.run(
            [sys.executable, str(RUNNER), str(case)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("  PASS")
            if result.stdout.strip():
                print("  STDOUT:")
                for line in result.stdout.strip().splitlines():
                    print(f"    {line}")
        else:
            print("  FAIL")
            failed.append(case.name)
            if result.stderr.strip():
                print("  STDERR:")
                for line in result.stderr.strip().splitlines():
                    print(f"    {line}")
        print()

    if failed:
        print("Failed cases:")
        for name in failed:
            print(f"- {name}")
        return 1

    print("All non-interactive runtime cases finished.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
