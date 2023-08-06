all: lint test clean


.PHONY: venv
venv:
	python3.10 -m venv venv; \
	activate

.PHONY: activate
activate:
	. venv/bin/activate

.PHONY: dev
dev:
	venv; \
	pip install -e .[tests]; \
	pip install pre-commit tox

.PHONY: lint
lint:
	git add .
	activate; \
	pre-commit run --all-files

.PHONY: test
test:
	activate; \
	pytest tests -x -v --disable-warnings

.PHONY: tox
tox:
	tox

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf .tox
	rm -rf build
	rm -rf src/pythonic_dbm.egg-info

.PHONY: push
push:
	git push origin head

.PHONY: amend
amend:
	git add .
	git commit --amend --no-edit
	git push origin head -f

.PHONY: stable
stable:
	git checkout main
	git branch -D stable
	git checkout -b stable
	git push origin head -f
	git checkout main

.PHONY: git
git:
	git config --local user.email "hakancelikdev@gmail.com"
	git config --local user.name "Hakan Celik"

.PHONY: publish
publish:
	activate; \
	python -m pip install --upgrade pip; \
	python -m pip install --upgrade build; \
	python -m pip install --upgrade twine; \
	python -m build; \
	python -m twine upload dist/*

.PHONY: doc
doc:
	activate; \
	pip install -e .[docs]; \
	mkdocs serve
