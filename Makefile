up:
	docker compose up -d

upa:
	docker compose up api
	
down:
	docker compose down

rebuild:
	docker compose build --no-cache api

up-api:
	docker compose build --no-cache api
	docker compose up

build-api:
	docker compose build --no-cache api
