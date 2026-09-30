from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from datetime import time

class UserProfile(models.Model):
 user = models.OneToOneField(
  settings.AUTH_USER_MODEL,
  on_delete=models.CASCADE,
  related_name="profile"
 )
 # Not collected at signup, so optional until the user sets it.
 brand_name = models.CharField(max_length=100, blank=True, null=True)
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)

 def __str__(self):
  return f"{self.user}: {self.brand_name or 'no brand name'}"

class UserSchedule(models.Model):
 user = models.OneToOneField(
  settings.AUTH_USER_MODEL,
  on_delete=models.CASCADE,
  related_name="schedule"
 )
 default_start_time = models.TimeField(default=time(9, 0))
 default_end_time = models.TimeField(default=time(17, 0))
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)

 def clean(self):
  if self.default_start_time >= self.default_end_time:
   raise ValidationError("default_start_time must be before default_end_time.")

 def save(self, *args, **kwargs):
  # Using clean() directly since all writes currently go through the
  # DRF serializer, which already validates field types/formats.
  # If a non-API write path is ever added (admin, scripts, shell),
  # switch to self.full_clean() to also re-validate field-level rules.
  self.clean()
  super().save(*args, **kwargs)

 def __str__(self):
  return f"{self.user}: {self.default_start_time} - {self.default_end_time}"