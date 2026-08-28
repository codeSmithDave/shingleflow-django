import pytest
from inquiries.tests.conftest import api_url_v1_inquiries_convert
from operations.models import Project, Client

def test_inquiry_put_not_allowed(
 user_a,
 make_inquiry,
 api_client,
 api_url_v1_inquiries,
):
 inquiry = make_inquiry(user_a)
 updated_inquiry = {
  'first_name': 'test',
  'last_name': 'test',
 }
 url = f'{api_url_v1_inquiries}{inquiry.pk}/'
 api_client.force_authenticate(user_a)
 
 response = api_client.put(url, updated_inquiry)
 
 assert response.status_code == 405
 
def test_inquiry_delete_not_allowed(
 user_a,
 make_inquiry,
 api_client,
 api_url_v1_inquiries,
):
 inquiry = make_inquiry(user_a)
 url = f'{api_url_v1_inquiries}{inquiry.pk}/'
 api_client.force_authenticate(user_a)
 
 response = api_client.delete(url)
 
 assert response.status_code == 405
 
def test_inquiry_converted_to_client(
 user_a,
 make_inquiry,
 api_url_v1_inquiries,
 api_client,
 # make_project,
):
 inquiry = make_inquiry(user=user_a)
 url = api_url_v1_inquiries_convert(api_url_v1_inquiries, inquiry.pk)
 
 assert inquiry.status is not 'converted'
 
 api_client.force_authenticate(user_a)
 response = api_client.post(url)
 
 assert response.status_code == 201
 inquiry.refresh_from_db()
 assert inquiry.status == 'converted'
 assert inquiry.client is not None
 
def test_inquiry_converted_create_new_project(
 user_a,
 make_inquiry,
 api_client,
 api_url_v1_inquiries,
):
 inquiry = make_inquiry(user=user_a)
 url = api_url_v1_inquiries_convert(api_url_v1_inquiries, inquiry.pk)
 api_client.force_authenticate(user_a)
 
 response = api_client.post(url)
 
 assert response.status_code == 201
 client_id = response.data['id']
 project = Project.objects.get(client_id=client_id)
 assert project.job_type == inquiry.job_type
 
def test_inquiry_converted_matches_existing_client(
 api_client,
 user_a,
 make_client,
 make_inquiry,
 api_url_v1_inquiries,
):
 client = make_client(
  user=user_a,
  address='123 boulevard',
  email='BOB@steak.au',
  first_name='Different',
  last_name='Person',
  phone='19999999999',
  )
 inquiry = make_inquiry(
  user=user_a,
  address='123 boulevard',
  email='aus@steak.au',
  first_name='InquiryBob',
  last_name='Steak',
  phone='19999999999',
  )
 url = api_url_v1_inquiries_convert(api_url_v1_inquiries, inquiry.pk)
 api_client.force_authenticate(user_a)
  
 initial_clients = Client.objects.filter(user=user_a).count()
 response = api_client.post(url)

 assert response.status_code == 201
 assert Client.objects.filter(user=user_a).count() == initial_clients
 assert client.id == response.data['id']
 
def test_inquiry_convert_rejects_already_converted(
 api_url_v1_inquiries,
 user_a,
 make_client,
 make_inquiry,
 api_client,
):
 client = make_client(user_a)
 initial_project_count = Project.objects.filter(client=client).count()
 inquiry = make_inquiry(user=user_a, client=client)
 url = api_url_v1_inquiries_convert(api_url_v1_inquiries, inquiry.pk)
 
 api_client.force_authenticate(user_a)
 response = api_client.post(url)
 
 assert response.status_code == 400
 assert Project.objects.filter(client=client).count() == initial_project_count
 
def test_inquiry_convert_returns_404_for_other_users_inquiry(
 user_a,
 user_b,
 make_inquiry,
 api_client,
 api_url_v1_inquiries
):
 inquiry = make_inquiry(user_a)
 url = api_url_v1_inquiries_convert(api_url_v1_inquiries, inquiry.pk)
 
 api_client.force_authenticate(user_b)
 
 response = api_client.post(url)
 
 assert response.status_code == 404