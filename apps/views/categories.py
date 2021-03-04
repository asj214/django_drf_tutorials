from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from apps.serializers import CategorySerializer
from apps.models import Category


class CategoryViewset(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related(
        'children'
    )

    def get_object(self, pk=None):
        try:
            user = self.queryset.get(pk=pk)
            return user
        except Category.DoesNotExist:
            raise NotFound('Does not exist.')

    def list(self, request):

        category_id = request.query_params.get('category_id', None)
        if category_id is None:
            self.queryset = self.queryset.filter(parent=None)
        else:
            self.queryset = self.queryset.filter(parent=category_id)

        serializer = self.serializer_class(self.queryset, many=True)

        return Response(serializer.data)

    def create(self, request):

        context = {'user': request.user, 'request': request}
        parent_id = request.data.get('parent_id', None)
        depth = 1
        parent = None

        if parent_id is not None:
            parent = self.get_object(parent_id)
            depth = parent.depth + 1

        params = {
            'parent': parent_id,
            'name': request.data.get('name'),
            'depth': depth,
            'is_active': request.data.get('is_active', False),
        }

        serializer = self.serializer_class(
            data=params, context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, **kwargs):
        return Response({'method': 'retrieve'})