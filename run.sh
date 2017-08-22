#!/bin/bash

# Expected Environment Variables
## LANGUAGE_CODE      (default: "en")
## TIME_ZONE          (default: "Etc/UTC")
## LANGUAGES          (default: "en")
## DATABASE_ENGINE    (default: "django.db.backends.sqlite3")
## DATABASE_HOST      (default: "localhost")
## DATABASE_PORT
## DATABASE_NAME      (default: "project.db")
## DATABASE_USER
## DATABASE_PASSWORD

# Sync database
if [ ! -f "/home/django/custom/.initialized" ]; then
  echo "Synchronizing environment..."
  echo

  export PYTHONPATH=/home/django/custom:/home/django/djangocms

  su -p django -c ". /home/django/env/bin/activate && \
    python /home/django/custom/manage.py makemigrations        --noinput  && \
    python /home/django/custom/manage.py migrate               --noinput  && \
    python /home/django/custom/manage.py collectstatic --clear --noinput  && \
    echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python /home/django/custom/manage.py shell && \
    deactivate &&\
    touch /home/django/custom/.initialized"
  
  echo "Environment ready!"
  echo
fi

# Start Nginx
if (( $(ps -ef | grep -v grep | grep nginx | wc -l) <= 0 ))
then
  echo "Starting Nginx..."
  echo
  service nginx start
fi

# Start Gunicorn
echo "Starting Gunicorn..."
echo
if (( $(ps -ef | grep "gunicorn: master" | grep -v grep | wc -l) > 0 ))
then
  ps -ef | grep "gunicorn: master" | grep -v grep | awk '{print $2}' | xargs kill
fi
su -p django -c ". /home/django/env/bin/activate && \
                /home/django/env/bin/gunicorn -c /home/django/gunicorn_config.py wsgi &"

while [ ! -f /var/log/gunicorn/access.log ];
do
    sleep 1;
done;

echo "Server started!"
echo
tail -f /var/log/gunicorn/access.log
