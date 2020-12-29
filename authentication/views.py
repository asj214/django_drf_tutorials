from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from .models import User
from .serializers import RegisterSerializer, LoginSerializer


# Create your views here.
class RegisterApiView(APIView):

    permission_classes = (AllowAny,)
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
    serializer_class = LoginSerializer

    def post(self, request):

        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
