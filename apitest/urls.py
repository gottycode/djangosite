from django.urls import path, include
from rest_framework import routers

from apitest.views import AppUserViewSet
from apitest.views import UserLoginApiView

router = routers.DefaultRouter()
router.register('users', AppUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', UserLoginApiView.as_view()),
]
