.PHONY: test
test:
	pytest --cov --cov-config=./tests/.coveragerc --cov-report=term-missing -n auto tests

.PHONY: reformat
reformat:
	ruff check . --fix
	black .

.PHONY: lint
lint:
	ruff . --no-fix
	black . --check

.PHONY: build
build:
	python3 -m build

.PHONY: init
init:
	pip install -e .
	pip install -U -r requirements.txt

.PHONY: init-demo
init-demo:
	-rm demo/db.sqlite3
	python demo/manage.py migrate
	DJANGO_SUPERUSER_PASSWORD="admin" python demo/manage.py createsuperuser  --username=admin --email=foo@bar.com --noinput