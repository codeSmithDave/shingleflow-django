from django.contrib import admin
from .models import Client, Project, WorkDay

# Register your models here.
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(WorkDay)