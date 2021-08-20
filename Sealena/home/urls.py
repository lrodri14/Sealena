"""
    This urls.py file contains all the urls used by the home app.
"""

from django.urls import path
from .views import home

app_name = 'home'
urlpatterns = [
    path('', home, name='home'),
]
