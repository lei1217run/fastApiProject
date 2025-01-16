DOCKER_COMPOSE = sudo docker compose -f ./docker/docker-compose.yml -p project

.PHONY: build
build:
	${DOCKER_COMPOSE} build app

.PHONY: up
up: build
	APP_ENV=$(APP_ENV) ${DOCKER_COMPOSE} up --attach app

.PHONY: down
down: build
	${DOCKER_COMPOSE} down --volumes --rmi=local