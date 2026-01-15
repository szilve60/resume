from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import PersonalInfo, Experience, Education, Skill, Project


def home(request):
    person = PersonalInfo.objects.first()
    experiences = Experience.objects.all().order_by('-id')
    educations = Education.objects.all().order_by('-id')
    skills = Skill.objects.all()
    projects = Project.objects.all()
    context = {
        'person': person,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'projects': projects,
        'force_en': False,
        'force_lang': None,
    }
    return render(request, 'home.html', context)


def en_home(request):
    """Render the homepage with English content forced.

    This view returns the same template but sets `force_en` so the
    template displays `_en` fields when present.
    """
    person = PersonalInfo.objects.first()
    experiences = Experience.objects.all().order_by('-id')
    educations = Education.objects.all().order_by('-id')
    skills = Skill.objects.all()
    projects = Project.objects.all()
    context = {
        'person': person,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'projects': projects,
        'force_en': True,
        'force_lang': 'en',
    }
    response = render(request, 'home.html', context)
    # set the django language cookie so subsequent pages remain English
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'en', max_age=365*24*60*60)
    return response


def hu_home(request):
    """Render the homepage with Hungarian language forced and set cookie.

    This mirrors `en_home` but forces Hungarian and sets the language cookie
    to 'hu' so subsequent requests remain in Hungarian.
    """
    person = PersonalInfo.objects.first()
    experiences = Experience.objects.all().order_by('-id')
    educations = Education.objects.all().order_by('-id')
    skills = Skill.objects.all()
    projects = Project.objects.all()
    context = {
        'person': person,
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'projects': projects,
        'force_en': False,
        'force_lang': 'hu',
        'profile_image_url': getattr(settings, 'PROFILE_IMAGE_URL', ''),
    }
    response = render(request, 'home.html', context)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'hu', max_age=365*24*60*60)
    return response
