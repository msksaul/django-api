from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import circles as circle_views

router = DefaultRouter()
router.register(r'circles', circle_views.CircleViewSet, basename='circle')

urlpatterns = [
  path('', include(router.urls))
]