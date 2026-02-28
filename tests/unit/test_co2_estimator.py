import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "app" / "backend"))

from app.co2_estimator import estimate_monthly_co2_kg


def test_estimate_office_monthly_co2():
    estimated = estimate_monthly_co2_kg(
        usage_type="office",
        area_m2=50,
        operating_hours_per_day=8,
        working_days_per_month=20,
    )
    assert estimated == 48.0


def test_estimate_meeting_is_higher_than_office_given_same_inputs():
    office = estimate_monthly_co2_kg("office", 20, 6, 22)
    meeting = estimate_monthly_co2_kg("meeting", 20, 6, 22)
    assert meeting > office


def test_invalid_input_raises_error():
    try:
        estimate_monthly_co2_kg("office", area_m2=0, operating_hours_per_day=8)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert "area_m2" in str(error)
