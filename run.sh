#!/bin/bash

export PYTHONPATH=/home/django/custom:/home/django/djangocms

# Initialize DjangoCMS
if [ ! -f "/home/django/custom/.initialized" ]; then
  echo "Initializing environment..."
  echo
  su -p django -c ". /home/django/env/bin/activate && \
    python /home/django/custom/manage.py makemigrations        --noinput  && \
    python /home/django/custom/manage.py migrate               --noinput  && \
    python /home/django/custom/manage.py collectstatic --clear --noinput  && \
    deactivate && \
    touch /home/django/custom/.initialized"
  
  echo "Environment ready!"
  echo
fi

# Restart Nginx
echo "Restarting Nginx..."
echo
service nginx restart

# Start Gunicorn
echo "Restarting Gunicorn..."
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
