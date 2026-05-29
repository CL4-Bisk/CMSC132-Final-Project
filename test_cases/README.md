# Test Cases for CMSC132 ISA Final Project

This folder contains instruction-program test cases that cover the major scope of the project:
- arithmetic/data movement operations
- addressing modes
- comments parsing
- exception path (division by zero)
- block/function/jump compile paths

## Folder Layout

- `run_cases/`: runnable end-to-end cases using `run.py`
- `compile_cases/`: compiler-focused cases (some are intentionally edge/invalid)
- `run_all_run_cases.py`: runs all files in `run_cases/`
- `check_compile_cases.py`: compiles each file in `compile_cases/`

## Run All Runtime Cases

```powershell
python test_cases\run_all_run_cases.py
```

## Check Compile Cases

```powershell
python test_cases\check_compile_cases.py
```

## Notes

- `run_cases/10_scan_prnt_interactive.mjg` is interactive (`SCAN`) and asks for input.
- `compile_cases/05_invalid_operand_rules.mjg` is expected to produce compile errors.
