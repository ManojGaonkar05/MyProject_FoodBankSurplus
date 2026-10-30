"""Simple point-of-sale checkout and receipt logging."""

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Sequence

PRICE_LIST = {"pen": 10, "notebook": 45, "bag": 799, "bottle": 150}
STOCK_LEVELS = {item_name: 0 for item_name in PRICE_LIST}


@dataclass
class SalesState:
    """Hold this session's total and receipt history."""

    total: float = 0.0
    receipt_lines: list[str] = field(default_factory=list)


SALES = SalesState()


def process_checkout(
    cart_items: Sequence[tuple[str, int]],
    tax_rate: float = 0.05,
    receipts: list[float] | None = None,
) -> float:
    """Calculate a cart total, update sales, and optionally collect totals."""
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative.")
    if receipts is None:
        receipts = []

    subtotal = 0
    for item_name, quantity in cart_items:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Item quantities must be whole numbers.")
        if quantity <= 0:
            raise ValueError("Item quantities must be positive.")
        try:
            unit_price = PRICE_LIST[item_name]
        except KeyError as error:
            raise ValueError(f"Unknown item: {item_name}") from error
        subtotal += unit_price * quantity

    total = subtotal * (1 + tax_rate)
    receipts.append(total)
    SALES.total += total
    receipt_number = len(SALES.receipt_lines) + 1
    SALES.receipt_lines.append(f"Receipt #{receipt_number} total={total:.2f}")
    return total


def apply_promo_code(code_str: str) -> float:
    """Apply a safe promo expression such as 'total * 0.9' or 'total - 50'."""
    match = re.fullmatch(r"\s*total\s*([*-])\s*(\d+(?:\.\d+)?)\s*", code_str)
    if match is None:
        raise ValueError(
            "Promo must use 'total * number' or 'total - number'."
        )

    operator, amount_text = match.groups()
    amount = float(amount_text)
    if operator == "*":
        discounted_total = SALES.total * amount
    else:
        discounted_total = SALES.total - amount
    if discounted_total < 0:
        raise ValueError("Promo cannot reduce sales below zero.")
    return discounted_total


def update_stock(item: str, quantity: int) -> None:
    """Report a stock adjustment for an item in the price list."""
    if item not in PRICE_LIST:
        raise ValueError(f"Unknown item: {item}")
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise ValueError("Stock adjustment must be a whole number.")
    if quantity <= 0:
        raise ValueError("Stock adjustment must be positive.")
    STOCK_LEVELS[item] += quantity
    print(f"Stock updated for {item} by {quantity}")


def save_receipt_log(file: str = "pos_log.txt") -> None:
    """Append the current session's receipts to a UTF-8 text file."""
    with Path(file).open("a", encoding="utf-8") as receipt_file:
        for line in SALES.receipt_lines:
            receipt_file.write(f"{line}\n")


def print_sales() -> None:
    """Print the total sales recorded in this session."""
    print(f"Sales so far: {SALES.total:.2f}")


def main() -> None:
    """Run a small checkout demonstration and prompt for a promo code."""
    print("Bill 1:", process_checkout([("pen", 3), ("notebook", 2)]))
    print("Bill 2:", process_checkout([("bag", 1)]))
    print("Bill 3:", process_checkout([("bottle", 4)]))
    print("After promo:", apply_promo_code("total * 0.9"))

    prompt = "Enter promo code (e.g. total - 50): "
    code = input(prompt).strip() or "total - 50"
    try:
        print("After your promo:", apply_promo_code(code))
    except ValueError as error:
        print(f"Invalid promo code: {error}")

    save_receipt_log()
    print_sales()


if __name__ == "__main__":
    main()
