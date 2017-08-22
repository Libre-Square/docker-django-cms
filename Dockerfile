# Dockerfile to build Django CMS container images
# Included DjangoCMS, Gunicorn and Nginx
# Require a separate running PostgreSQL container

FROM ubuntu

# Create user and folder structure
RUN useradd -m -d /home/django django && \
    mkdir -p /home/django/djangocms && \
    mkdir -p /home/django/custom && \
    mkdir -p /home/django/custom/templates && \
    mkdir -p /var/log/gunicorn && \
    chown -R django:django /home/django && \
    chown -R django:django /var/log/gunicorn

# Install Python and Nginx
RUN apt-get update && \
    apt-get -y install iputils-ping python3 python3-pip systemd nginx && \
    pip3 install --upgrade pip && \
    pip3 install virtualenv

# Install Python packages
RUN su django -c "virtualenv /home/django/env && \
                  . /home/django/env/bin/activate && \
                  pip3 install gunicorn setproctitle psycopg2 djangocms-installer aldryn-bootstrap3 && \
                  pip3 install cmsplugin-filer djangocms-column djangocms-googlemap djangocms-link djangocms-snippet djangocms-style djangocms-video && \
                  pip3 install aldryn-boilerplates aldryn-bootstrap3 aldryn-newsblog django-cms-articles Markdown django-markwhat && \
                  pip3 install cmsplugin-markdown djangocms-history djangocms-timed djangocms-light-gallery djangocms-page-meta djangocms-maps && \
                  djangocms -f -p /home/django/djangocms mysite && \
                  deactivate"

# Copy customized files
ADD custom/manage.py                /home/django/custom/manage.py
ADD custom/my_settings.py           /home/django/custom/my_settings.py
ADD custom/wsgi.py                  /home/django/custom/wsgi.py
ADD custom/templates/flexible.html  /home/django/custom/templates/flexible.html
ADD gunicorn_config.py              /home/django/gunicorn_config.py
ADD nginx.conf                      /etc/nginx/sites-available/nginx.conf
ADD run.sh                          /home/django/run.sh

RUN rm /etc/nginx/sites-available/default && \
    rm /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf && \
    chmod +x /home/django/run.sh && \
    ln -s /home/django/run.sh /run.sh

EXPOSE 80

ENTRYPOINT /run.sh
