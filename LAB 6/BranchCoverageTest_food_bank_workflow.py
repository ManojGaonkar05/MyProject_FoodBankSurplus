import pytest

from food_bank_workflow import check_cold_chain, summarize_surplus_batches


def batch(**changes):
    record = {"is_active": True, "quantity_kg": 10, "hours_to_expiry": 24}
    record.update(changes)
    return record


@pytest.mark.parametrize(
    "records, minimum, expected_status, expected_flagged, expected_urgent",
    [
        ([batch(is_active=False)], 1, "NO_AVAILABLE_SURPLUS", 0, 0),
        ([batch(quantity_kg=0)], 1, "NO_AVAILABLE_SURPLUS", 1, 0),
        ([batch(hours_to_expiry=0)], 1, "NO_AVAILABLE_SURPLUS", 1, 0),
        ([batch(quantity_kg=0.5)], 1, "NO_AVAILABLE_SURPLUS", 1, 0),
        ([batch(hours_to_expiry=6)], 1, "PRIORITY_RESCUE", 0, 1),
        ([batch()], 1, "READY_FOR_RESERVATION", 0, 0),
        ([batch(quantity_kg=0) for _ in range(5)], 1, "REVIEW_REQUIRED", 5, 0),
    ],
)
def test_summary_decision_branches(records, minimum, expected_status, expected_flagged, expected_urgent):
    result = summarize_surplus_batches(records, minimum)
    assert result["status"] == expected_status
    assert result["flagged_batches"] == expected_flagged
    assert result["urgent_batches"] == expected_urgent


@pytest.mark.parametrize("records", [None, {}, "not-a-list"])
def test_non_list_batches_take_validation_branch(records):
    with pytest.raises(ValueError):
        summarize_surplus_batches(records)


def test_negative_minimum_takes_validation_branch():
    with pytest.raises(ValueError):
        summarize_surplus_batches([], minimum_kg=-0.01)


def test_cold_chain_decision_branches_and_streak_reset():
    assert check_cold_chain([]) == "NO_READINGS"
    assert check_cold_chain([6]) == "SAFE"
    assert check_cold_chain([6, 4, 6]) == "SAFE"
    assert check_cold_chain([5, 5.01, 5.1]) == "COLD_CHAIN_ALERT"
