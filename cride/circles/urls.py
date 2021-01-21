from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import circles as circle_views
from .views import memberships as membership_views

router = DefaultRouter()
router.register(r'circles', circle_views.CircleViewSet, basename='circle')
router.register(
  r'circles/(?P<slug_name>[-a-zA-Z0-0_]+)/members',
  membership_views.MembershipViewSet,
  basename='membership'
)

urlpatterns = [
  path('', include(router.urls))
]