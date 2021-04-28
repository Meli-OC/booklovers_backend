# wiseaty_api

# Features

Django et django rest framework with Python 3.9
Postgres13
Pytest for backend tests
Docker compose for easier development


# Development
The only dependencies for this project should be docker and docker-compose. When cloning, do for the first time:

- Enter your directory:

    - `cd booklovers_backend/`

- Create a secret key, tape in your terminal:

    - `openssl rand -hex 32`


- Create a .env.dev file with that syntax:
    - `DEBUG=1`
    - `DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]`
    - `POSTGRES_ENGINE=django.db.backends.postgresql` 
    - `SECRET_KEY=secret_key (copy/paste your terminal's code)`
    - `POSTGRES_USER=username`
    - `POSTGRES_PASSWORD=password`
    - `POSTGRES_HOST=wiseaty_db`
    - `POSTGRES_PORT=5432`
    - `POSTGRES_DB=database_name`

- Build your docker:
    - `docker-compose up --build`

- Create your tables:
    - `docker-compose exec booklovers python manage.py migrate`
    
- Create superuser:
    - `docker-compose exec booklovers python manage.py createsuperuser`

- To run tests:
    - `docker-compose exec wiseaty pytest -v`
    
- url:
    - login: localhost:8888/api/auth/login/
    - registration : localhost:8888/api/auth/registration/
    - facebook: localhost:8888/api/auth/facebook/