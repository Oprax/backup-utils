.PHONY: build run test testdev clean install upload doc

clean:
	rm -rf src/*.egg-info
	rm -rf src/dist
	rm -rf src/build

build: clean
	pipenv run python -m zipapp -m "backup_utils:main" -p "/usr/bin/env python3" -o ./dist/backup_utils.pyz ./src

run: build
	pipenv run python ./dist/backup_utils.pyz -v

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
