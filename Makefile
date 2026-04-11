start:
	uv run python manage.py runserver 0.0.0.0:8000

render-start:
	uv run gunicorn task_manager.wsgi

build:
	./build.sh

install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --no-input

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=gendiff --cov-report=xml:coverage.xml

check:
	uv run python manage.py check
