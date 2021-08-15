from rest_framework import viewsets

from accounts.models import AppUser
from apitest.serializer import AppUserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
