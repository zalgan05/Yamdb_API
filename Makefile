
include .env

PROJECT_NAME = api_yamdb

.ONESHELL:

git_auth:
	git config user.name "${GIT_USERBANE}"
	git config user.email "${GIT_EMAIL}"

run:
	cd ${PROJECT_NAME}
	python manage.py runserver

lint:
	isort ${PROJECT_NAME}
	black ${PROJECT_NAME}
	flake8 ${PROJECT_NAME} --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 ${PROJECT_NAME} --count --exit-zero --max-complexity=10 --max-line-length=79 --statistics --config=setup.cfg

test: djtest
	pytest
