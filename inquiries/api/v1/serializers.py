from rest_framework import serializers
from ...models import Inquiry

class InquirySerializer(serializers.ModelSerializer):
 class Meta:
  model = Inquiry
  fields = [
   "id", "user", "client", "first_name", "last_name", "email", "phone",
   "address", "city", "province", "postal_code",
   "job_type", "scope_description", "status",
   "created_at", "updated_at",
  ]
  read_only_fields = ["user", "client", "created_at", "updated_at"]