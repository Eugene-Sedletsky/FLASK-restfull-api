# Help target
help:
	@echo "Available targets"
	@echo "  setup       - Create virtual environment and install dependencies"
	@echo "  run         - run app"
	@echo "  debug       - run debug"
	@echo "  test        - Run tests with pytest"
	@echo "  lint        - run lint on code"
	@echo "  help        - Display this help message"


check_dependencies:
	@echo "Running hard check for dependencies..."
	poetry check
	poetry install --no-root --dry-run

install:
	poetry install --no-root

init: 
	poetry run flask init_db


setup: install init

test:
	poetry run python -m pytest --cov-report term-missing --cov=project

lint:
	poetry run pylint tests/ project/

run: check_dependencies
	poetry run flask --app app run

debug:
	poetry run flask --app app --debug run

