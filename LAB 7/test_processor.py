import math

from hypothesis import given, strategies as st

from processor import (
    INVALID_RECORD,
    format_donation_summary,
    parse_quantity_readings,
    sanitize_batch_id,
)


@given(st.one_of(st.text(), st.none(), st.integers(), st.floats(allow_nan=True)))
def test_sanitize_batch_id_is_safe_and_removes_separators(value):
    result = sanitize_batch_id(value)
    assert isinstance(result, str)
    assert not any(character in result for character in " -_#@")
    assert result == result.upper()


@given(st.one_of(st.text(), st.none(), st.integers(), st.lists(st.integers())))
def test_quantity_parser_is_safe_and_returns_finite_nonnegative_numbers(value):
    result = parse_quantity_readings(value)
    assert isinstance(result, list)
    assert all(isinstance(number, float) and math.isfinite(number) and number >= 0
               for number in result)


@given(st.one_of(st.text(), st.none(), st.integers(), st.lists(st.text())))
def test_donation_formatter_never_crashes(value):
    assert isinstance(format_donation_summary(value), str)


def test_donation_summary_accepts_valid_record():
    assert format_donation_summary("Green Grocer:Apples:12.5:6") == (
        "Green Grocer donated 12.5 kg of Apples; expires in 6 hours"
    )


def test_quantity_parser_skips_bad_negative_and_infinite_tokens():
    assert parse_quantity_readings("2, bad, -1, 3.5, inf, , 4") == [2.0, 3.5, 4.0]


def test_malformed_donation_record_returns_clear_error():
    assert format_donation_summary("Shelter:Soup:not-a-number:5") == INVALID_RECORD
