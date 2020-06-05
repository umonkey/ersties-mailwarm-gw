NAME=mailwarm-bridge
TAG=latest
REPO=ersties/$(NAME)

build:
	docker build --tag $(REPO):$(TAG) .
	docker images

compose:
	docker-compose up

release: build
	docker push $(REPO):$(TAG)

run: build
	docker run --rm -p 1025:1025/tcp --name $(NAME) --env-file /etc/ersties/mailwarm-bridge.env $(REPO):$(TAG)

run-noapi: build
	mkdir -p var
	docker run --rm -p 1025:1025/tcp --name $(NAME) --mount type=bind,source=`pwd`/var,target=/var/bridge --env EXPERTSENDER_DUMP_FOLDER=/var/bridge $(REPO):$(TAG)

run-local:
	EXPERTSENDER_DUMP_FOLDER=`pwd`/var python3 src/server.py

shell: build
	docker run --rm -it $(REPO):$(TAG) /bin/bash

test:
	python3 src/test.py

.PHONY: test
