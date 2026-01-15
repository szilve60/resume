#!/bin/sh
set -e

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create superuser if env vars are provided (idempotent)
echo "[start.sh] DJANGO_SUPERUSER_USERNAME='${DJANGO_SUPERUSER_USERNAME:-<not set>}'"
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "[start.sh] Superuser envs present (password hidden). Attempting to ensure superuser exists..."
  python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model();\
if not User.objects.filter(username=\"$DJANGO_SUPERUSER_USERNAME\").exists():\
    User.objects.create_superuser(\"$DJANGO_SUPERUSER_USERNAME\", \"$DJANGO_SUPERUSER_EMAIL\", \"$DJANGO_SUPERUSER_PASSWORD\")"
  echo "[start.sh] Superuser ensure step finished."
else
  echo "[start.sh] Superuser envs missing or incomplete; skipping creation."
fi

# Start Gunicorn
exec gunicorn cvsite.wsgi:application --bind 0.0.0.0:${PORT:-8000}
