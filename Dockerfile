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
    apt-get --no-install-recommends -y install locales python3 python3-pip python3-dev gcc systemd nginx && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8 && \
    pip3 install --upgrade pip && \
    pip3 install virtualenv



EXPOSE 80

ENTRYPOINT /run.sh
