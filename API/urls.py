from django import views
from django.urls import path, include
from . import serializer
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
from . import views
from rest_framework.authtoken.views import obtain_auth_token
app_name='api'

urlpatterns = [
       path('token/', obtain_auth_token, name="api_token_auth"),
       path('empenhos/', views.add_empenho.as_view()),       
]