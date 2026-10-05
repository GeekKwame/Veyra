import pytest
from rest_framework.test import APIClient
from apps.careers.models import Career

@pytest.mark.django_db
def test_career_list_and_detail_endpoints():
    client = APIClient()

    # Load or create career
    career = Career.objects.filter(slug='junior-fullstack-developer').first()
    if not career:
        career = Career.objects.create(
            slug='junior-fullstack-developer',
            title='Junior Fullstack Web Developer',
            description='Test description',
            industry_category='Technology',
            is_published=True
        )

    # 1. Career List
    res_list = client.get('/api/v1/careers/')
    assert res_list.status_code == 200
    assert len(res_list.data) >= 1

    # 2. Career Detail
    res_detail = client.get(f'/api/v1/careers/{career.slug}/')
    assert res_detail.status_code == 200
    assert res_detail.data['slug'] == career.slug
    assert 'competencies' in res_detail.data
    assert 'milestones' in res_detail.data

@pytest.mark.django_db
def test_discovery_evaluation_endpoint():
    client = APIClient()

    Career.objects.get_or_create(
        slug='junior-fullstack-developer',
        defaults={
            'title': 'Junior Fullstack Web Developer',
            'description': 'Test description',
            'industry_category': 'Technology',
            'is_published': True
        }
    )

    eval_res = client.post('/api/v1/careers/discovery/evaluate/', {
        'available_hours_per_week': 12,
        'work_style': 'ANALYTICAL',
        'environment': 'REMOTE'
    }, format='json')

    assert eval_res.status_code == 200
    assert 'recommendations' in eval_res.data
    recs = eval_res.data['recommendations']
    assert len(recs) >= 1
    assert recs[0]['match_percentage'] > 50
    assert 'rationale' in recs[0]
