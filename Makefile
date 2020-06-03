build:
	docker build --tag mailwarm-bridge:v1 .
	docker images

compose:
	docker-compose up

run: build
	docker run --rm -p 1025:1025/tcp --name mailwarm-bridge --env-file /etc/ersties/mailwarm-bridge.env mailwarm-bridge:v1

run-noapi: build
	mkdir -p var
	docker run --rm -p 1025:1025/tcp --name mailwarm-bridge --mount type=bind,source=`pwd`/var,target=/var/bridge --env EXPERTSENDER_DUMP_FOLDER=/var/bridge mailwarm-bridge:v1

run-local:
	EXPERTSENDER_DUMP_FOLDER=`pwd`/var python3 src/server.py

shell: build
	docker run --rm -it mailwarm-bridge:v1 /bin/bash

test:
	python3 src/test.py

.PHONY: test
