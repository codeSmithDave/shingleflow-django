from django.db import transaction
from django.db.models import Q
from inquiries.models import Inquiry
from operations.models import Project, Client

def convert_inquiry_to_client(inquiry):
 with transaction.atomic():
  existing_client = find_matching_client(inquiry)  # your matching logic here

  if existing_client:
   backfill_empty_fields(existing_client, inquiry)  # only fill blanks, never overwrite
   client = existing_client
  else:
   client = Client.objects.create(
    user=inquiry.user,
    first_name=inquiry.first_name,
    last_name=inquiry.last_name,
    email=inquiry.email,
    phone=inquiry.phone,
    address=inquiry.address,
    city=inquiry.city,
    province=inquiry.province,
    postal_code=inquiry.postal_code,
   )
  
  Project.objects.create(
   client=client,
   job_type=inquiry.job_type,
   description=inquiry.scope_description,
  )

  inquiry.status = Inquiry.InquiryStatus.CONVERTED
  inquiry.client = inquiry.client or client  # if Inquiry.client FK isn't already set
  inquiry.save()

 return client

def find_matching_client(inquiry):
 name_match = Q(first_name=inquiry.first_name, last_name=inquiry.last_name)
 email_match = Q(email=inquiry.email)
 phone_match = Q(phone=inquiry.phone)
 
 secondary_match = name_match | email_match | phone_match
 
 return Client.objects.filter(
  Q(user=inquiry.user) & Q(address=inquiry.address) & secondary_match
 ).first()
 
def backfill_empty_fields(client, inquiry):
 fields_to_check = ["first_name", "last_name", "email", "phone", "city", "province", "postal_code"]
 updated = False
 for field in fields_to_check:
  if not getattr(client, field):
   setattr(client, field, getattr(inquiry, field))
   updated = True
 
 if updated:
  client.save()
 