from django.urls import include, path
from rest_framework import routers

from api.views import CoilViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'coil', CoilViewSet, basename='coil')


urlpatterns = [
    path(r'', include(router.urls)),
]
