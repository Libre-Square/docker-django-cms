# docker-django-cms

This docker image consists of a **DjangoCMS** + **Gunicorn** + **Nginx** stack.  
A separate **PostgreSQL** container is expected as the database backend.  
  
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

## Step 3: Deploy the DjangoCMS container in the private network
> export LANGUAGE_CODE=`Language code (E.g. en)`  
> export TIME_ZONE=`Time zone (E.g. Etc/UTC)`  
> export LANGUAGES=`"<Language code>:<Language name>;..." (E.g. en:English;zh-hant:繁;zh-hans:简)`  
> export DATABASE_ENGINE=django.db.backends.postgresql_psycopg2  
> export DATABASE_HOST=`PostgreSQL container name`  
> export DATABASE_PORT=5432  
> export DATABASE_NAME=`database name`  
> export DATABASE_USER=`database user name`  
> export DATABASE_PASSWORD=`database user password`  

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
>   alexchanwk/docker-django-cms /run.sh  

## Step 4: Connect the DjangoCMS container to the host bridge network
> docker ps -a | grep docker-django-cms | awk '{print $1}' | xargs docker network connect bridge  

## Step 5: Access the DjangoCMS
Wait for DjangoCMS to prepare its database if you are starting the container for the first time. It may take about 10 minutes.  
You may attach to the container to check its status.  

When the server is started successfully, visit the administration page of DjangoCMS  
E.g. http://hostname:port/admin  

Default administrator login:  
* Username: admin  
* Password: admin  

You should change the default password via the administration interface.  

## Note:
* A number of DjangoCMS plugins are installed. Please refer to the Dockerfile and my_settings.py for details.
* All customizations are self contained. The default templates and settings.py file are left untouched.
* The DjangoCMS is configured to use a customized template. Please refer to template files in the repository for details.
  * The purpose of this is to make it possible to build the web layouts entirely inside the administration interface. That is to define sections in `DIV`, and then use CSS grid layout to arrange the sections.
