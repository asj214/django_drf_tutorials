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
    queryset = Category.objects

    def get_object(self, pk=None):
        try:
            user = self.queryset.get(pk=pk)
            return user
        except Category.DoesNotExist:
            raise NotFound('Does not exist.')

    def list(self, request):
        category_id = request.query_params.get('category_id', None)
        qs = self.queryset.all()
        categories = self.category_build(rows=qs, category_id=category_id)
        return Response({'categories': categories})

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

        return self.list(request)

    def retrieve(self, request, pk=None, **kwargs):
        category = self.get_object(pk)
        result = category.childs()
        return Response(result)
    
    def category_build(self, rows=[], depth=1, category_id=None):
        if category_id is not None:
            category_id = int(category_id)
            depth = [r.depth for r in rows if r.id == category_id].pop()

        ret = []
        for row in rows:
            if row.depth != depth:
                continue
            if category_id is not None and category_id != row.id:
                continue

            childs = [r for r in rows if r.parent_id == row.id]
            ret.append({
                'id': row.id,
                'parent_id': row.parent_id,
                'name': row.name,
                'depth': row.depth,
                'order': row.order,
                'is_active': row.is_active,
                'children': self.category_build(rows=childs, depth=row.depth + 1)
            })

        return ret