from rest_framework.generics import RetrieveUpdateAPIView
from profiles.models import UserSchedule
from profiles.api.v1.serializers import UserScheduleSerializer


class UserScheduleView(RetrieveUpdateAPIView):
 serializer_class = UserScheduleSerializer
 http_method_names = ['get', 'patch']

 def get_object(self):
  return self.request.user.schedule