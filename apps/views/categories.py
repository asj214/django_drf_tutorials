from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from apps.serializers import CategorySerializer, UserSerializer
from apps.models import Category


class CategoryViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('user')

    def get_object(self, pk=None):
        try:
            user = self.queryset.get(pk=pk)
            return user
        except Category.DoesNotExist:
            raise NotFound('Does not exist.')

    def list(self, request):
        category_id = request.query_params.get('category_id', None)
        is_active = request.query_params.get('is_active', None)
        is_admin = request.query_params.get('is_admin', None)

        qs = self.queryset
        if is_active is not None:
            qs = qs.filter(is_active=is_active)

        qs = qs.all()

        if request.query_params.get('pure', None) is not None:
            serializer = self.serializer_class(qs, many=True)
            return Response(serializer.data)

        categories = self.category_build(rows=qs, category_id=category_id, is_admin=is_admin)
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
            'order': request.data.get('order', 1)
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

    def update(self, request, pk=None, **kwargs):
        category = self.get_object(pk)
        params = {
            'parent': None,
            'depth': 1,
            'name': request.data.get('name', None),
            'order': request.data.get('order', 1),
            'is_active': request.data.get('is_active', False)
        }

        parent_id = request.data.get('parent_id', None)

        if parent_id is not None:
            parent = Category.objects.get(pk=parent_id)
            params['parent'] = parent.id
            params['depth'] = parent.depth + 1

        serializer = self.serializer_class(
            category,
            data=params
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.list(request)

    def destroy(self, request, pk=None, **kwargs):
        category = self.get_object(pk)
        category.delete()

        return self.list(request)

    def category_build(self, rows=[], depth=1, parent_id=None, category_id=None, is_admin=None):
        if category_id is not None:
            category_id = int(category_id)
            depth = [r.depth for r in rows if r.id == category_id].pop()

        ret = []
        for row in rows:
            if row.depth != depth:
                continue
            if category_id is not None and category_id != row.id:
                continue
            if parent_id is not None and row.parent_id != parent_id:
                continue

            add = {
                'id': row.id,
                'parent_id': row.parent_id,
                'name': row.name,
                'depth': row.depth,
                'order': row.order,
                'is_active': row.is_active,
                'children': self.category_build(rows=rows, parent_id=row.id, depth=row.depth + 1, is_admin=is_admin)
            }

            if is_admin is not None:
                serializer = UserSerializer(row.user)
                add['user'] = serializer.data

            ret.append(add)

        return ret