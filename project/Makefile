nope:
	$(error Invalid target)

check-env-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

req:
	pip install --upgrade pip
	pip install -r requirements/common.txt

req-dev:
	pip install --upgrade pip
	pip install -r requirements/dev.txt

migrate:
	./manage.py makemigrations
	./manage.py migrate -v 3 --noinput

static:
	./manage.py collectstatic -l --noinput

app: migrate
	./manage.py runserver 0.0.0.0:8000

gunicorn: static migrate
	gunicorn \
		--bind 0.0.0.0:8000 \
		--workers 4 \
		apps.wsgi:application


celery:
	celery -A apps worker -l info -B -c 4

celery-beat:
	celery -A apps beats -L info

test:
	flake8
	pytest
