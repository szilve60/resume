"""
Context processors for theme system.
Provides theme-related variables to all templates.
"""

from .themes import theme_registry, get_theme_from_request


def theme_context(request):
    """
    Add theme-related context variables to all templates.
    """
    current_theme_slug = get_theme_from_request(request)
    
    return {
        'current_theme': current_theme_slug,
        'available_themes': theme_registry.get_all_themes(),
        'theme_obj': theme_registry.get_theme(current_theme_slug),
    }