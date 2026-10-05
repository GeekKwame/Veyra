from datetime import date, timedelta
from typing import List, Dict, Any

def calculate_projected_completion(
    remaining_hours: float,
    hours_per_week: int,
    start_date: date = None
) -> Dict[str, Any]:
    """
    Calculates completion timeline based on remaining hours and weekly commitment.
    """
    if start_date is None:
        start_date = date.today()

    eff_hours = max(hours_per_week, 1)
    weeks_needed = remaining_hours / eff_hours
    days_needed = int(weeks_needed * 7)
    projected_date = start_date + timedelta(days=days_needed)

    return {
        'remaining_hours': round(remaining_hours, 1),
        'hours_per_week': eff_hours,
        'estimated_weeks': round(weeks_needed, 1),
        'projected_completion_date': projected_date,
    }

def recalibrate_schedule(
    user_roadmap,
    new_hours_per_week: int
) -> None:
    """
    Recalculates and updates the roadmap completion projection without altering mastered state.
    """
    from apps.roadmaps.models import UserSkillProgress
    from django.db.models import Sum

    # Sum estimated hours of all non-mastered skills
    uncompleted_skills = UserSkillProgress.objects.filter(
        roadmap=user_roadmap
    ).exclude(status='MASTERED').values_list('skill__estimated_hours', flat=True)

    total_remaining = sum(float(h) for h in uncompleted_skills)

    calc = calculate_projected_completion(
        remaining_hours=total_remaining,
        hours_per_week=new_hours_per_week,
        start_date=date.today()
    )

    user_roadmap.committed_hours_per_week = new_hours_per_week
    user_roadmap.projected_completion_date = calc['projected_completion_date']
    user_roadmap.save(update_fields=['committed_hours_per_week', 'projected_completion_date'])
