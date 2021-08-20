"""
    This urls.py file contains all the urls used by the main app.
"""

from django.urls import path
from .views import main

app_name = 'main'
urlpatterns = [
    path('', main, name='main'),
]