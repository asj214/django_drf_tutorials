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
    RedisView,
    CategoryViewset
)

router = DefaultRouter(trailing_slash=False)

# posts
router.register(r'posts', PostApiViewset)

# categories
router.register(r'categories', CategoryViewset)


urlpatterns = [
    path('users/register', RegisterApiView.as_view()),
    path('users/login', LoginApiView.as_view()),
    path('users', UserApiView.as_view()),
    path('examples/redis', RedisView.as_view()),
]

urlpatterns += router.urls