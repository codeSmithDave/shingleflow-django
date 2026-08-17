from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ...models import Inquiry
from .serializers import InquirySerializer

# Create your views here.
class InquiryViewSet(viewsets.ModelViewSet):
 serializer_class = InquirySerializer
 http_method_names = ['get', 'post', 'patch', 'head', 'options']

 # TODO: no auth backend wired up yet —
 # request.user will be AnonymousUser until then, so this permission
 # + queryset scoping is correct but not yet enforceable end-to-end.
 permission_classes = [IsAuthenticated]
 
 def get_queryset(self):
  return Inquiry.objects.filter(user = self.request.user)
 
 def perform_create(self, serializer):
  serializer.save(user = self.request.user)