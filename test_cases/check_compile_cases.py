from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = ROOT / "test_cases" / "compile_cases"

EXPECTED_FAIL = {
    "05_invalid_operand_rules.mjg",
}


def compile_case(case_path: Path) -> subprocess.CompletedProcess[str]:
    snippet = (
        "from compiler import Instruction;"
        "from pathlib import Path;"
        f"lines=Path(r'{str(case_path)}').read_text(encoding='utf-8').splitlines();"
        "Instruction.encodeProgram(lines)"
    )
    return subprocess.run(
        [sys.executable, "-c", snippet],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def main() -> int:
    case_files = sorted(CASES_DIR.glob("*.mjg"))
    if not case_files:
        print("No compile cases found.")
        return 1

    print(f"Checking {len(case_files)} compile case(s)...")
    print()

    failed = []
    for case in case_files:
        expected_fail = case.name in EXPECTED_FAIL
        result = compile_case(case)
        did_fail = result.returncode != 0

        print(f"- CHECK {case.name}")

        if expected_fail:
            if did_fail:
                print("  PASS (failed as expected)")
            else:
                print("  WARN (expected to fail, but process exited 0)")
        else:
            if did_fail:
                print("  FAIL")
                failed.append(case.name)
            else:
                print("  PASS")

        if result.stdout.strip():
            print("  STDOUT:")
            for line in result.stdout.strip().splitlines():
                print(f"    {line}")
        if result.stderr.strip():
            print("  STDERR:")
            for line in result.stderr.strip().splitlines():
                print(f"    {line}")
        print()

    if failed:
        print("Compile cases that failed unexpectedly:")
        for name in failed:
            print(f"- {name}")
        return 1

    print("Compile-case checks finished.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
