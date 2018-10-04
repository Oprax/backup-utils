.PHONY: build run

build: ./src/backup-utils/__main__.py
	pipenv run python -m zipapp -o ./dist/backup-utils.pyz ./src/backup-utils

run: build
	pipenv run python ./dist/backup-utils.pyz
