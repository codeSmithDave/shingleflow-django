import pytest
from inquiries.models import Inquiry

@pytest.fixture
def make_inquiry():
 def _make_inquiry(user, client=None, **overrides):
  defaults = {
   'first_name': 'InquiryBob',
   'last_name': 'Steak',
   'email': 'aus@steak.au',
   'phone': '17809114567',
   'address': '123 boulevard',
   'city': 'Calgary',
   'province': 'AB',
   'postal_code': 'A1A 1A2',
   'job_type': 'gutter_install',
   'scope_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras porta diam in justo hendrerit blandit. Pellentesque facilisis pellentesque sapien vitae viverra. Proin pellentesque sollicitudin massa eget pellentesque. Nulla facilisi. Curabitur porta, tortor id lobortis eleifend, sem nulla euismod mi, in sodales nisi lacus vitae felis. Fusce vitae luctus justo, id vehicula nunc. Donec egestas, sapien sed egestas mollis, tellus purus sodales orci, id aliquet dolor sem vel ex. Nulla viverra, erat sit amet feugiat scelerisque, ante nisl finibus nisl, vitae lacinia tortor ex sit amet tellus. Duis sit amet nibh quam. Nam sit amet venenatis libero, ac rutrum mi. Curabitur posuere, turpis in eleifend vulputate, felis nisl vehicula leo, et viverra justo odio in mi. Vestibulum gravida sodales sapien, quis sodales ipsum sollicitudin sollicitudin.',
   'status': 'new',
  }
  defaults.update(overrides)
  return Inquiry.objects.create(user=user, client=client, **defaults)
 return _make_inquiry

@pytest.fixture
def api_url_v1_inquiries():
 return '/api/v1/inquiries/'

def api_url_v1_inquiries_convert(api_url_v1_inquiries, pk):
 return f"{api_url_v1_inquiries}{pk}/convert/"