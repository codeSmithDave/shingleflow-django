import pytest

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