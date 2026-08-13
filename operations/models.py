from django.db import models
from django.conf import settings
from common.validators import postal_code_validator
from django.utils import timezone

# Create your models here.
class Client(models.Model):
 class Province(models.TextChoices):
  AB = "AB", "Alberta"
  BC = "BC", "British Columbia"
  MB = "MB", "Manitoba"
  NB = "NB", "New Brunswick"
  NL = "NL", "Newfoundland and Labrador"
  NS = "NS", "Nova Scotia"
  NT = "NT", "Northwest Territories"
  NU = "NU", "Nunavut"
  ON = "ON", "Ontario"
  PE = "PE", "Prince Edward Island"
  QC = "QC", "Quebec"
  SK = "SK", "Saskatchewan"
  YT = "YT", "Yukon"
 
 user = models.ForeignKey(
  settings.AUTH_USER_MODEL,
  on_delete=models.PROTECT,
  related_name="clients",
  )
 first_name = models.CharField(max_length=50)
 last_name = models.CharField(max_length=50)
 email = models.EmailField(max_length=254)
 phone = models.CharField(max_length=15)
 address = models.CharField(max_length=100)
 city = models.CharField(max_length=100)
 province = models.CharField(
  max_length=2,
  choices=Province.choices
 )
 postal_code = models.CharField(
  max_length=7,
  validators=[postal_code_validator]
 )
 
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)
 
 def __str__(self):
  return f"{self.first_name} {self.last_name}"
 
class Project(models.Model):
 class JobType(models.TextChoices):
  ROOF_REPLACEMENT = "roof_replacement", "Roof Replacement"
  REPAIR = "repair", "Repair"
  INSPECTION = "inspection", "Inspection"
  GUTTER_INSTALL = "gutter_install", "Gutter Install"
  
 class Status(models.TextChoices):
  UNSCHEDULED = "unscheduled", "Unscheduled"
  SCHEDULED = "scheduled", "Scheduled"
  IN_PROGRESS = "in_progress", "In Progress"
  ATTENTION_NEEDED = "attention_needed", "Attention Needed"
  COMPLETED = "completed", "Completed"
  CANCELLED = "cancelled", "Cancelled"
 
 client = models.ForeignKey(
  Client,
  on_delete=models.PROTECT,
  related_name="projects"
 )
 job_type = models.CharField(
  max_length=16,
  choices=JobType.choices
 )
 deposit_amount = models.DecimalField(
  max_digits=10,
  decimal_places=2,
  null=True,
  blank=True,
 )
 final_payment = models.DecimalField(
  max_digits=10,
  decimal_places=2,
  null=True,
  blank=True,
 )
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)
 
 @property
 def status(self):
  workdays = self.workdays.all()

  if not workdays.exists():
   return self.Status.UNSCHEDULED

  statuses = set(workdays.values_list("status", flat=True))

  if statuses == {WorkDay.Status.CANCELLED}:
   return self.Status.CANCELLED

  if statuses == {WorkDay.Status.COMPLETED}:
   return self.Status.COMPLETED

  if any(wd.is_overdue for wd in workdays):
   return self.Status.ATTENTION_NEEDED

  if WorkDay.Status.COMPLETED in statuses:
   return self.Status.IN_PROGRESS

  return self.Status.SCHEDULED
  
 def __str__(self):
  return f"{self.job_type} - {self.client.first_name} {self.client.last_name}"
 
class WorkDay(models.Model):
 class Status(models.TextChoices):
  SCHEDULED = "scheduled", "Scheduled"
  COMPLETED = "completed", "Completed"
  RESCHEDULED = "rescheduled", "Rescheduled"
  CANCELLED = "cancelled", "Cancelled"
  
 project = models.ForeignKey(
  Project,
  on_delete=models.PROTECT,
  related_name="workdays"
 )
 status = models.CharField(
  max_length=11,
  choices=Status.choices,
  default=Status.SCHEDULED
 )
 scheduled_date = models.DateField()
 rescheduled_date = models.DateField(null=True, blank=True)
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)

 @property
 def effective_date(self):
  return self.rescheduled_date or self.scheduled_date

 @property
 def is_overdue(self):
  return (
   self.status in (self.Status.SCHEDULED, self.Status.RESCHEDULED)
   and self.effective_date < timezone.now().date()
  )
  
 def __str__(self):
  return f"{self.project}: {self.status.capitalize()} - {self.effective_date}"