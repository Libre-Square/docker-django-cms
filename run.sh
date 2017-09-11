#!/bin/bash

export PYTHONPATH=/home/django/custom:/home/django/djangocms

# Start Redis
echo "Restarting Redis..."
echo
if (( $(ps -ef | grep -v grep | grep redis-server | wc -l) > 0 ))
then
  redis-cli shutdown
fi
redis-server --bind 127.0.0.1 --daemonize yes
##################

# Migrate
if [ ! -f "/home/django/custom/.initialized" ]; then
  echo "Initializing environment..."
  echo
  su -p django -c ". /home/django/env/bin/activate && \
    python /home/django/custom/manage.py makemigrations        --noinput  && \
    python /home/django/custom/manage.py migrate               --noinput  && \
    python /home/django/custom/manage.py collectstatic --clear --noinput  && \
    echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python /home/django/custom/manage.py shell && \
    deactivate && \
    touch /home/django/custom/.initialized"
  
  echo "Environment ready!"
  echo
fi

# Restart Nginx
echo "Restarting Nginx..."
echo
service nginx restart

# Restart Daphne
echo "Restarting Daphne..."
echo
if (( $(ps -ef | grep "daphne" | grep -v grep | wc -l) > 0 ))
then
  ps -ef | grep "daphne" | grep -v grep | awk '{print $2}' | xargs kill
fi
su -p django -c ". /home/django/env/bin/activate && \
                daphne -b 127.0.0.1 -p 8080 asgi:channel_layer &"

# Restart workers
echo "Restarting workers..."
echo
if (( $(ps -ef | grep "runworker" | grep -v grep | wc -l) > 0 ))
then
  ps -ef | grep "runworker" | grep -v grep | awk '{print $2}' | xargs kill
fi
seq $(echo $((`grep -c ^processor /proc/cpuinfo`*2+1))) | xargs -I{} su -p django -c ". /home/django/env/bin/activate && python /home/django/custom/manage.py runworker &"

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
