""" API RouteConf """


from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.viewsets import UserViewSet


# Create your routers here
router = DefaultRouter(trailing_slash=False)
router.register('', UserViewSet, 'user')


urlpatterns = [
    path('api/', include(router.urls)),
]
