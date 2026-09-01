from django.conf import settings
from django.db import models
from datetime import time

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

 def __str__(self):
  return f"{self.user}: {self.default_start_time} - {self.default_end_time}"