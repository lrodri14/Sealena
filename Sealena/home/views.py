"""
    This views.py file contains the views needed for the home app to work. It is composed of a single view: home -> This
    view is responsible for rendering the home page of the application.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required()
def home(request):
    """
        DOCSTRING:
        Home view is responsible of rendering home page of the project.
    """
    return render(request, 'home/home.html')
