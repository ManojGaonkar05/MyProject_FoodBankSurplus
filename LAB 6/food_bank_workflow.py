"""Small Food Bank Surplus Platform workflows used by the Lab 6 tests."""


def summarize_surplus_batches(batches, minimum_kg=1.0):
    """Count active, unexpired donations and flag invalid or urgent batches."""
    if not isinstance(batches, list) or minimum_kg < 0:
        raise ValueError("batches must be a list and minimum_kg cannot be negative")

    available_kg = 0.0
    urgent_batches = 0
    flagged_batches = 0

    for batch in batches:
        if not batch.get("is_active", False):
            continue

        quantity = batch.get("quantity_kg", 0)
        hours_left = batch.get("hours_to_expiry", 0)
        if quantity <= 0 or hours_left <= 0:
            flagged_batches += 1
            continue

        if quantity < minimum_kg:
            flagged_batches += 1
            continue

        if hours_left <= 6:
            urgent_batches += 1
        available_kg += float(quantity)

    if flagged_batches > 4:
        status = "REVIEW_REQUIRED"
    elif available_kg == 0.0:
        status = "NO_AVAILABLE_SURPLUS"
    elif urgent_batches:
        status = "PRIORITY_RESCUE"
    else:
        status = "READY_FOR_RESERVATION"

    return {
        "available_kg": round(available_kg, 2),
        "urgent_batches": urgent_batches,
        "flagged_batches": flagged_batches,
        "status": status,
    }


def check_cold_chain(temperature_readings):
    """Flag a pickup container after two consecutive readings above 5°C."""
    if not temperature_readings:
        return "NO_READINGS"

    high_temperature_streak = 0
    for temperature in temperature_readings:
        if temperature > 5:
            high_temperature_streak += 1
            if high_temperature_streak >= 2:
                return "COLD_CHAIN_ALERT"
        else:
            high_temperature_streak = 0
    return "SAFE"
