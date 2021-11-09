![GitHub](https://img.shields.io/github/license/bandirom/DjangoTemplateWithDocker?style=plastic)
![Codecov](https://img.shields.io/codecov/c/gh/bandirom/DjangoTemplateWithDocker?style=plastic)
[![Documentation Status](https://readthedocs.org/projects/djangotemplatewithdocker/badge/?version=latest)](https://djangotemplatewithdocker.readthedocs.io/en/latest/?badge=latest)

# Django template in docker with docker-compose

### Features of the template:

#### Project features:
* Docker/Docker-compose environment
* Environment variables
* Separated settings for Dev and Prod django version
* Docker configuration for nginx for 80 and/or 443 ports (dev/stage/prod) (Let's Encrypt certbot)
* Celery worker
* Redis service for caching using socket. Also message broker for queue
* RabbitMQ configuration
* Debug mode (PyCharm Professional)
* ASGI support
* Flake8 integration
* Swagger in Django Admin Panel
* Ready for deploy by one click
* Separated configuration for dev and prod (requirements and settings)
* GitHub Actions
* Redefined default User model (main.models.py)
* MailHog, Jaeger, RabbitMQ integrations
* Multi-stage build for prod versions
* PostgreSql Backup

### How to use:

#### Clone the repo:

    git clone https://github.com/bandirom/DjangoTemplateWithDocker.git ./project_name
    

#### Before running add your superuser email/password and project name in docker/prod/env/.data.env file

    SUPERUSER_EMAIL=example@email.com
    SUPERUSER_PASSWORD=secretp@ssword
    MICROSERVICE_TITLE=MyProject

#### Run the local develop server:

    docker-compose up -d --build
    docker-compose logs -f
    
##### Server will bind 8000 port. You can get access to server by browser [http://localhost:8000](http://localhost:8000)


#### Configuration for develop stage at 9000 port:
    docker-compose -f prod.yml -f prod.dev.yml up -d --build

##### The same configuration could be for stage and prod:
    docker-compose -f prod.yml -f prod.stage.yml up -d --build
    docker-compose -f prod.yml -f prod.prod.yml up -d --build


##### For testing mail backend you can use MailHog service
    docker-compose -f docker-compose -f docker/modules/mailhog.yml up -d --build
    docker-compose -f prod.yml -f prod.dev.yml -f docker/modules/mailhog.yml up -d --build

<b>Don't forget to set SMTP mail backend in settings</b>

#### For set https connection you should have a domain name
<b> In prod.certbot.yml: </b>

Change the envs:
    CERTBOT_EMAIL: your real email
    ENVSUBST_VARS: list of variables which set in nginx.conf files
    APP: value of the variable from list ENVSUBST_VARS
    
To set https for 2 and more nginx servers:
    
    ENVSUBST_VARS: API UI
    API: api.domain.com
    UI: domain.com
    
Run command:

    docker-compose -f prod.yml -f prod.certbot.yml up -d --build
    
### Will be added 

* PgBouncer
