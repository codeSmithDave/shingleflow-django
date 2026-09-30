import pytest
from datetime import time
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from operations.models import Project, Client
from profiles.models import UserSchedule

User = get_user_model()

@pytest.fixture
def user_a(db):
 return User.objects.create_user(email='user_a@example.com', password='123123', auth_id='auth-user-a')

@pytest.fixture
def user_b(db):
 return User.objects.create_user(email='user_b@example.com', password='123123', auth_id='auth-user-b')

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
def make_user_schedule():
 def _make_user_schedule(user, **overrides):
  defaults = {
   'default_start_time': time(9, 0),
   'default_end_time': time(17, 0),
  }
  defaults.update(overrides)
  return UserSchedule.objects.create(user=user, **defaults)
 return _make_user_schedule

@pytest.fixture
def api_client():
 return APIClient()
