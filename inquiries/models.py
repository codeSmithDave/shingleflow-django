from django.conf import settings
from django.db import models
from common.validators import postal_code_validator
from operations.models import Client, Project

# Create your models here.
class Inquiry(models.Model):
 class InquiryStatus(models.TextChoices):
  NEW = "new", "New"
  CONTACTED = "contacted", "Contacted"
  QUOTED = "quoted", "Quoted"
  CONVERTED = "converted", "Converted"
  LOST = "lost", "Lost"
 
 user = models.ForeignKey(
  settings.AUTH_USER_MODEL,
  on_delete=models.PROTECT,
  related_name="inquiries",
  )
 client = models.ForeignKey(
  Client,
  on_delete=models.PROTECT,
  related_name="inquiries",
  null=True,
  blank=True,
 )
 first_name = models.CharField(max_length=50)
 last_name = models.CharField(max_length=50)
 email = models.EmailField(max_length=250)
 phone = models.CharField(max_length=15)
 address = models.CharField(max_length=100)
 city = models.CharField(max_length=100)
 province = models.CharField(
  max_length=2,
  choices=Client.Province.choices
 )
 postal_code = models.CharField(
  max_length=7,
  validators=[postal_code_validator]
 )
 job_type = models.CharField(
  max_length=16,
  choices=Project.JobType.choices
 )
 scrope_description = models.TextField()
 status = models.CharField(
  max_length=9,
  choices=InquiryStatus.choices,
  default=InquiryStatus.NEW
 )
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)
 
 def __str__(self):
  return f"{self.first_name} {self.last_name} - {self.created_at.date()}"