import pytest

from food_bank_workflow import check_cold_chain, summarize_surplus_batches


def batch(**changes):
    record = {"is_active": True, "quantity_kg": 10, "hours_to_expiry": 24}
    record.update(changes)
    return record


def test_code_paths_for_donation_summary_and_cold_chain():
    # Invalid function arguments
    with pytest.raises(ValueError):
        summarize_surplus_batches(None)
    with pytest.raises(ValueError):
        summarize_surplus_batches([], minimum_kg=-1)

    # Active/inactive, invalid quantity/expiry, minimum threshold and urgency
    assert summarize_surplus_batches([batch(is_active=False)])["status"] == "NO_AVAILABLE_SURPLUS"
    assert summarize_surplus_batches([batch(quantity_kg=0)])["flagged_batches"] == 1
    assert summarize_surplus_batches([batch(hours_to_expiry=0)])["flagged_batches"] == 1
    assert summarize_surplus_batches([batch(quantity_kg=0.5)], minimum_kg=1)["flagged_batches"] == 1
    assert summarize_surplus_batches([batch(hours_to_expiry=6)])["status"] == "PRIORITY_RESCUE"
    assert summarize_surplus_batches([batch()])["status"] == "READY_FOR_RESERVATION"
    assert summarize_surplus_batches([batch(quantity_kg=0) for _ in range(5)])["status"] == "REVIEW_REQUIRED"
    assert summarize_surplus_batches([batch(quantity_kg=1.236)])["available_kg"] == 1.24

    # Empty input, safe readings, reset after a normal reading, and alert
    assert check_cold_chain([]) == "NO_READINGS"
    assert check_cold_chain([7, 4, 8]) == "SAFE"
    assert check_cold_chain([4, 6, 7]) == "COLD_CHAIN_ALERT"
