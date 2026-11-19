# Lab 6 — Code and Branch Coverage

This lab applies code and branch testing to a Food Bank Surplus Redistribution Platform workflow (problem statement #62). The workflow aggregates active, eligible donation batches, prioritizes food near expiry, flags invalid batches for review, and monitors cold-chain readings during pickup.

## Files

| File | Purpose |
|---|---|
| `food_bank_workflow.py` | Donation summary and cold-chain workflow under test |
| `test_food_bank_workflow.py` | Branch-focused pytest cases |
| `requirements.txt` | Test and coverage dependencies |
| `screenshots/` | Code and branch coverage result images |

Run from the repository root after installing `LAB 6/requirements.txt`:

```powershell
python -m pytest --cov=food_bank_workflow --cov-branch --cov-report=term-missing "LAB 6"
```

The tests cover active/inactive donations, expiry and minimum-quantity checks, each workflow status, invalid arguments, and empty/safe/unsafe temperature readings.

Latest run: **8 passed**, **100% statement coverage**, and **26/26 branches covered**. See `screenshots/code_coverage.png` and `screenshots/branch_coverage.png`.
