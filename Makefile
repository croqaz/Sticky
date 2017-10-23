
ENV=./env/bin

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +

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
