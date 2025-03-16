Notification mailing service
=====

Project description
----------
The project is a service for working with customer data and managing message distribution.

The project is deployed in five Docker containers: a web application for the admin panel and API, a celery application for distribution, a postgresql database, a redis database, and an nginx server.

Models are configured for display in the admin panel.

System requirements
----------

* Python 3.8+
* Docker
* Works on Linux

Technology stack
----------

* Python 3.8+
* Django 3.1
* Django Rest Framework
* PostreSQL
* Nginx
* gunicorn
* Docker, Docker Compose
* Сelery
* Redis

Installing the project from the repository
----------
1. Cloning the repository:
```bash
git clone git@github.com:NikitaChalykh/backend.git

cd backend # Go to the directory with the project
```

2. Create a ```.env``` file using ```env.example``` as a template in the infra folder

3. Installing and running the service in the container:
```bash
docker-compose up -d
```

4. Launching migrations, collecting statics and creating a superuser:
```bash
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py collectstatic --no-input

docker-compose exec web python manage.py
```

Working with the project
----------
Documentation on the API service:

```http://127.0.0.1/redoc/```

```http://127.0.0.1/swagger/```

Service admin panel:

```http://127.0.0.1/admin/```
