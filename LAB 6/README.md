# Lab 6 — Code and Branch Coverage

This lab measures line/code coverage and decision-branch coverage for the Food Bank Surplus workflow (problem statement #62).

## Application under test

- `food_bank_workflow.py` — summarizes eligible surplus batches and checks cold-chain readings.

## Separate required test files

- `CodeCoverageTest_food_bank_workflow.py` — code-coverage test cases.
- `BranchCoverageTest_food_bank_workflow.py` — explicit decision-branch test cases.
- `test_food_bank_workflow.py` — original combined regression test suite.
- `requirements.txt` — pytest and coverage dependencies.

## Run the code-coverage test

From the repository root:

```powershell
python -m coverage erase
python -m coverage run --branch -m pytest -q "LAB 6/CodeCoverageTest_food_bank_workflow.py"
python -m coverage report -m "LAB 6/food_bank_workflow.py"
```

## Run the branch-coverage test

```powershell
python -m coverage erase
python -m coverage run --branch -m pytest -q "LAB 6/BranchCoverageTest_food_bank_workflow.py"
python -m coverage report -m "LAB 6/food_bank_workflow.py"
```

## Verification performed

Both dedicated test files were run against the current application code in a Python environment. The code-coverage test passed (1 test) and the branch-coverage test passed (12 parameterized test cases). Each run reported **100% statement coverage (39/39)** and **100% branch coverage (26/26)** for `food_bank_workflow.py`.

## Submission evidence still to capture

The lab handout specifically asks for terminal-output screenshots after achieving at least 90% code coverage and at least 90% branch coverage. Capture the output from each command above on your own machine and save the images in `screenshots/`. Do not use the same image for both deliverables. The screenshots already in this repository are not a substitute for both separate result screenshots.
