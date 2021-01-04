from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import CreateCommentApiView


urlpatterns = [
    path('comments', CreateCommentApiView.as_view()),
]
