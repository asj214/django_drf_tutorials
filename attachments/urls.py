from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CreateAttachmentApiView, DestroyAttachmentApiView


urlpatterns = [
    path('attachments', CreateAttachmentApiView.as_view()),
    path('attachments/<int:pk>', DestroyAttachmentApiView.as_view()),
]