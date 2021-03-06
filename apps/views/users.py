from rest_framework import status, viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from configs.renderers import BaseRenderer
from configs.utils import numeric
from apps.models import User
from apps.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    PasswordChange
)


# Create your views here.
class RegisterApiView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (BaseRenderer,)
    serializer_class = RegisterSerializer

    def post(self, request):
        user = {
            'name': request.data.get('name', ''),
            'email': request.data.get('email', ''),
            'password': request.data.get('password', ''),
        }

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginApiView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (BaseRenderer, )
    serializer_class = LoginSerializer

    def post(self, request):
        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }

        serializer = self.serializer_class(data=data)
        # 로그인 시리얼라이즈는 ... 다 좋은데 뭔가 좀 내가 이해가 부족한건가 ...
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserApiView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseRenderer,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class UserViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (BaseRenderer,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self, pk=None):
        try:
            return self.queryset.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound('Does not exist.')

    def list(self, request):
        qs = self.queryset
        search_type = request.query_params.get('search_type', '')
        search_value = request.query_params.get('search_value', None)

        if search_type == 'id' and search_value != '':
            search_value = int(numeric(search_value))
            qs = qs.filter(id=search_value)

        if search_type == 'email' and search_value != '':
            qs = qs.filter(email=search_value)

        if search_type == 'name' and search_value != '':
            qs = qs.filter(name=search_value)


        page = self.paginate_queryset(qs)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        user = self.get_object(pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    
    def update(self, request, pk=None, **kwargs):
        user = self.get_object(pk)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        user = self.get_object(pk)
        data = {
            'password': request.data.get('password', None)
        }

        serializer = PasswordChange(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, **kwargs):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)