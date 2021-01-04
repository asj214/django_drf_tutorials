from rest_framework import serializers
from .models import Comment
from authentication.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'commentable_id', 'commentable_type', 'user', 'body', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context.get('user', None)
        comment = Comment.objects.create(user=user, **validated_data)
        return comment