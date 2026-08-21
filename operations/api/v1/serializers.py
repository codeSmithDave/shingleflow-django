from rest_framework import serializers
from ...models import Client, Project, WorkDay

class ClientSerializer(serializers.ModelSerializer):
 class Meta:
  model = Client
  fields = ["id", "user", "first_name", "last_name", "email", "phone",
   "address", "city", "province", "postal_code",
   "created_at", "updated_at",]
  read_only_fields = ["user", "created_at", "updated_at"]
  
class ProjectSerializer(serializers.ModelSerializer):
 status = serializers.ChoiceField(
  choices=Project.Status.choices,
  read_only=True
  )
 
 class Meta:
  model = Project
  fields = ["id", "client", "job_type", "status",
   "deposit_amount", "final_payment",
   "created_at", "updated_at",]
  read_only_fields = ["client", "created_at", "updated_at"]
  
class WorkDaySerializer(serializers.ModelSerializer):
 effective_date = serializers.DateField(read_only=True)
 is_overdue = serializers.BooleanField(read_only=True)
 
 class Meta:
  model = WorkDay
  fields = ["id", "project", "status", "scheduled_date", "rescheduled_date",
   "effective_date", "is_overdue",
   "created_at", "updated_at",]
  read_only_fields = ["effective_date", "is_overdue", "project", "created_at", "updated_at"]