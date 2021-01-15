from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import ReferenceApiView


router = DefaultRouter(trailing_slash=False)
router.register(r'references', ReferenceApiView)

urlpatterns = [
    path('', include(router.urls)),
]
