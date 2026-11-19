import pytest

from food_bank_workflow import check_cold_chain, summarize_surplus_batches


def batch(**changes):
    record = {"is_active": True, "quantity_kg": 10, "hours_to_expiry": 24}
    record.update(changes)
    return record


def test_counts_active_unexpired_donations_and_marks_urgent():
    result = summarize_surplus_batches([
        batch(quantity_kg=12.5, hours_to_expiry=4),
        batch(quantity_kg=8, hours_to_expiry=20),
        batch(is_active=False, quantity_kg=100),
    ])
    assert result == {
        "available_kg": 20.5,
        "urgent_batches": 1,
        "flagged_batches": 0,
        "status": "PRIORITY_RESCUE",
    }


def test_empty_or_expired_batches_are_not_available():
    result = summarize_surplus_batches([batch(hours_to_expiry=0)])
    assert result["available_kg"] == 0
    assert result["status"] == "NO_AVAILABLE_SURPLUS"


def test_too_many_invalid_batches_require_review():
    result = summarize_surplus_batches([batch(quantity_kg=0) for _ in range(5)])
    assert result["flagged_batches"] == 5
    assert result["status"] == "REVIEW_REQUIRED"


def test_batch_below_minimum_quantity_is_flagged():
    result = summarize_surplus_batches([batch(quantity_kg=0.5)], minimum_kg=1)
    assert result["flagged_batches"] == 1
    assert result["available_kg"] == 0


def test_normal_batches_are_ready_for_reservation():
    result = summarize_surplus_batches([batch(hours_to_expiry=12)])
    assert result["status"] == "READY_FOR_RESERVATION"


@pytest.mark.parametrize("batches,minimum", [(None, 1), ([], -1)])
def test_invalid_summary_arguments_raise(batches, minimum):
    with pytest.raises(ValueError):
        summarize_surplus_batches(batches, minimum)


def test_cold_chain_needs_two_consecutive_high_readings():
    assert check_cold_chain([]) == "NO_READINGS"
    assert check_cold_chain([7, 4, 8]) == "SAFE"
    assert check_cold_chain([4, 6, 7]) == "COLD_CHAIN_ALERT"
