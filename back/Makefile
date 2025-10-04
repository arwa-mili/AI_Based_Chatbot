# Variables
SHELL := /bin/bash
ENV_FILE=.env.docker
PYTHON=python3
PIP=pip
DJANGO_MANAGE=$(PYTHON) manage.py

# Docker commands
up:
	docker compose --env-file $(ENV_FILE) up -d

down:
	docker compose --env-file $(ENV_FILE) down

logs:
	docker compose logs -f

# Django commands
run:
	source venv/bin/activate && $(DJANGO_MANAGE) runserver

migrate:
	source venv/bin/activate && $(DJANGO_MANAGE) migrate

makemigrations:
	source venv/bin/activate && $(DJANGO_MANAGE) makemigrations

createsuperuser:
	source venv/bin/activate && $(DJANGO_MANAGE) createsuperuser

# Python package management
install:
	source venv/bin/activate && $(PIP) install -r requirements.txt

freeze:
	source venv/bin/activate && $(PIP) freeze > requirements.txt

activate:
	source venv/bin/activate

# Init project
init:
	python3 -m venv venv
	source venv/bin/activate
