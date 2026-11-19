"""Defensive input helpers for food donations and pickup reservations."""

import math

INVALID_RECORD = "Invalid donation record"


def sanitize_batch_id(batch_id):
    """Remove separators from a donated-batch reference; non-text is empty."""
    if not isinstance(batch_id, str):
        return ""
    cleaned = batch_id.strip()
    for character in " -_#@":
        cleaned = cleaned.replace(character, "")
    return cleaned.upper()


def parse_quantity_readings(readings_csv):
    """Parse comma-separated kg values, ignoring empty or invalid entries."""
    if not isinstance(readings_csv, str):
        return []
    values = []
    for token in readings_csv.split(","):
        try:
            value = float(token.strip())
        except ValueError:
            continue
        if math.isfinite(value) and value >= 0:
            values.append(value)
    return values


def format_donation_summary(donation_record):
    """Format a 'Donor:Food:Quantity:ExpiryHours' record safely."""
    if not isinstance(donation_record, str):
        return INVALID_RECORD
    parts = donation_record.split(":")
    if len(parts) != 4:
        return INVALID_RECORD
    donor, food, quantity_text, expiry_text = (part.strip() for part in parts)
    if not donor or not food:
        return INVALID_RECORD
    try:
        quantity = float(quantity_text)
        expiry = float(expiry_text)
    except ValueError:
        return INVALID_RECORD
    if not math.isfinite(quantity) or not math.isfinite(expiry):
        return INVALID_RECORD
    if quantity <= 0 or expiry <= 0:
        return INVALID_RECORD
    return f"{donor} donated {quantity:g} kg of {food}; expires in {expiry:g} hours"
