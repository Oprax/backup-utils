.PHONY: build run test testdev clean install upload doc

clean:
	rm -rf src/*.egg-info
	rm -rf src/dist
	rm -rf src/bin
	rm -rf src/build

build: clean
	pipenv lock -r > requirements.txt
	pipenv run pip install -r requirements.txt --target dist/
	cp README.md dist/
	cp -a ./src/. ./dist/
	mkdir -p bin
	pipenv run shiv --site-packages dist --compressed -p "/usr/bin/env python3" -o ./bin/backup_utils.pyz -e backup_utils.main

run: build
	pipenv run python ./bin/backup_utils.pyz -v

test:
	PYTHONPATH="${PYTHONPATH}:${PWD}/src" pipenv run pytest --cov=backup_utils

testdev:
	PYTHONPATH="${PYTHONPATH}:${PWD}/src" pipenv run pytest -s -x

install: clean
	cd src && pipenv run python setup.py install

upload: clean
	cd src && pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload src/dist/*

doc:
	cd docs && pipenv run make html
