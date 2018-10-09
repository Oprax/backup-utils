.PHONY: build run

build: ./src/__main__.py
	pipenv run python -m zipapp -c -p "/usr/bin/env python3" -o ./dist/backup_utils.pyz ./src

run: build
	pipenv run python ./dist/backup_utils.pyz

test:
	PYTHONPATH="${PYTHONPATH}:${PWD}/src" pipenv run pytest
