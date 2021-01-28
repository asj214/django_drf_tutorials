from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from configs.renderers import BaseRenderer
from apps.models import User
from apps.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer
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
