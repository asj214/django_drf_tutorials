from rest_framework import serializers
from .models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    path = serializers.CharField()

    class Meta:
        model = Attachment
        fields = ('id', 'attachmentable_type', 'attachmentable_id', 'name', 'path', 'created_at')
    
    def create(self, validated_data):
        user = self.context.get('user', None)
        attachment = Attachment.objects.create(user=user, **validated_data)
        return attachment