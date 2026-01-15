import polib
p = polib.pofile('locale/en/LC_MESSAGES/django.po')
p.save_as_mofile('locale/en/LC_MESSAGES/django.mo')
print('Compiled .mo written')
