.PHONY: build run test testdev clean install upload doc uploadbin

clean:
	rm -rf src/*.egg-info
	rm -rf src/dist
	rm -rf ./dist
	rm -rf ./bin
	rm -rf src/build

build: clean
	poetry export -f requirements.txt -o requirements.txt
	poetry run pip install -r requirements.txt --target dist/
	cp README.md dist/
	cp -a ./src/. ./dist/
	mkdir -p bin
	poetry run shiv --site-packages dist --compressed -p "/usr/bin/env python3" -o ./bin/backup_utils.pyz -e backup_utils.main

run: build
	poetry run python ./bin/backup_utils.pyz -v

test:
	PYTHONPATH="${PYTHONPATH}:${PWD}/src" poetry run pytest --cov-report=xml --cov=backup_utils

testdev:
	PYTHONPATH="${PYTHONPATH}:${PWD}/src" poetry run pytest -s -x

install: clean
	cd src && poetry run python setup.py install

upload: clean
	poetry publish --build 

uploadbin: build
	./upload-bin.sh

doc:
	cd docs && poetry run make html
