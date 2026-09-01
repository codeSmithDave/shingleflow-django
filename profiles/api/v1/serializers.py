from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from profiles.models import UserSchedule

class UserScheduleSerializer(serializers.ModelSerializer):
 class Meta:
  model = UserSchedule
  fields = ["id", "default_start_time", "default_end_time", "created_at", "updated_at"]
  read_only_fields = ["created_at", "updated_at"]
  
 def validate(self, attrs):
  instance = self.instance
  
  start = attrs.get("default_start_time", getattr(instance, "default_start_time", None))
  end = attrs.get("default_end_time", getattr(instance, "default_end_time", None))

  instance.default_start_time = start
  instance.default_end_time = end

  try:
   instance.clean()
  except DjangoValidationError as e:
   raise serializers.ValidationError(e.message_dict if hasattr(e, "message_dict") else e.messages)

  return attrs