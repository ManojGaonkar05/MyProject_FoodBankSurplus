# Lab 7 — Hypothesis Fuzz Testing

This lab applies property-based input testing to the Food Bank Surplus Redistribution Platform (problem statement #62). It checks donation batch IDs, quantity readings, and donation-summary records, including malformed text, missing values, and non-text inputs.

## Files

| File | Purpose |
|---|---|
| `processor.py` | Defensive food-donation input helpers |
| `test_processor.py` | Hypothesis properties and example regressions |
| `fuzzing_report.md` | Scope, bugs targeted, and fixes |
| `requirements.txt` | Test dependencies |
| `screenshots/` | Captured test-result evidence |

Run from the repository root after installing `LAB 7/requirements.txt`:

```powershell
python -m pytest "LAB 7"
```

Hypothesis generates Unicode text, `None`, numbers, lists, malformed delimiters, and arbitrary numeric strings. The helpers return safe values or a clear validation result instead of leaking parsing exceptions. Latest run: **6 passed**; see `screenshots/hypothesis_tests_passing.png`.
