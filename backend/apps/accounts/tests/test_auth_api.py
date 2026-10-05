import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User

@pytest.mark.django_db
def test_user_registration_and_login():
    client = APIClient()

    # 1. Register new user
    reg_res = client.post('/api/v1/auth/register/', {
        'email': 'elena@example.com',
        'full_name': 'Elena Rostova',
        'password': 'StrongPassword123!'
    }, format='json')

    assert reg_res.status_code == 201
    assert 'token' in reg_res.data
    assert reg_res.data['user']['email'] == 'elena@example.com'

    token = reg_res.data['token']

    # 2. Authenticated /me endpoint
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    me_res = client.get('/api/v1/auth/me/')
    assert me_res.status_code == 200
    assert me_res.data['full_name'] == 'Elena Rostova'

    # 3. Login with credentials
    unauth_client = APIClient()
    login_res = unauth_client.post('/api/v1/auth/login/', {
        'email': 'elena@example.com',
        'password': 'StrongPassword123!'
    }, format='json')

    assert login_res.status_code == 200
    assert login_res.data['token'] == token
