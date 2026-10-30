# Static Analysis Findings

Line numbers below refer to the original `pos_system.py` from the supplied ZIP.
The findings are ordered with higher severity first.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval` in promo handling (Bandit B307; Pylint W0123) | Security / medium | 27 | `eval(code_str)` executes arbitrary Python entered as a promo code, allowing commands beyond the intended discount math. | Replace evaluation with a strict parser accepting only `total * number` or `total - number`; reject all other input. |
| Broad exception hides invalid cart data (Pylint W0718; Flake8 E722) | Reliability / medium | 16-17 | A bare `except` catches programming errors and invalid item or quantity data, then silently treats it as a zero-value line. | Validate quantities and item names and raise a specific `ValueError` for invalid inputs. |
| Mutable default receipt list | Correctness / medium | 10 | The default `receipts=[]` is shared between calls, so later checkouts can unexpectedly retain earlier totals. | Use `None` as the default and create a new list inside each call. |
| Invalid checkout values are accepted | Correctness / medium | 12, 37-38 | Negative quantities and negative tax rates can produce negative or misleading totals. | Reject nonpositive quantities and negative tax rates before calculating totals. |
| Pseudo-random receipt ID (Bandit B311) | Security / low | 21 | A non-cryptographic random number is used as a receipt identifier; IDs can collide and are not suitable as security tokens. | Use a monotonically increasing receipt number for display. |
| Silent exception in stock update (Bandit B110) | Reliability / low | 31-34 | A failed stock update is swallowed, so the caller receives no indication that the item was unknown. | Validate the item and quantity, update the stock count, and report invalid input. |
| Receipt file is not managed safely (Pylint W1514, R1732) | Reliability / low | 37-39 | The opened file is not explicitly closed, and the file has no explicit encoding. | Use `Path.open` in a context manager with UTF-8 encoding. |
| Naming and entry point reduce maintainability (Pylint C0103) | Style / low | 41, 44-45 | `printSales` does not follow snake_case, and calling `main()` on import causes prompts and file writes unexpectedly. | Rename to `print_sales` and use the standard `if __name__ == "__main__"` guard. |

## Verification status

The original file received a Pylint score of 5.65/10. Bandit reported one medium and two low-severity findings, and Flake8 reported style and syntax issues. After changes, Pylint scored 10.00/10, Bandit reported no issues, and Flake8 produced no findings.
