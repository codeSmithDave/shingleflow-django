from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ClientViewSet, ProjectViewSet, WorkDayViewSet

router = DefaultRouter()
router.register(r"clients", ClientViewSet, basename="client")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"workdays", WorkDayViewSet, basename="workday")

urlpatterns = router.urls + [
 path(
  "clients/<int:client_pk>/projects/",
  ProjectViewSet.as_view(
   {
    "get": "list",
    "post": "create"
    }
   ),
 ),
 path(
  "projects/<int:project_pk>/workdays/",
  WorkDayViewSet.as_view(
   {
    "get": "list",
    "post": "create",
   }
  )
 )
]