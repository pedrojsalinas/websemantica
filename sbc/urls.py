from django.urls import path
from sbc.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
]
