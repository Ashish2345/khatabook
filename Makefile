.PHONY: install
install:
	poetry install


.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: lint
lint:
	poetry run pre-commit run --all-files --verbose

.PHONY: shell
shell:
	poetry run python khata_core/manage.py shell

.PHONY: migrate
migrate:
	poetry run python khata_core/manage.py migrate

.PHONY: migrations
migrations:
	poetry run python khata_core/manage.py makemigrations

.PHONY: run-server
run-server:
	poetry run python khata_core/manage.py runserver

.PHONY: superuser
superuser:
	poetry run python khata_core/manage.py createsuperuser

.PHONY: update
update: install migrations migrate;

.PHONY: gitall
gitall:
	git add .
	git commit -m "$(m)"
	git push
