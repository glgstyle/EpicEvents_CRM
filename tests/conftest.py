import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

import pytest

User = get_user_model()

@pytest.fixture
def api_client():
    user = User.objects.create_user(
        first_name='john', email='sales_staff@gmail.com', password='123')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client