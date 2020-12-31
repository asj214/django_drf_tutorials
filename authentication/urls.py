from django.urls import path
from .views import RegisterApiView, LoginApiView


urlpatterns = [
    path('users/register', RegisterApiView.as_view()),
    path('users/login', LoginApiView.as_view()),
]
