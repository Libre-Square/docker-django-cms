# docker-django-cms

This docker image consists of a **DjangoCMS** + **Gunicorn** + **Nginx** stack.
A separate **PostgreSQL** container is expected as the database backend.
The following is a suggestion of how to use this image

## Step 1: Create a user defined bridge network
> docker network create -d bridge *bridge network name*

## Step 2: Deploy a PostgreSQL container in the private network
> export POSTGRES_DB=*database name*  
> export POSTGRES_USER=*database user name*  
> export POSTGRES_PASSWORD=*database user password*  

> docker run -d \  
>   --name *PostgreSQL container name* \  
>   --network=*bridge network name* \  
>   -e POSTGRES_DB \  
>   -e POSTGRES_USER \  
>   -e POSTGRES_PASSWORD \  
>   postgres

## Step 3: Deploy the DjangoCMS container in the private network
> export LANGUAGE_CODE=*E.g. en*  
> export TIME_ZONE=*E.g. Asia/Hong_Kong*  
> export LANGUAGES="*Language code:Language name;...*"  
> export DATABASE_ENGINE=django.db.backends.postgresql_psycopg2  
> export DATABASE_HOST=*PostgreSQL container name*  
> export DATABASE_PORT=5432  
> export DATABASE_NAME=*database name*  
> export DATABASE_USER=*database user name*  
> export DATABASE_PASSWORD=*database user password*  

> docker run -d \  
>   --name *DjangoCMS container name* \  
>   --network=*bridge network name* \  
>   -p *host publish port*:80 \  
>   -e LANGUAGE_CODE \  
>   -e TIME_ZONE \  
>   -e LANGUAGES \  
>   -e DATABASE_ENGINE \  
>   -e DATABASE_HOST \  
>   -e DATABASE_NAME \  
>   -e DATABASE_USER \  
>   -e DATABASE_PASSWORD \  
>   alexchanwk/docker-django-cms  

## Step 4: Connect the DjangoCMS container to the host bridge network
> docker ps -a | grep django-cms | awk '{print $1}' | xargs docker network connect bridge

## Step 5: Access the DjangoCMS
Visit the administration page of DjangoCMS
E.g. http://hostname:port/admin

The default administrator login:
  Username: admin
  Password: admin

YOu should change the default password via the administration interface.
