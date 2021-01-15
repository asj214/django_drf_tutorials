from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from .models import Reference
from .renderers import ReferenceRenderer
from .serializers import ReferenceSerializer


class ReferenceApiView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReferenceSerializer
    renderer_classes = (ReferenceRenderer,)
    queryset = Reference.objects

    def list(self, request):

        name = self.request.query_params.get('name', None)

        if name is not None:
            self.queryset = self.queryset.filter(name=name)

        serializer = self.serializer_class(self.queryset, many=True)

        return Response(serializer.data)

    def create(self, request):

        params = {
            'name': request.data.get('name'),
            'key': request.data.get('key'),
            'value': request.data.get('value'),
            'order': request.data.get('order'),
        }

        serializer = self.serializer_class(data=params)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
