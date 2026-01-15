# CV Website (prototype)

This is a minimal Django prototype for a CV/portfolio site. It includes a simple header with a left `Szilveszter.` button, center `Rólam.` and `English` buttons, and a homepage built from the supplied Hungarian CV layout.

Quick start (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Notes:
- The `English` button currently toggles content client-side (JS). If you'd like full Django i18n, tell me and I'll switch to `django` translation setup.
- Add your real profile image to `resume/static/img/profile.svg` or replace with `profile.jpg`.

Deployment (Railway)

- Railway will detect the `Procfile` and run the `web` command. The `Procfile` runs migrations, `collectstatic` and starts `gunicorn`.
- Set the following environment variables in Railway:
	- `DJANGO_SECRET_KEY` — a production secret key
	- `ALLOWED_HOSTS` — comma-separated hostnames (optional; default '*' is used if empty)
	- `DATABASE_URL` — optional, Railway provides this when attaching a database
	- `DJANGO_DEBUG` — set to `False` in production

Commands Railway runs (via `Procfile`):

```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn cvsite.wsgi --bind 0.0.0.0:$PORT --log-file -
```
