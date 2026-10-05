import pytest
from datetime import date, timedelta
from apps.roadmaps.engine.pacing import calculate_projected_completion

def test_pacing_calculation():
    # 40 hours of content at 10 hours/week = 4 weeks (28 days)
    start = date(2026, 10, 1)
    res = calculate_projected_completion(
        remaining_hours=40.0,
        hours_per_week=10,
        start_date=start
    )

    assert res['remaining_hours'] == 40.0
    assert res['hours_per_week'] == 10
    assert res['estimated_weeks'] == 4.0
    assert res['projected_completion_date'] == start + timedelta(days=28)

def test_pacing_halving_hours_doubles_duration():
    start = date(2026, 10, 1)
    res_10h = calculate_projected_completion(remaining_hours=60.0, hours_per_week=10, start_date=start)
    res_5h = calculate_projected_completion(remaining_hours=60.0, hours_per_week=5, start_date=start)

    assert res_5h['estimated_weeks'] == res_10h['estimated_weeks'] * 2
    assert (res_5h['projected_completion_date'] - start).days == (res_10h['projected_completion_date'] - start).days * 2

def test_pacing_zero_hours_protected():
    # Should fall back to minimum 1 hour/week to avoid DivisionByZero
    res = calculate_projected_completion(remaining_hours=20.0, hours_per_week=0)
    assert res['hours_per_week'] == 1
    assert res['estimated_weeks'] == 20.0
