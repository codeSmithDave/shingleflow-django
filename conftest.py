import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user_a(db):
 return User.objects.create_user(username='user_a', password='123123')

@pytest.fixture
def user_b(db):
 return User.objects.create_user(username='user_b', password='123123')

@pytest.fixture
def api_client():
 return APIClient()
