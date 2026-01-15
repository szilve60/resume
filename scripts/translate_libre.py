import os
import time
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cvsite.settings')
import django
django.setup()

from resume.models import PersonalInfo, Experience, Education, Skill, Project

ENDPOINTS = [
    'https://libretranslate.com/translate',
    'https://translate.argosopentech.com/translate',
    'https://libretranslate.de/translate',
]

HEADERS = {'Accept': 'application/json'}

def translate_text(text):
    if not text:
        return ''
    for url in ENDPOINTS:
        try:
            resp = requests.post(url, data={
                'q': text,
                'source': 'hu',
                'target': 'en',
                'format': 'text'
            }, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                # LibreTranslate returns {'translatedText': '...'}
                if isinstance(data, dict) and 'translatedText' in data:
                    return data['translatedText']
                # Argos returns same key; be defensive
                if isinstance(data, dict) and 'result' in data:
                    return data['result']
            else:
                print(f"Endpoint {url} returned {resp.status_code}")
        except Exception as e:
            print(f"Translate error for endpoint {url}: {e}")
        time.sleep(1)
    return text

if __name__ == '__main__':
    counts = {'personal':0,'experience':0,'education':0,'skill':0,'project':0}

    p = PersonalInfo.objects.first()
    if p:
        changed = False
        if not getattr(p, 'full_name_en', None) and getattr(p, 'full_name', None):
            p.full_name_en = translate_text(p.full_name)
            changed = True
        if not getattr(p, 'title_en', None) and getattr(p, 'title', None):
            p.title_en = translate_text(p.title)
            changed = True
        if changed:
            p.save()
            counts['personal'] += 1

    for e in Experience.objects.all():
        changed = False
        if not getattr(e, 'title_en', None) and getattr(e, 'title', None):
            e.title_en = translate_text(e.title)
            changed = True
        if not getattr(e, 'company_en', None) and getattr(e, 'company', None):
            e.company_en = translate_text(e.company)
            changed = True
        if not getattr(e, 'description_en', None) and getattr(e, 'description', None):
            e.description_en = translate_text(e.description)
            changed = True
        if changed:
            e.save()
            counts['experience'] += 1

    for ed in Education.objects.all():
        changed = False
        if not getattr(ed, 'degree_en', None) and getattr(ed, 'degree', None):
            ed.degree_en = translate_text(ed.degree)
            changed = True
        if not getattr(ed, 'institution_en', None) and getattr(ed, 'institution', None):
            ed.institution_en = translate_text(ed.institution)
            changed = True
        if not getattr(ed, 'period_en', None) and getattr(ed, 'period', None):
            ed.period_en = translate_text(ed.period)
            changed = True
        if changed:
            ed.save()
            counts['education'] += 1

    for s in Skill.objects.all():
        changed = False
        if not getattr(s, 'name_en', None) and getattr(s, 'name', None):
            s.name_en = translate_text(s.name)
            changed = True
        if not getattr(s, 'details_en', None) and getattr(s, 'details', None):
            s.details_en = translate_text(s.details)
            changed = True
        if changed:
            s.save()
            counts['skill'] += 1

    for proj in Project.objects.all():
        changed = False
        if not getattr(proj, 'title_en', None) and getattr(proj, 'title', None):
            proj.title_en = translate_text(proj.title)
            changed = True
        if not getattr(proj, 'summary_en', None) and getattr(proj, 'summary', None):
            proj.summary_en = translate_text(proj.summary)
            changed = True
        if changed:
            proj.save()
            counts['project'] += 1

    print('Translation complete. Counts:', counts)
