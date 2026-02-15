"""
URL configuration for newsletters app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('unsubscribe/<uuid:token>/', views.unsubscribe, name='unsubscribe'),
]
