from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from configs.utils import (
    aes_encrypt,
    aes_decrypt
)


class AesCryptoView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    @action(methods=['POST'], detail=True)
    def encrypt(self, request):
        word = request.data.get('word', None)
        encrypt = aes_encrypt(word)
        return Response({'word': word, 'encrypt': encrypt})

    @action(methods=['GET'], detail=True)
    def decrypt(self, request):
        encrypt = request.query_params.get('encrypt', None)
        decrypt = aes_decrypt(encrypt)
        return Response({'encrypt': encrypt, 'decrypt': decrypt})
