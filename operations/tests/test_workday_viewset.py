import pytest
from datetime import time, date

def test_user_can_create_own_workday(
 user_a,
 make_client,
 make_project,
 make_user_schedule,
 api_url_v1_projects,
 api_client
):
 make_user_schedule(user_a)
 client = make_client(user_a)
 project = make_project(client)
 url = f"{api_url_v1_projects}{project.pk}/workdays/"
 api_client.force_authenticate(user_a)
 payload = {
  'status': 'scheduled',
  'scheduled_date': '2026-09-01',
 }

 response = api_client.post(
  url,
  payload
 )

 assert response.status_code == 201
 assert response.data['status'] == 'scheduled'
 assert response.data['scheduled_date'] == '2026-09-01'

def test_user_can_see_own_workdays(
 user_a,
 make_client,
 make_project,
 make_user_schedule,
 make_workday,
 api_client,
 api_url_v1_workdays,
):
 make_user_schedule(user_a)
 client = make_client(user_a)
 project_1 = make_project(client)
 project_2 = make_project(client)
 make_workday(project_1)
 make_workday(project_2)
 api_client.force_authenticate(user_a)

 response = api_client.get(api_url_v1_workdays)

 assert response.status_code == 200
 assert len(response.data) == 2

def test_user_cannot_see_others_workdays(
 user_a,
 user_b,
 make_client,
 make_project,
 make_user_schedule,
 make_workday,
 api_client,
 api_url_v1_workdays,
):
 make_user_schedule(user_a)
 client = make_client(user_a)
 project = make_project(client)
 workday = make_workday(project)
 api_client.force_authenticate(user_b)
 url = f"{api_url_v1_workdays}{workday.pk}/"
 response = api_client.get(url)

 assert response.status_code == 404

def test_workday_uses_default_schedule_when_times_not_provided(
 user_a,
 make_client,
 make_project,
 make_user_schedule,
 make_workday,
):
 make_user_schedule(user_a)
 client = make_client(user_a)
 project = make_project(client)

 workday = make_workday(
  project=project,
  scheduled_date=date(2026, 8, 15),
 )

 assert workday.start_time == time(9, 0)
 assert workday.end_time == time(17, 0)

def test_workday_respects_explicit_times(
 user_a,
 make_client,
 make_project,
 make_workday,
 make_user_schedule,
):
 make_user_schedule(user_a)
 client = make_client(user_a)
 project = make_project(client)
 workday = make_workday(
  project=project,
  scheduled_date=date(2026, 8, 15),
  start_time=time(13, 0),
  end_time=time(15, 30),
 )

 assert workday.start_time == time(13, 0)
 assert workday.end_time == time(15, 30)