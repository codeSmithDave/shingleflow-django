from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from inquiries.models import Inquiry
from inquiries.services import convert_inquiry_to_client
from .serializers import InquirySerializer
from operations.api.v1.serializers import ClientSerializer
from rest_framework.exceptions import ValidationError

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

 @action(detail=True, methods=['post'])
 def convert(self, request, pk=None):
  inquiry = self.get_object()
  
  if inquiry.client is not None:
   raise ValidationError(
    detail='This inquiry has already been converted.',
    code='already_converted',
   )
  
  client = convert_inquiry_to_client(inquiry)
  return Response(ClientSerializer(client).data, status=201)