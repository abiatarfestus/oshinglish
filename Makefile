DJANGO = manage.py #Reference to the DJANGO.py script

help:
	make -h

venv: #Open the virtual environment shell
	poetry shell

check: # Check for inconsistencies using Black Formatter
	black --check --diff oshinglish

format: #Format code with Black and isort
	black oshinglish
	isort --profile black oshinglish

test: # Run tests with pytest
	cd onestop
	pytest

migrate: #Run migrations
	python $(DJANGO) makemigrations
	python $(DJANGO) migrate

runserver: #Run the Django localhost server
	python $(DJANGO) runserver

djangoshell: #Open the Django interactive shell
	python $(DJANGO) shell

lock: Pipfile #Update poetry.lock file
	poetry lock
