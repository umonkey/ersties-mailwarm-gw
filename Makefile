build:
	docker build --tag mailwarm-bridge:v1 .
	docker images

run: build
	docker run --rm -p 1025:1025/tcp --name mailwarm-bridge mailwarm-bridge:v1

shell: build
	docker run --rm -it mailwarm-bridge:v1 /bin/bash

test:
	python3 src/test.py

.PHONY: test
