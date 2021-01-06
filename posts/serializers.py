from rest_framework import serializers
from .models import Post
from authentication.serializers import UserSerializer
from comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'body', 'comments', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context.get('user', None)
        post = Post.objects.create(user=user, **validated_data)
        return post