from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.circles import IsCircleAdmin

from cride.circles.serializers import CircleModelSerializer

from cride.circles.models import Circle, Membership

class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

  serializer_class = CircleModelSerializer
  lookup_field = 'slug_name'

  def get_queryset(self):
    queryset = Circle.objects.all()
    if self.action == 'list':
      return queryset.filter(is_public=True)
    return queryset

  def get_permissions(self):
    permissions = [IsAuthenticated]
    if self.action in ['update', 'partial_update']:
      permissions.append(IsCircleAdmin)
    return [permission() for permission in permissions]

  def perform_create(self, serializer):
    circle = serializer.save()
    user = self.request.user
    profile = user.profile
    Membership.objects.create(
      user=user,
      profile=profile,
      circle=circle,
      is_admin=True,
      remaining_invitations=10
    )
