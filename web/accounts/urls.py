"""
URL configuration for accounts app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Will add authentication endpoints here
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
