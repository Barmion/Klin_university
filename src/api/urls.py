from django.urls import include, path
from rest_framework import routers

from api.views import WorkerViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'workers', WorkerViewSet, basename='workers')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.authtoken')),
]
