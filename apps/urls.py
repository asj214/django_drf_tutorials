from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    # authentication
    RegisterApiView,
    LoginApiView,
    UserApiView,
)


urlpatterns = [
    path('users/register', RegisterApiView.as_view()),
    path('users/login', LoginApiView.as_view()),
    path('users', UserApiView.as_view()),
]

# urlpatterns += router.urls