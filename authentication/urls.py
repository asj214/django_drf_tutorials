from django.urls import path
from .views import RegisterApiView, LoginApiView


urlpatterns = [
    path('auth/register', RegisterApiView.as_view()),
    path('auth/login', LoginApiView.as_view()),
]
