# Lab 7 Fuzzing Report — Food Bank Surplus Platform

**Objective:** Exercise donation input helpers with Hypothesis-generated inputs and make malformed input handling predictable.

## Target functions

- `sanitize_batch_id`: normalizes donation batch references and tolerates non-text input.
- `parse_quantity_readings`: parses comma-separated donated quantities, skipping invalid, negative, and non-finite values.
- `format_donation_summary`: validates a four-field `Donor:Food:Quantity:ExpiryHours` record before formatting it.

## Failure cases addressed

| Input condition | Failure risk in a direct parser | Handling in the fixed helper |
|---|---|---|
| `None` or another non-string | `.strip()` or `.split()` raises `AttributeError` | Return an empty value or `Invalid donation record` |
| Missing or extra `:` separators | Index or unpacking errors | Require exactly four fields |
| Non-numeric quantity or expiry | Uncaught `ValueError` | Return `Invalid donation record` |
| `nan`, infinity, zero, or negative quantity/expiry | Invalid values pass into a donation listing | Reject non-finite and non-positive values |
| Mixed valid and malformed CSV values | One bad field aborts parsing | Skip invalid entries and preserve valid non-negative quantities |

## Test evidence

The Hypothesis properties and regression examples are in `test_processor.py`. Install dependencies from this folder's `requirements.txt`, then run `python -m pytest "LAB 7"` from the repository root. The completed run passed all 6 tests; the result image is `screenshots/hypothesis_tests_passing.png`.
