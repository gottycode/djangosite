from rest_framework import serializers

from appauth.models import AppUser


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('username', 'email')
