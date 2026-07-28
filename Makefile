.PHONY: docker-build \
	docker-alltest \
	docker-decrypt \
	docker-doctest \
	docker-fasttest \
	docker-lint \
	docker-longtest \
	docker-release \
	docker-upload

NAME := ghost
VERSION := $(shell git rev-parse --short HEAD 2>/dev/null || echo "latest")
IMAGE := ghcr.io/anaticulae/$(NAME):$(VERSION)

WORKDIR := /var/workdir
TMP := /tmp/ghost

DOCKER_RUN := docker run \
	-v $(CURDIR):$(WORKDIR) \
	-v $(TMP):$(TMP)

docker-build:
	docker build -t $(IMAGE) .

docker-upload: docker-build
	docker push $(IMAGE)

docker-doctest: docker-build
	$(DOCKER_RUN) \
		$(IMAGE) \
		"baw test docs"

docker-fasttest: docker-decrypt
	$(DOCKER_RUN) \
		$(IMAGE) \
		"baw test fast"

docker-longtest: docker-decrypt
	$(DOCKER_RUN) \
		$(IMAGE) \
		"baw test long"

docker-alltest: docker-decrypt
	$(DOCKER_RUN) \
		$(IMAGE) \
		"baw test all"

docker-lint: docker-build
	$(DOCKER_RUN) \
		$(IMAGE) \
		"baw lint all"

docker-decrypt: docker-build
	$(DOCKER_RUN) \
		-e HOVERPOWER_STORE=$(WORKDIR)/hoverpower/repo \
		-e HOVERPOWER_SECRET \
		$(IMAGE) \
		"powerdownload && powerdecrypt"

docker-release: docker-build
	@if git describe --exact-match --tags HEAD >/dev/null 2>&1; then \
		echo "Current commit is already tagged. Skipping release."; \
	else \
		$(DOCKER_RUN) \
			-e GH_TOKEN \
			$(IMAGE) \
			"baw release --no_test --no_linter"; \
	fi
