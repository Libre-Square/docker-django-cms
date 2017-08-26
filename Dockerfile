# Dockerfile to build Django CMS container images
# Included DjangoCMS, Gunicorn and Nginx
# Require a separate running PostgreSQL container

FROM ubuntu

# Create user and folder structure
RUN useradd -m -d /home/django django && \
    mkdir -p /home/django/djangocms && \
    mkdir -p /home/django/custom && \
    mkdir -p /var/log/gunicorn && \
    chown -R django:django /home/django && \
    chown -R django:django /var/log/gunicorn

# Install Python and Nginx
RUN apt-get update && \
    apt-get -y install locales python3 python3-pip systemd nginx && \
    pip3 install --upgrade pip && \
    pip3 install virtualenv

# UTF-8
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

# Install Python packages
RUN su django -c "virtualenv /home/django/env && \
                  . /home/django/env/bin/activate && \
                  pip3 install gunicorn setproctitle psycopg2 djangocms-installer aldryn-bootstrap3 && \
                  pip3 install cmsplugin-filer djangocms-column djangocms-googlemap djangocms-link djangocms-snippet djangocms-style djangocms-video && \
                  pip3 install aldryn-bootstrap3 aldryn-newsblog django-cms-articles Markdown django-markwhat cmsplugin-markdown && \
                  pip3 install djangocms-history djangocms-timed djangocms-light-gallery djangocms-maps && \
                  djangocms -f -p /home/django/djangocms mysite && \
                  deactivate"

# Copy customized files
COPY custom/               /home/django/custom/
COPY gunicorn_config.py    /home/django/gunicorn_config.py
COPY nginx.conf            /etc/nginx/sites-available/nginx.conf
COPY run.sh                /home/django/run.sh

RUN rm /etc/nginx/sites-available/default && \
    rm /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf && \
    chmod +x /home/django/run.sh && \
    ln -s /home/django/run.sh /run.sh

EXPOSE 80

ENTRYPOINT /run.sh
