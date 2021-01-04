from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from .models import Comment
# from .renderers import PostRenderer
from .serializers import CommentSerializer


class CreateCommentApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.prefetch_related('user')

    def post(self, request):
        serializer_context = {'user': request.user, 'request': request}

        commentable = ContentType.objects.get(app_label=request.data.get('commentable_type'))

        serializer_data = {
            'commentable_id': request.data.get('commentable_id'),
            'commentable_type': commentable.id,
            'body': request.data.get('body'),
        }

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)