import pytest

def test_user_can_create_own_projects(
 user_a,
 make_client,
 api_url_v1_clients,
 api_client,
 ):
 client_a = make_client(user_a)
 payload = {
  'job_type': 'roof_replacement',
  'deposit_amount': 500.00,
  'final_payment': 1500.00,
 }
 api_client.force_authenticate(user_a)
 url = f"{api_url_v1_clients}{client_a.pk}/projects/"
 
 response = api_client.post(
  url,
  payload,
  format='json'
 )
 
 assert response.status_code == 201
 
def test_user_can_see_own_projects(
 api_client,
 api_url_v1_projects,
 user_a,
 make_project,
 make_client
):
 client = make_client(user_a)
 make_project(client=client)
 
 api_client.force_authenticate(user_a)
 response = api_client.get(api_url_v1_projects)
 
 assert response.status_code == 200
 assert len(response.data) == 1

def test_user_cannot_see_others_projects(
 user_a,
 user_b,
 make_client,
 make_project,
 api_client,
 api_url_v1_projects,
):
 client = make_client(user_a)
 project = make_project(client)
 url = f"{api_url_v1_projects}{project.pk}/"
 api_client.force_authenticate(user_b)
 response = api_client.get(url)
 
 assert response.status_code == 404
 
def test_project_notes_update_via_patch(
 make_project,
 user_a,
 make_client,
 api_client,
 api_url_v1_projects,
):
 client = make_client(user_a)
 project = make_project(client)
 url = f'{api_url_v1_projects}{project.pk}/'
 notes = 'this is are notes'
 payload = {
  'notes': notes
 }
 
 api_client.force_authenticate(user_a)
 response = api_client.patch(path=url, data=payload, format='json')
 
 assert response.status_code == 200
 assert response.data['notes'] == notes