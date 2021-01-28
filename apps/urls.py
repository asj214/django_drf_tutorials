from django.urls import path
from .views import (
    # authentication
    RegisterApiView,
    LoginApiView,
    UserApiView,
    # example
    AesCryptoEncryptView,
    AesCryptoDecryptView,
    RedisView,
)


urlpatterns = [
    path('users/register', RegisterApiView.as_view()),
    path('users/login', LoginApiView.as_view()),
    path('users', UserApiView.as_view()),
    path('examples/aescrypto/encrypt', AesCryptoEncryptView.as_view()),
    path('examples/aescrypto/decrypt', AesCryptoDecryptView.as_view()),
    path('examples/redis', RedisView.as_view()),
]
