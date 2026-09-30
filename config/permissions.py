from rest_framework.permissions import BasePermission
from django.conf import settings

class HasSchemaAPIKey(BasePermission):
 def has_permission(self, request, view):
  key = request.headers.get('X-Schema-Key')
  return key == settings.DOCS_SCHEMA_API_KEY