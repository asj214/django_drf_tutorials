from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Attachment
from rest_framework_jwt.settings import api_settings


class AttachmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    path = serializers.CharField()
    created_at = serializers.DateTimeField()

    class Meta:
        model = Attachment
        fields = ('id', 'name', 'path')