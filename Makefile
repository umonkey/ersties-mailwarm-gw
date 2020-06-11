NAME=mailwarm-bridge
TAG=latest
REPO=ersties/$(NAME)

all:
	@echo "make build    -- prepare the image"
	@echo "make run      -- run the image"
	@echo "make shell    -- open bash in the running image"
	@echo "make release  -- publish image on docker hub"

build:
	docker build --tag $(REPO):$(TAG) .
	docker images

release: build
	docker push $(REPO):$(TAG)

run: build
	docker run --rm -p 1025:1025/tcp --name $(NAME) $(REPO):$(TAG)

run-local:
	EXPERTSENDER_DUMP_FOLDER=`pwd`/var python3 src/server.py

shell: build
	docker run --rm -it $(REPO):$(TAG) /bin/bash

test:
	python3 src/test.py

.PHONY: test
