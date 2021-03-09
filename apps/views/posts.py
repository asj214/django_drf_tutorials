from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from configs.renderers import BaseRenderer
from configs.permissions import IsOwnerOrReadOnly
from apps.models import Post
from apps.serializers import PostSerializer


class PostApiViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    renderer_classes = (BaseRenderer,)
    queryset = Post.objects.prefetch_related(
        'user',
    )

    def get_object(self, pk=None):
        try:
            post = self.queryset.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise NotFound('Does not exist.')

    def list(self, request, *args, **kwargs):
        context = {'request': request}

        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            self.queryset = self.queryset.filter(user_id=user_id)

        page = self.paginate_queryset(self.queryset)
        serializer = self.serializer_class(page, context=context, many=True)

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        post = self.get_object(pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'user': request.user, 'request': request}
        params = {
            'title': request.data.get('title'),
            'body': request.data.get('body'),
        }

        serializer = self.serializer_class(
            data=params, context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):

        self.permission_classes = (IsOwnerOrReadOnly,)

        context = {'request': request}
        post = self.get_object(pk)
        params = request.data

        serializer = self.serializer_class(
            post,
            context=context,
            data=params,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, **kwargs):

        self.permission_classes = (IsOwnerOrReadOnly,)
        post = self.get_object(pk)
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)