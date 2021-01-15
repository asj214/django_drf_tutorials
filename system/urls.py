from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('attachments.urls')),
    path('api/', include('references.urls')),
]
