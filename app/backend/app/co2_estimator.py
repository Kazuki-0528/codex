from __future__ import annotations

USAGE_EMISSION_FACTOR = {
    "office": 0.0060,
    "meeting": 0.0080,
    "corridor": 0.0035,
    "storage": 0.0025,
}
DEFAULT_FACTOR = 0.0050


def estimate_monthly_co2_kg(
    usage_type: str,
    area_m2: float,
    operating_hours_per_day: float,
    working_days_per_month: int = 22,
) -> float:
    """Simple monthly CO2 estimate based on room usage, area and operation hours.

    Formula:
      monthly_kgco2 = area_m2 * operating_hours_per_day * working_days_per_month * usage_factor
    """
    if area_m2 <= 0:
        raise ValueError("area_m2 must be greater than 0")
    if operating_hours_per_day <= 0:
        raise ValueError("operating_hours_per_day must be greater than 0")
    if working_days_per_month <= 0:
        raise ValueError("working_days_per_month must be greater than 0")

    factor = USAGE_EMISSION_FACTOR.get(usage_type.lower(), DEFAULT_FACTOR)
    estimated = area_m2 * operating_hours_per_day * working_days_per_month * factor
    return round(estimated, 3)
