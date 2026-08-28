import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from operations.models import Project, Client

User = get_user_model()

@pytest.fixture
def user_a(db):
 return User.objects.create_user(username='user_a', password='123123')

@pytest.fixture
def user_b(db):
 return User.objects.create_user(username='user_b', password='123123')

@pytest.fixture
def make_client():
 def _make_client(user, **overrides):
  defaults = {
   'first_name': 'Australian',
   'last_name': 'Steak',
   'email': 'aus@steak.au',
   'phone': '17809114567',
   'address': '123 boulevard',
   'city': 'Calgary',
   'province': 'AB',
   'postal_code': 'A1A 1A2',
  }
  defaults.update(overrides)
  return Client.objects.create(user=user, **defaults)
 return _make_client

@pytest.fixture
def make_project():
 def _make_project(client, **overrides):
  defaults = {
   'job_type': 'roof_replacement',
   'deposit_amount': 500.00,
   'final_payment': 1500.00,
  }
  defaults.update(overrides)
  return Project.objects.create(client=client, **defaults)
 return _make_project

@pytest.fixture
def api_client():
 return APIClient()
