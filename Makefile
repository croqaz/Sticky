
ENV=./env/bin

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf cover
	python3 setup.py clean

update:
	${ENV}/pip install -U -r requirements-dev.txt

lint:
	${ENV}/flake8 sticky

coverage:
	${ENV}/pytest --cov-report term --cov=sticky tests/

test:
	${ENV}/pytest -ra --capture=no --verbose tests/

icky:
	${ENV}/python -m sticky.cli -s sticky/
