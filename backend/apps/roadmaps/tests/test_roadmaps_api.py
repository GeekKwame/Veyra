import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.careers.models import Career

@pytest.mark.django_db
def test_roadmap_enrollment_and_recalibration():
    # Setup test user and career
    user = User.objects.create_user(
        email='marcus@example.com',
        full_name='Marcus Vance',
        password='TestPassword123!'
    )
    career = Career.objects.filter(slug='residential-electrician-foundations').first()
    if not career:
        career = Career.objects.create(
            slug='residential-electrician-foundations',
            title='Residential Electrician Foundations',
            description='Electrical trades track',
            industry_category='Skilled Trades',
            is_published=True
        )

    client = APIClient()
    client.force_authenticate(user=user)

    # 1. Enroll in career
    enroll_res = client.post('/api/v1/roadmaps/enroll/', {
        'career_id': str(career.id),
        'committed_hours_per_week': 10
    }, format='json')

    assert enroll_res.status_code == 201
    assert enroll_res.data['career_title'] == career.title
    assert enroll_res.data['committed_hours_per_week'] == 10
    assert 'progress_summary' in enroll_res.data
    assert enroll_res.data['projected_completion_date'] is not None

    initial_date = enroll_res.data['projected_completion_date']

    # 2. Get active roadmap
    active_res = client.get('/api/v1/roadmaps/active/')
    assert active_res.status_code == 200
    assert active_res.data['career_slug'] == career.slug

    # 3. Recalibrate pacing (reduce hours to 5 hrs/week)
    recal_res = client.patch('/api/v1/roadmaps/recalibrate/', {
        'hours_per_week': 5
    }, format='json')

    assert recal_res.status_code == 200
    assert recal_res.data['committed_hours_per_week'] == 5
    # Decreasing hours should push the completion date further out
    assert str(recal_res.data['projected_completion_date']) >= str(initial_date)
