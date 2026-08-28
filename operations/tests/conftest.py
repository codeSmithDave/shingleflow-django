import pytest
from operations.models import Client, Project, WorkDay

@pytest.fixture
def client_api_payload():
 return {
  'first_name': 'Australian',
  'last_name': 'Steak',
  'email': 'aus@steak.au',
  'phone': '17809114567',
  'address': '123 boulevard',
  'city': 'Calgary',
  'province': 'AB',
  'postal_code': 'A1A 1A2'
 }
 
@pytest.fixture
def make_workday():
 def _make_workday(project, **overrides):
  defaults = {
   'status': 'scheduled',
   'scheduled_date': '2026-09-01',
  }
  defaults.update(overrides)
  return WorkDay.objects.create(project=project, **defaults)
 return _make_workday

@pytest.fixture
def api_url_v1_clients():
 return '/api/v1/clients/'

@pytest.fixture
def api_url_v1_projects():
 return '/api/v1/projects/'

@pytest.fixture
def api_url_v1_workdays():
 return '/api/v1/workdays/'