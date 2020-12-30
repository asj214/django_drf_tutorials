from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from .models import Post
from .renderers import PostRenderer
from .serializers import PostSerializer


class PostApiView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    renderer_classes = (PostRenderer,)
    queryset = Post.objects.prefetch_related('user')

    def list(self, request):
        serializer_context = {'request': request}

        page = self.paginate_queryset(self.queryset)
        serializer = self.serializer_class(page, context=serializer_context, many=True)

        return self.get_paginated_response(serializer.data)
    
    def create(self, request):
        serializer_context = {'user': request.user, 'request': request}
        serializer_data = {
            'title': request.data.get('title'),
            'body': request.data.get('body'),
        }

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Does not exist.')

        serializer_data = request.data

        serializer = self.serializer_class(
            serializer_instance, 
            context=serializer_context,
            data=serializer_data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):

        try:
            post = self.queryset.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Does not exist.')
    
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)