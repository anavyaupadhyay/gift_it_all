from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from website.api.views import obtainAuthToken

urlpatterns = [
    path('get_auth_token/', obtainAuthToken, name='get_auth_token'),
]
