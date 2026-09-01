import pytest
from datetime import time

def test_user_can_get_own_schedule(
 user_a,
 make_user_schedule,
 api_client,
 api_url_v1_schedule,
):
 make_user_schedule(
  user_a, 
  default_start_time=time(8, 0), 
  default_end_time=time(16, 0)
  )
 api_client.force_authenticate(user_a)

 response = api_client.get(api_url_v1_schedule)

 assert response.status_code == 200
 assert response.data["default_start_time"] == "08:00:00"
 assert response.data["default_end_time"] == "16:00:00"


def test_user_can_update_start_time(
 user_a,
 make_user_schedule,
 api_client,
 api_url_v1_schedule,
):
 make_user_schedule(user_a)
 api_client.force_authenticate(user_a)

 response = api_client.patch(api_url_v1_schedule, {"default_start_time": "07:30:00"})

 assert response.status_code == 200
 assert response.data["default_start_time"] == "07:30:00"


def test_user_can_update_end_time(
 user_a,
 make_user_schedule,
 api_client,
 api_url_v1_schedule,
):
 make_user_schedule(user_a)
 api_client.force_authenticate(user_a)

 response = api_client.patch(api_url_v1_schedule, {"default_end_time": "18:00:00"})

 assert response.status_code == 200
 assert response.data["default_end_time"] == "18:00:00"


def test_user_can_update_both_times(
 user_a,
 make_user_schedule,
 api_client,
 api_url_v1_schedule,
):
 make_user_schedule(user_a)
 api_client.force_authenticate(user_a)

 response = api_client.patch(
  api_url_v1_schedule,
  {"default_start_time": "06:00:00", "default_end_time": "14:00:00"},
 )

 assert response.status_code == 200
 assert response.data["default_start_time"] == "06:00:00"
 assert response.data["default_end_time"] == "14:00:00"
 
def test_put_not_allowed(
 user_a,
 make_user_schedule,
 api_client,
 api_url_v1_schedule,
):
 make_user_schedule(user_a)
 api_client.force_authenticate(user_a)

 response = api_client.put(
  api_url_v1_schedule,
  {"default_start_time": "06:00:00", "default_end_time": "14:00:00"},
 )

 assert response.status_code == 405
 
def test_patch_rejects_start_time_after_end_time(
 user_a,
 make_user_schedule,
 api_client,
 api_url_v1_schedule,
):
 make_user_schedule(user_a, default_start_time=time(8, 0), default_end_time=time(16, 0))
 api_client.force_authenticate(user_a)

 response = api_client.patch(
  api_url_v1_schedule,
  {"default_start_time": "17:00:00", "default_end_time": "16:00:00"},
 )

 assert response.status_code == 400

def test_patch_rejects_start_time_equal_to_end_time(
 user_a,
 make_user_schedule,
 api_client,
 api_url_v1_schedule,
):
 make_user_schedule(user_a, default_start_time=time(8, 0), default_end_time=time(16, 0))
 api_client.force_authenticate(user_a)

 response = api_client.patch(
  api_url_v1_schedule,
  {"default_start_time": "16:00:00", "default_end_time": "16:00:00"},
 )

 assert response.status_code == 400

def test_patch_partial_update_still_validates_against_existing_end_time(
 user_a,
 make_user_schedule,
 api_client,
 api_url_v1_schedule,
):
 make_user_schedule(user_a, default_start_time=time(8, 0), default_end_time=time(9, 0))
 api_client.force_authenticate(user_a)

 response = api_client.patch(
  api_url_v1_schedule,
  {"default_start_time": "10:00:00"},
 )

 assert response.status_code == 400