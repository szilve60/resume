"""
Theme system for the CV website.
Handles theme registration, resolution, and template rendering.
"""

from typing import Dict, List, Optional
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.shortcuts import render
from django.conf import settings
import os


class Theme:
    """Represents a single theme configuration."""
    
    def __init__(self, slug: str, name: str, description: str, preview_image: str = None):
        self.slug = slug
        self.name = name
        self.description = description
        self.preview_image = preview_image or f"img/themes/{slug}_preview.jpg"


class ThemeRegistry:
    """Registry for managing available themes."""
    
    def __init__(self):
        self._themes = {}
        self.default_theme = 'minimal'
        self._register_default_themes()
    
    def _register_default_themes(self):
        """Register the default themes."""
        self.register(Theme(
            slug='minimal',
            name='Minimal',
            description='Clean and simple design with focus on content',
            preview_image='img/themes/minimal_preview.jpg'
        ))
        self.register(Theme(
            slug='corporate',
            name='Corporate',
            description='Professional business-style layout',
            preview_image='img/themes/corporate_preview.jpg'
        ))
        self.register(Theme(
            slug='creative',
            name='Creative',
            description='Modern and artistic design with animations',
            preview_image='img/themes/creative_preview.jpg'
        ))
    
    def register(self, theme: Theme):
        """Register a new theme."""
        self._themes[theme.slug] = theme
    
    def get_theme(self, slug: str) -> Optional[Theme]:
        """Get a theme by its slug."""
        return self._themes.get(slug)
    
    def get_all_themes(self) -> List[Theme]:
        """Get all registered themes."""
        return list(self._themes.values())
    
    def is_valid_theme(self, slug: str) -> bool:
        """Check if a theme slug is valid."""
        return slug in self._themes
    
    def get_default_theme(self) -> Theme:
        """Get the default theme."""
        return self._themes[self.default_theme]


# Global theme registry instance
theme_registry = ThemeRegistry()


def get_theme_from_request(request) -> str:
    """
    Resolve the current theme for a request.
    Priority: URL preview > Session preference > Default theme
    """
    # Check if this is a theme preview URL
    if hasattr(request, 'theme_preview'):
        return request.theme_preview
    
    # Check session for preferred theme
    session_theme = request.session.get('preferred_theme')
    if session_theme and theme_registry.is_valid_theme(session_theme):
        return session_theme
    
    # Fall back to default theme
    return theme_registry.default_theme


def render_with_theme(request, template_name: str, context: dict = None, content_type=None, status=None, using=None):
    """
    Render a template with theme support.
    Tries to find the template in the current theme first, falls back to default theme.
    """
    if context is None:
        context = {}
    
    current_theme = get_theme_from_request(request)
    print(f"DEBUG: Current theme resolved to: {current_theme}")
    
    # Add theme context
    context.update({
        'current_theme': current_theme,
        'available_themes': theme_registry.get_all_themes(),
        'theme_obj': theme_registry.get_theme(current_theme),
    })
    
    # Try to find the template in the current theme
    theme_template = f"themes/{current_theme}/{template_name}"
    print(f"DEBUG: Trying template: {theme_template}")
    
    try:
        get_template(theme_template)
        template_to_use = theme_template
        print(f"DEBUG: Using theme template: {template_to_use}")
    except TemplateDoesNotExist:
        # Fall back to default theme if template doesn't exist in current theme
        default_theme_template = f"themes/{theme_registry.default_theme}/{template_name}"
        try:
            get_template(default_theme_template)
            template_to_use = default_theme_template
            print(f"DEBUG: Using default theme template: {template_to_use}")
        except TemplateDoesNotExist:
            # Fall back to the original template name (for backward compatibility)
            template_to_use = template_name
            print(f"DEBUG: Using original template: {template_to_use}")
    
    return render(request, template_to_use, context, content_type, status, using)


def get_available_themes():
    """Helper function to get all available themes (for use in templates)."""
    return theme_registry.get_all_themes()


def set_theme_preference(request, theme_slug: str):
    """Set the user's preferred theme in session."""
    if theme_registry.is_valid_theme(theme_slug):
        request.session['preferred_theme'] = theme_slug
        return True
    return False


def clear_theme_preference(request):
    """Clear the user's theme preference."""
    if 'preferred_theme' in request.session:
        del request.session['preferred_theme']