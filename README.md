# Notification Service (Django, DRF, React.js, Nginx, Celery, Gitlab-ci, Unittests (100% coverage), Docker, Oauth2)

### Getting Started:

- Install Docker

- `git clone https://gitlab.com/python883344/notification-service.git` - clone the repository

- Create .backend.env, .db.env, and .frontend.env files in the docker/dev/env folder


- `docker-compose up --build` - run the project

- go to http://127.0.0.1:3000/login/   to see Web UI. email: admin@gmail.com, password: 1

### Populate the Database with Test Data:

Create 6 clients with different time zones for testing

- `docker exec -it notification_service_django python manage.py shell` - launch the console

- `exec(open('setup_db.txt').read())` - populate the database

- `exit()` - exit from console

**Environment Configuration Examples**:

`.backend.env`:
- JWT_TOKEN - your jwt token for External service API (https://probe.fbrq.cloud/docs)

- SUPERUSER_EMAIL and SUPERUSER_PASSWORD - it will automatically create django admin superuser

```env
SECRET_KEY=ly+oy=jqkhq=roqerh++ob=nripq-hroir-bqqfk
DEBUG=1
DJANGO_ALLOWED_HOSTS=*

DJANGO_SETTINGS_MODULE=backend.settings_dev

ENABLE_DEBUG_TOOLBAR=1


SQL_ENGINE=django.db.backends.postgresql

JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzAzMDQwMTQsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9EZW5fZ3Vkb2sifQ.NjlSPKYqR6KFuJ9DtmnKf-EgDmZSk6Q29YgHB3EQBm8

SUPERUSER_EMAIL=admin@gmail.com
SUPERUSER_PASSWORD=1

OAUTH_REDIRECT_URL=http://localhost:3000/
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=YOUR_KEY_GOOGLE
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=YOUR_SECRET_GOOGLE
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

- REACT_APP_BACKEND_URL - your domain name.

- example for produciton: `https://domain.com/api/`

```env
REACT_APP_BACKEND_URL=http://127.0.0.1:8000/
```
