# Django template in docker with docker-compose

### Features of the template:

#### Project features:
* Docker-compose
* Setting Django app via environment variables
* Separated settings for Dev and Prod django version
* Docker configuration for nginx for 80 and/or 443 ports
* Celery worker
* Redis service for caching. Also like message broker for queue
* RabbitMQ configuration
* Debug mode (PyCharm Professional)
* ASGI support for dev and prod
* Flake8 integration
* Swagger in Django Admin Panel
* Ready for deploy by one click
* Separated configuration for dev and prod (requirements and settings)

* Redefined default User model (main.models.py)

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
    
##### Server will bind 8009 port. You can got access to server by browser [http://localhost:8009](http://localhost:8009)

