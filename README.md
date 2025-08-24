![GitHub](https://img.shields.io/github/license/bandirom/DjangoTemplateWithDocker?style=plastic)
![Codecov](https://img.shields.io/codecov/c/gh/bandirom/DjangoTemplateWithDocker?style=plastic)
[![Documentation Status](https://readthedocs.org/projects/djangotemplatewithdocker/badge/?version=latest)](https://djangotemplatewithdocker.readthedocs.io/en/latest/?badge=latest)
[![Docker Image CI](https://github.com/bandirom/DjangoTemplateWithDocker/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/bandirom/DjangoTemplateWithDocker/actions/workflows/main.yml)

---

# Django project template in docker


### 1. Project Structure

```text
django-template/
├── .github/ # GitHub actions for CI/CD
├── docker/ # Docker configs for dev & prod
│ ├── dev/
│ ├── prod/
├── web/ # Django app source
│ ├── src/
│ ├── manage.py
│ ├── pyproject.toml # Poetry config
├── docker-compose.yml # Dev docker-compose file
├── prod.yml # Prod docker-compose file
```


### ✅ **2. Project features**
| Feature                           | Status |
|-----------------------------------|--------|
| Dockerized Environment            | ✅      |
| Celery & Redis                    | ✅      |
| PostgreSQL + Backup               | ✅      |
| ASGI (Uvicorn) Support            | ✅      |
| Swagger (DRF-Spectacular)         | ✅      |
| CI/CD (GitHub Actions)            | ✅      |
| Multi-stage Docker build for prod | ✅      |
| RabbitMQ Support                  | ✅      |
| Mailpit for Dev SMTP              | ✅      |
| Linters (black, ruff)             | ✅      |
| Postgres backup                   | ✅      |



### ✅ **3. Quick Start (Dev)**

#### Click "Use this template" button or clone the repository:

```shell
git clone https://github.com/bandirom/django-template.git ./project_name
```


#### Before running add your superuser email/password and project name in docker/prod/env/.data.env file

```dotenv
SUPERUSER_EMAIL=example@email.com
SUPERUSER_PASSWORD=secretp@ssword
PROJECT_TITLE=MyProject
```

#### Run the local develop server:

```shell
docker-compose up -d --build
docker-compose logs -f
```
    
##### Server will run on 8000 port. You can get access to server by browser [http://localhost:8000](http://localhost:8000)

Run django commands through exec:
```shell
docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py shell
```

Get access to the container
```shell
docker-compose exec web sh
```

#### Run Tests
```shell
docker-compose run --rm web pytest
```


##### Run Mailpit service. Mail smtp for local development

* Run Mailpit
```shell
docker run -p 1025:1025 -p 8025:8025 -d -it --rm axllent/mailpit
```

**Don't forget to set SMTP mail backend in settings**

```dotenv
# docker/dev/env/.email.env
EMAIL_HOST=<mailpit_hostname>
```

**Where `<mailpit_hostname>`:**
* `host.docker.internal` for Window and macOS
* `172.17.0.1` for Linux OS

---

### Production environment

If your server under LoadBalancer or nginx with SSL/TLS certificate you can run `prod.yml` configuration

```shell
docker-compose -f prod.yml up -d --build
```

or build image directly

```shell
docker build -t django-project -f docker/prod/web/Dockerfile .
```
