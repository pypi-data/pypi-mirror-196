.venv/bin/python3:
	python3 -m venv --prompt $(shell basename $(shell pwd)) .venv
	.venv/bin/pip install -U setuptools wheel pip pip-tools

# See `https://widdowquinn.github.io/coding/update-pypi-package/' for
# latest pypi upload info I reference.
pypi-upload: dist-files
	python -m twine upload dist/*

test-pypi-upload: dist-files
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

dist-files:
	rm -f dist/*
	python setup.py sdist bdist_wheel
