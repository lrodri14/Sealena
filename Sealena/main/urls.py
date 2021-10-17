"""
    This urls.py file contains all the urls used by the main app.
"""

from django.urls import path
from .views import *

app_name = 'main'
urlpatterns = [
    path('', main, name='main'),
    path('lobby/', lobby, name='lobby')
]