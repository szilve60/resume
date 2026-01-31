"""
Middleware for handling theme preview URLs and theme context.
"""

import re
from django.http import Http404
from django.urls import resolve
from .themes import theme_registry


class ThemeMiddleware:
    """Middleware to handle theme preview URLs and add theme context."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Compile regex for theme preview URLs
        self.theme_preview_regex = re.compile(r'^/t/([a-zA-Z0-9_-]+)(/.*)?$')
    
    def __call__(self, request):
        # Check if this is a theme preview URL
        match = self.theme_preview_regex.match(request.path)
        if match:
            theme_slug = match.group(1)
            
            # Validate theme exists
            if not theme_registry.is_valid_theme(theme_slug):
                raise Http404(f"Theme '{theme_slug}' not found")
            
            # Store the theme slug for this request
            request.theme_preview = theme_slug
            
            # Rewrite the path to remove the theme prefix
            remaining_path = match.group(2) or '/'
            request.path_info = remaining_path
            request.path = remaining_path
        
        response = self.get_response(request)
        return response