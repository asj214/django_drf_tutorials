from django.db import connection
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from configs.utils import (
    aes_encrypt,
    aes_decrypt,
    fetchone,
    fetchall,
)
from configs.redis_connect import redis
from apps.serializers import ArticleSerializer


class AesCryptoEncryptView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        word = request.data.get('word', None)
        encrypt = aes_encrypt(word)
        return Response({'word': word, 'encrypt': encrypt})


class AesCryptoDecryptView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        encrypt = request.data.get('encrypt', None)
        decrypt = aes_decrypt(encrypt)
        return Response({'encrypt': encrypt, 'decrypt': decrypt})


class RedisView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # redis.hset('ktown4u:authentications', 'token', )
        # return Response({'foo': redis.hget('ktown4u:authentications', 'token')})
        return Response()


class RawQueryCRUDViewset(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ArticleSerializer

    def get_object(self, pk=None):
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM posts WHERE 1=1 AND `deleted_at` IS NULL AND `id` = %s', [pk])
            post = fetchone(cursor)
            return post
        except Exception as e:
            raise NotFound('Does not exist.')

    def list(self, request):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM posts WHERE 1=1 AND `deleted_at` IS NULL')
        results = fetchall(cursor)

        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        post = self.get_object(pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
