.PHONY: build run test testdev clean install upload doc

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
	PYTHONPATH="${PYTHONPATH}:${PWD}/src" poetry run pytest --cov=backup_utils

testdev:
	PYTHONPATH="${PYTHONPATH}:${PWD}/src" poetry run pytest -s -x

install: clean
	cd src && poetry run python setup.py install

upload: clean
	cd src && poetry run python setup.py sdist bdist_wheel
	poetry run twine upload src/dist/*

doc:
	cd docs && poetry run make html
