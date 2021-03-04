from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    # authentication
    RegisterApiView,
    LoginApiView,
    UserApiView,
    # posts
    PostApiViewset,
    # example
    AesCryptoEncryptView,
    AesCryptoDecryptView,
    RedisView,
    CategoryViewset,
)

router = DefaultRouter(trailing_slash=False)

# posts
router.register(r'posts', PostApiViewset)

# categories
router.register(r'categories', CategoryViewset)

urlpatterns = [
    path('auth/register', RegisterApiView.as_view()),
    path('auth/login', LoginApiView.as_view()),
    path('auth/me', UserApiView.as_view()),
    path('examples/aescrypto/encrypt', AesCryptoEncryptView.as_view()),
    path('examples/aescrypto/decrypt', AesCryptoDecryptView.as_view()),
    path('examples/redis', RedisView.as_view()),
]

urlpatterns += router.urls