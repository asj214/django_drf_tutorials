from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from configs.utils import (
    aes_encrypt,
    aes_decrypt
)
from configs.redis_connect import redis


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


        return Response()
        # redis.hset('ktown4u:authentications', 'token', )
        # return Response({'foo': redis.hget('ktown4u:authentications', 'token')})
