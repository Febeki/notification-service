# Notification Service (Django, DRF, React.js, Nginx, Celery, Gitlab-ci, Unittests (100% coverage), Docker)

### Getting Started:

- Install Docker

- `git clone https://gitlab.com/python883344/notification-service.git` - clone the repository

- Create .backend.env, .db.env, and .frontend.env files in the docker/dev/env folder


- `docker-compose up --build` - run the project

- go to http://127.0.0.1:3000/login/   to see Web UI. username: admin, password: 1

### Populate the Database with Test Data:

Create 6 clients with different time zones for testing

- `docker exec -it notification_service_django python manage.py shell` - launch the console

- `exec(open('setup_db.txt').read())` - populate the database

- `exit()` - exit from console

**Environment Configuration Examples**:

`.backend.env`:
- JWT_TOKEN - your jwt token for External service API (https://probe.fbrq.cloud/docs)

- SUPERUSER_USERNAME and SUPERUSER_PASSWORD - it will automatically create django admin superuser

```env
SECRET_KEY=ly+oy=jqkhq=roqerh++ob=nripq-hroir-bqoasp
DEBUG=1
DJANGO_ALLOWED_HOSTS=*

ENABLE_DEBUG_TOOLBAR=1

SQL_ENGINE=django.db.backends.postgresql

JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzAzMDQwMTQsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9EZW5fZ3Vkb2sifQ.NjlSPKYqR6KFuJ9DtmnKf-EgDmZSk6Q29YgHB3EQBm8

SUPERUSER_USERNAME=admin
SUPERUSER_PASSWORD=1
```

`.db.env`:

```env
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=test_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345
```

`.frontend.env`:

- REACT_APP_API_URL - your domain name + /api/.

- example for produciton: `https://domain.com/api/`

```env
REACT_APP_API_URL=http://127.0.0.1:8000/api/
```

### Additional Tasks:

- add testing
- Docker compose for start all services with 1 command
- add Swagger UI. path /docs/
- Add Web UI
