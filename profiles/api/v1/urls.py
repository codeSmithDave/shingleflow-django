from rest_framework.routers import DefaultRouter
from django.urls import path
from profiles.api.v1.views import UserScheduleView

# router = DefaultRouter()

urlpatterns = [
 path('schedule/', UserScheduleView.as_view(), name='user-schedule'),
]