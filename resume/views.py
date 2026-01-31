from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import PersonalInfo, Experience, Education, Skill, Project, SoftwareSkill, PreferredAI
from .themes import render_with_theme, theme_registry, set_theme_preference, clear_theme_preference
from .models import PersonalInfo, Experience, Education, Skill, Project, SoftwareSkill, PreferredAI
from .themes import render_with_theme, theme_registry, set_theme_preference, clear_theme_preference


def home(request):
    # Handle theme parameter from URL
    theme_param = request.GET.get('theme')
    if theme_param and theme_registry.is_valid_theme(theme_param):
        set_theme_preference(request, theme_param)
    
    person = PersonalInfo.objects.first()
    experiences = Experience.objects.all().order_by('-id')
    educations = Education.objects.all().order_by('-id')
    skills = Skill.objects.all()
    software_skills_qs = SoftwareSkill.objects.all().order_by('-rating', 'name')
    software_skills = []
    for s in software_skills_qs:
        software_skills.append({
            'name': s.name,
            'name_en': s.name_en,
            'details': s.details,
            'details_en': s.details_en,
            'rating': s.rating,
            'percent': int((s.rating or 0) * 20),
        })
    projects = Project.objects.all()
    ai_qs = PreferredAI.objects.all().order_by('-rating', 'name')
    ai_skills = []
    for a in ai_qs:
        ai_skills.append({
            'name': a.name,
            'name_en': a.name_en,
            'rating': a.rating,
        })
    context = {
        'person': person,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'software_skills': software_skills,
        'ai_skills': ai_skills,
        'projects': projects,
        'force_en': False,
        'force_lang': None,
        'lang': request.LANGUAGE_CODE,
        'is_en': request.LANGUAGE_CODE == 'en',
        'is_hu': request.LANGUAGE_CODE == 'hu',
    }
    return render_with_theme(request, 'home.html', context)


def en_home(request):
    """Render the homepage with English content forced.

    This view returns the same template but sets `force_en` so the
    template displays `_en` fields when present.
    """
    # Handle theme parameter from URL
    theme_param = request.GET.get('theme')
    if theme_param and theme_registry.is_valid_theme(theme_param):
        set_theme_preference(request, theme_param)
    
    person = PersonalInfo.objects.first()
    experiences = Experience.objects.all().order_by('-id')
    educations = Education.objects.all().order_by('-id')
    skills = Skill.objects.all()
    software_skills_qs = SoftwareSkill.objects.all().order_by('-rating', 'name')
    software_skills = []
    for s in software_skills_qs:
        software_skills.append({
            'name': s.name,
            'name_en': s.name_en,
            'details': s.details,
            'details_en': s.details_en,
            'rating': s.rating,
            'percent': int((s.rating or 0) * 20),
        })
    projects = Project.objects.all()
    ai_qs = PreferredAI.objects.all().order_by('-rating', 'name')
    ai_skills = []
    for a in ai_qs:
        ai_skills.append({
            'name': a.name,
            'name_en': a.name_en,
            'rating': a.rating,
        })
    context = {
        'person': person,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'software_skills': software_skills,
        'ai_skills': ai_skills,
        'projects': projects,
        'force_en': True,
        'force_lang': 'en',
        'lang': 'en',
        'is_en': True,
        'is_hu': False,
    }
    response = render_with_theme(request, 'home.html', context)
    # set the django language cookie so subsequent pages remain English
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'en', max_age=365*24*60*60)
    return response


def hu_home(request):
    """Render the homepage with Hungarian language forced and set cookie.

    This mirrors `en_home` but forces Hungarian and sets the language cookie
    to 'hu' so subsequent requests remain in Hungarian.
    """
    # Handle theme parameter from URL
    theme_param = request.GET.get('theme')
    if theme_param and theme_registry.is_valid_theme(theme_param):
        set_theme_preference(request, theme_param)
    
    person = PersonalInfo.objects.first()
    experiences = Experience.objects.all().order_by('-id')
    educations = Education.objects.all().order_by('-id')
    skills = Skill.objects.all()
    software_skills_qs = SoftwareSkill.objects.all().order_by('-rating', 'name')
    software_skills = []
    for s in software_skills_qs:
        software_skills.append({
            'name': s.name,
            'name_en': s.name_en,
            'details': s.details,
            'details_en': s.details_en,
            'rating': s.rating,
            'percent': int((s.rating or 0) * 20),
        })
    projects = Project.objects.all()
    ai_qs = PreferredAI.objects.all().order_by('-rating', 'name')
    ai_skills = []
    for a in ai_qs:
        ai_skills.append({
            'name': a.name,
            'name_en': a.name_en,
            'rating': a.rating,
        })
    context = {
        'person': person,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'software_skills': software_skills,
        'ai_skills': ai_skills,
        'projects': projects,
        'force_en': False,
        'force_lang': 'hu',
        'lang': 'hu',
        'is_en': False,
        'is_hu': True,
        'profile_image_url': getattr(settings, 'PROFILE_IMAGE_URL', ''),
    }
    response = render_with_theme(request, 'home.html', context)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'hu', max_age=365*24*60*60)
    return response


def contact(request):
    """Simple contact page showing email/phone/linkedin from PersonalInfo."""
    # Handle theme parameter from URL
    theme_param = request.GET.get('theme')
    if theme_param and theme_registry.is_valid_theme(theme_param):
        set_theme_preference(request, theme_param)
    
    person = PersonalInfo.objects.first()
    context = {
        'person': person,
        'lang': request.LANGUAGE_CODE,
        'is_en': request.LANGUAGE_CODE == 'en',
        'is_hu': request.LANGUAGE_CODE == 'hu',
    }
    return render_with_theme(request, 'contact.html', context)


def lab(request):
    """Interactive PLC lab page (local only)."""
    # Handle theme parameter from URL
    theme_param = request.GET.get('theme')
    if theme_param and theme_registry.is_valid_theme(theme_param):
        set_theme_preference(request, theme_param)
    
    context = {
        'lang': request.LANGUAGE_CODE,
        'is_en': request.LANGUAGE_CODE == 'en',
        'is_hu': request.LANGUAGE_CODE == 'hu',
    }
    return render_with_theme(request, 'lab.html', context)


# Theme-related views
def themes_gallery(request):
    """Display all available themes with previews."""
    themes = theme_registry.get_all_themes()
    context = {
        'themes': themes,
        'lang': request.LANGUAGE_CODE,
        'is_en': request.LANGUAGE_CODE == 'en',
        'is_hu': request.LANGUAGE_CODE == 'hu',
    }
    return render_with_theme(request, 'themes_gallery.html', context)


@require_POST
def set_theme(request):
    """Set user's preferred theme via AJAX."""
    theme_slug = request.POST.get('theme')
    if theme_slug and theme_registry.is_valid_theme(theme_slug):
        set_theme_preference(request, theme_slug)
        return JsonResponse({'success': True, 'theme': theme_slug})
    return JsonResponse({'success': False, 'error': 'Invalid theme'}, status=400)


@require_POST 
def clear_theme(request):
    """Clear user's theme preference."""
    clear_theme_preference(request)
    return JsonResponse({'success': True})
