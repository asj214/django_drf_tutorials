from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    # authentication
    RegisterApiView,
    LoginApiView,
    UserApiView,
    # example
    AesCryptoEncryptView,
    AesCryptoDecryptView,
    RedisView,
    RawQueryCRUDViewset,
)

router = DefaultRouter(trailing_slash=False)

# reference view
router.register(r'examples/articles', RawQueryCRUDViewset, basename='articles')

urlpatterns = [
    path('users/register', RegisterApiView.as_view()),
    path('users/login', LoginApiView.as_view()),
    path('users', UserApiView.as_view()),
    path('examples/aescrypto/encrypt', AesCryptoEncryptView.as_view()),
    path('examples/aescrypto/decrypt', AesCryptoDecryptView.as_view()),
    path('examples/redis', RedisView.as_view()),
]

urlpatterns += router.urls