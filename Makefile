run:
	docker-compose up -d --force-recreate

build:
	docker-compose build --no-cache

stop:
	docker-compose stop
psql:
	docker-compose exec postgres psql -U postgres postgres