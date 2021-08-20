"""
    This global_tags file contains tags that are used throughout the project.
"""

from django import template
from Sealena.settings import STATIC_URL

register = template.Library()


@register.simple_tag
def display_wallpaper(wallpaper_identifier):
    """
        DOCSTRING:
        This display_wallpaper template tag constructs a path to a specific wallpaper based on the wallpaper settings from
        a specific user.
    """
    return STATIC_URL + 'web-backgrounds/bg-{}.jpg'.format(wallpaper_identifier)

