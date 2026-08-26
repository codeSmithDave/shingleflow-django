import pytest
from operations.models import Client

def test_user_can_create_client(
 user_a,
 api_client,
 api_url_v1_clients,
 client_api_payload,
):
 api_client.force_authenticate(user=user_a)

 response = api_client.post(
     api_url_v1_clients,
     data=client_api_payload,
 )

 assert response.status_code == 201
 assert response.data['first_name'] == 'Australian'
 assert response.data['user'] == user_a.pk


def test_user_cannot_see_other_users_clients(
 user_a,
 user_b,
 api_client,
 make_client,
):
 client_a = make_client(user_a)

 api_client.force_authenticate(user_b)
 url = f'/api/v1/clients/{client_a.pk}/'
 response = api_client.get(url)

 assert response.status_code == 404


def test_user_can_see_own_clients(
 user_a,
 api_client,
 api_url_v1_clients,
 make_client,
):
 make_client(user_a)
 make_client(user_a, first_name='Bobbie', email='bob@steak.au', address='456 boulevard', postal_code='B1A 1A2')

 api_client.force_authenticate(user_a)
 response = api_client.get(api_url_v1_clients)

 assert response.status_code == 200
 assert len(response.data) == 2