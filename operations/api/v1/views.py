from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from operations.models import Client, Project, WorkDay
from .serializers import ClientSerializer, ProjectSerializer, WorkDaySerializer

class ClientViewSet(viewsets.ModelViewSet):
 serializer_class = ClientSerializer
 http_method_names = ['get', 'post', 'patch', 'head', 'options']
 
 # TODO: no auth backend wired up yet
 permission_classes = [IsAuthenticated]
 
 def get_queryset(self):
  return Client.objects.filter(user=self.request.user)
 
 def perform_create(self, serializer):
  serializer.save(user = self.request.user)
  
  
class ProjectViewSet(viewsets.ModelViewSet):
 serializer_class = ProjectSerializer
 http_method_names = ['get', 'post', 'patch', 'head', 'options']
 # TODO: no auth backend wired up yet
 permission_classes = [IsAuthenticated]
 
 def get_queryset(self):
  # filter for data related to the user from auth
  queryset = Project.objects.filter(client__user = self.request.user)
  
  # further filter the query based on provided client ID
  # if provided through client_pk
  if('client_pk' in self.kwargs):
   queryset = queryset.filter(client_pk = self.kwargs['client_pk'])
  
  return queryset
 
 def perform_create(self, serializer):
  client = Client.objects.get(
   pk=self.kwargs["client_pk"],
   user=self.request.user,
  )
  serializer.save(client = client)
  
class WorkDayViewSet(viewsets.ModelViewSet):
 serializer_class = WorkDaySerializer
 http_method_names = ['get', 'post', 'patch', 'head', 'options']
 # TODO: no auth backend wired up yet
 permission_classes = [IsAuthenticated]
 
 def get_queryset(self):
  queryset = WorkDay.objects.filter(project__client__user = self.request.user)
  
  if('project_pk' in self.kwargs):
   queryset = queryset.filter(project__pk = self.kwargs['project_pk'])
  
  return queryset
 
 def perform_create(self, serializer):
  project = Project.objects.get(
   client__user = self.request.user,
   pk = self.kwargs['project_pk']
  )
  
  serializer.save(project = project)