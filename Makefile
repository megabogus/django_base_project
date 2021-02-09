nope:
	$(error Invalid target)

check-env-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

up:
	docker-compose up -d --build

restart:
	docker-compose restart app

shell:
	docker-compose exec app ./manage.py shell

migrate:
	docker-compose exec app make migrate

admin:
	docker-compose exec app ./manage.py createsuperuser
