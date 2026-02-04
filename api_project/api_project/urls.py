"""
URL configuration for api_project project.

This module includes:
- Admin site
- API endpoints from the api app
- Token authentication endpoint
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('api.urls')),
    
    # Token authentication endpoint
    # POST username and password to obtain authentication token
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
