from hypothesis import given, strategies as st
from processor import sanitize_license_plate, parse_trip_mileage, format_rental_invoice


@given(st.text() | st.none())
def test_sanitize_license_plate_no_crash(s):
    try:
        result = sanitize_license_plate(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"sanitize_license_plate crashed on {s!r}: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_parse_trip_mileage_safe(s):
    try:
        result = parse_trip_mileage(s)
        assert isinstance(result, list)
    except Exception as e:
        assert False, f"parse_trip_mileage crashed on {s!r}: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_format_rental_invoice_safe(s):
    try:
        result = format_rental_invoice(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"format_rental_invoice crashed on {s!r}: {type(e).__name__}: {e}"
