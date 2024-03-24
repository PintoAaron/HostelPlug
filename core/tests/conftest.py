from rest_framework.test import APIClient
from core.models import User
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        user = User.objects.create(is_staff=is_staff)
        api_client.force_authenticate(user=user)
    return do_authenticate

