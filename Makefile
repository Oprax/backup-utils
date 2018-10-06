.PHONY: build run

build: ./src/backup_utils/__main__.py
	pipenv run python -m zipapp -o ./dist/backup_utils.pyz ./src/backup_utils

run: build
	pipenv run python ./dist/backup_utils.pyz

test:
	PYTHONPATH="${PYTHONPATH}:${PWD}/src" pipenv run pytest
