from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import (
  AllowAny,
  IsAuthenticated
)

from cride.users.permissions import IsAccountOwner

from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers import (
  UserLoginSerializer,
  UserModelSerializer,
  UserSignUpSerializer,
  AccountVerificationSerializer,
)

from cride.users.models import User
from cride.circles.models import Circle

class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

  queryset = User.objects.filter(is_active=True, is_client=True)
  serializer_class = UserModelSerializer
  lookup_field = 'username'

  def get_permissions(self):
    if self.action in ['signup', 'login', 'verify']:
      permissions = [AllowAny]
    elif self.action == 'retrieve':
      permissions = [IsAuthenticated, IsAccountOwner]
    else:
      permissions = [IsAuthenticated]
    return [p() for p in permissions]

  @action(detail=False, methods=['post'])
  def login(self, request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, token = serializer.save()
    data = {
      'user': UserModelSerializer(user).data,
      'access_token': token
    }
    return Response(data, status=status.HTTP_201_CREATED)
  
  @action(detail=False, methods=['post'])
  def signup(self, request):
    serializer = UserSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    data = UserModelSerializer(user).data,
    return Response(data, status=status.HTTP_201_CREATED)
  
  @action(detail=False, methods=['post'])
  def verify(self, request):
    serializer = AccountVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    data = {'message': 'You are now verified'}
    return Response(data, status=status.HTTP_200_OK)

  def retrieve(self, request, *args, **kwargs):
    response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
    circles = Circle.objects.filter(members = request.user, membership__is_active=True)
    data = {
      'user': response.data,
      'circles': CircleModelSerializer(circles, many=True).data
    }
    response.data = data
    return response
    