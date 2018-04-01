# docker-django-cms

This docker image consists of a **DjangoCMS** + **Gunicorn** + **Nginx** stack.  
A separate **PostgreSQL** container is expected as the database backend.  
A separate **Redis** container is expected to serve as cache.  
  
The following is an example on how you may use this image.  
  

## Step 1: Create a user defined bridge network
> docker network create -d bridge --internal `bridge network name`
  

## Step 2: Deploy a PostgreSQL container in the private network
> export POSTGRES_DB=`database name`  
> export POSTGRES_USER=`database user name`  
> export POSTGRES_PASSWORD=`database user password`  

> docker run -d \  
>   --name `PostgreSQL container name` \  
>   --network=`bridge network name` \  
>   -e POSTGRES_DB \  
>   -e POSTGRES_USER \  
>   -e POSTGRES_PASSWORD \  
>   postgres  
  

## Step 3: Deploy a Redis container in the private network
> docker run -d \  
>   --name `Redis container name` \  
>   --network=`bridge network name` \  
>   redis \  
>   redis-server --appendonly yes  
  

## Step 4: Deploy the DjangoCMS container in the private network
> export LANGUAGE_CODE=`Language code (E.g. en)`  
> export TIME_ZONE=`Time zone (E.g. Etc/UTC)`  
> export LANGUAGES=`"<Language code>:<Language name>;..." (E.g. en:English;zh-hant:繁;zh-hans:简)`  
> export DATABASE_ENGINE=django.db.backends.postgresql_psycopg2  
> export DATABASE_HOST=`PostgreSQL container name`  
> export DATABASE_PORT=5432  
> export DATABASE_NAME=`database name`  
> export DATABASE_USER=`database user name`  
> export DATABASE_PASSWORD=`database user password`  
> export CACHE_REDIS_HOST=`Redis container name`  
> export CACHE_REDIS_PORT=6379  
> export DJANGOCMS_GOOGLEMAP_API_KEY=`Google Map API Key`  

> docker run -d \  
>   --name `DjangoCMS container name` \  
>   --network=`bridge network name` \  
>   -p 127.0.0.1:`host publish port`:80 \  
>   -e LANGUAGE_CODE \  
>   -e TIME_ZONE \  
>   -e LANGUAGES \  
>   -e DATABASE_ENGINE \  
>   -e DATABASE_HOST \  
>   -e DATABASE_NAME \  
>   -e DATABASE_USER \  
>   -e DATABASE_PASSWORD \  
>   -e CACHE_REDIS_HOST \  
>   -e CACHE_REDIS_PORT \  
>   -e DJANGOCMS_GOOGLEMAP_API_KEY \  
>   libresquare/docker-django-cms /run.sh  
  

## Step 5: Connect the DjangoCMS container to the host bridge network
> docker ps -a | grep docker-django-cms | awk '{print $1}' | xargs docker network connect bridge  
  

## Step 6: Access the DjangoCMS
Wait for DjangoCMS to prepare its database if you are starting the container for the first time. It may take about 10 minutes.  
You may attach to the container to check its status.  
  
When the server is started successfully, visit the administration page of DjangoCMS  
E.g. http://hostname:port/admin  
  
Default administrator login:  
* Username: admin  
* Password: admin  
  
**You should change the default password via the administration interface.**  
  
## Notes:
* All customizations are self contained in the `custom` directory (`/home/django/custom`). The default templates and settings.py file are left untouched.
* The DjangoCMS is configured to use a customized template. Please refer to template file (`custom/templates/page.html`) for details.
  * This is to make it possible to build the web layouts entirely inside the administration interface (i.e. define sections in `DIV`, and use CSS flex/grid layout to arrange the sections).
  

## References:
* Command examples
  * Attach to container as `root`
  * **cd into `custom` directory**

1. Clean up orphaned plugins
  > export PYTHONPATH=/home/django/custom:/home/django/djangocms  
  > su -p django -c ". /home/django/env/bin/activate && python manage.py cms delete-orphaned-plugins"  

2. List plugins in use
  > export PYTHONPATH=/home/django/custom:/home/django/djangocms  
  > su -p django -c ". /home/django/env/bin/activate && python manage.py cms list plugins | awk -F: '/model/{print \$2}' | awk -F. '{print \$1}' | sort | uniq"  

3. CMS Data export
    1. Copy `media` directory
    2. Export data as JSON file
  > export PYTHONPATH=/home/django/custom:/home/django/djangocms  
  > su -p django -c ". /home/django/env/bin/activate && python manage.py dumpdata --natural-foreign --exclude auth.permission --exclude contenttypes --indent 2 > cms_dumpdata.json"  

4. CMS Data import
    1. Replace `media` directory
    2. Import data from JSON file
  > export PYTHONPATH=/home/django/custom:/home/django/djangocms  
  > su -p django -c ". /home/django/env/bin/activate && python manage.py loaddata cms_dumpdata.json"  

