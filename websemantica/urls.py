from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('sbc.urls')),
]