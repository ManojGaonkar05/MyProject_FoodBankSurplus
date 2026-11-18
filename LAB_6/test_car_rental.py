import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics

# Example test case:
def test_single_economy_rental():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [100]
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 110.0
    assert result["status"] == "STANDARD"


# ---------- process_rental_fleet: validation ----------
def test_invalid_rentals_not_list():
    with pytest.raises(ValueError):
        process_rental_fleet("not a list", 10.0)

def test_invalid_negative_admin_fee():
    with pytest.raises(ValueError):
        process_rental_fleet([], -1.0)


# ---------- skipped / empty ----------
def test_unconfirmed_rental_skipped_gives_empty_batch():
    result = process_rental_fleet([{"is_confirmed": False, "days": 3}], 10.0)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}

def test_empty_list_gives_empty_batch():
    assert process_rental_fleet([], 10.0)["status"] == "EMPTY_BATCH"

def test_zero_days_flags_risk_and_skips():
    result = process_rental_fleet([{"is_confirmed": True, "days": 0}], 10.0)
    assert result["status"] == "EMPTY_BATCH"


# ---------- vehicle types ----------
def test_luxury_rate():
    r = [{"is_confirmed": True, "vehicle_type": "luxury", "driver_age": 30, "days": 1}]
    assert process_rental_fleet(r, 0.0)["total_revenue"] == 120.0

def test_suv_rate():
    r = [{"is_confirmed": True, "vehicle_type": "suv", "driver_age": 30, "days": 1}]
    assert process_rental_fleet(r, 0.0)["total_revenue"] == 70.0

def test_defaults_used_when_keys_missing():
    r = [{"is_confirmed": True}]
    assert process_rental_fleet(r, 5.0)["total_revenue"] == 45.0


# ---------- trip segments ----------
def test_negative_mileage_flagged_and_skipped():
    r = [{"is_confirmed": True, "driver_age": 30, "days": 1, "trip_segments": [-5, 100]}]
    assert process_rental_fleet(r, 0.0)["total_revenue"] == 60.0

def test_long_trip_adult_pays_higher_per_mile():
    r = [{"is_confirmed": True, "driver_age": 30, "days": 1, "trip_segments": [400]}]
    assert process_rental_fleet(r, 0.0)["total_revenue"] == 200.0

def test_long_trip_underage_flat_penalty_and_break():
    r = [{"is_confirmed": True, "driver_age": 20, "days": 1, "trip_segments": [400, 100]}]
    assert process_rental_fleet(r, 0.0)["total_revenue"] == 310.0


# ---------- underage surcharge ----------
def test_underage_luxury_surcharge():
    r = [{"is_confirmed": True, "vehicle_type": "luxury", "driver_age": 22, "days": 2}]
    assert process_rental_fleet(r, 0.0)["total_revenue"] == 340.0

def test_underage_non_luxury_surcharge():
    r = [{"is_confirmed": True, "vehicle_type": "economy", "driver_age": 22, "days": 2}]
    assert process_rental_fleet(r, 0.0)["total_revenue"] == 120.0


# ---------- final status ----------
def test_high_risk_audit():
    r = [{"is_confirmed": True, "days": 0} for _ in range(5)]
    assert process_rental_fleet(r, 10.0)["status"] == "HIGH_RISK_AUDIT"


# ---------- check_fleet_telematics ----------
def test_telematics_no_data():
    assert check_fleet_telematics([]) == "NO_DATA"

def test_telematics_ground_vehicle():
    assert check_fleet_telematics([[50, 110, 120]]) == "GROUND_VEHICLE"

def test_telematics_streak_reset_is_safe():
    assert check_fleet_telematics([[110, 50, 110, 50]]) == "SAFE"

def test_telematics_single_speed_spike_safe_across_vehicles():
    assert check_fleet_telematics([[110], [60, 70]]) == "SAFE"
