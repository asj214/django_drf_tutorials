from rest_framework import serializers
from .models import Reference


class ReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reference
        fields = '__all__'

    def create(self, validated_data):
        reference = Reference.objects.create(**validated_data)
        return reference