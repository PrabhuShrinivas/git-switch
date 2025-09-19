PY ?= python3
PIP ?= $(PY) -m pip
VENV ?= .venv

.PHONY: install build test test-file

install:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		if [ ! -d "$(VENV)" ]; then $(PY) -m venv $(VENV); fi; \
		. $(VENV)/bin/activate; \
		PIP_CMD=$(VENV)/bin/pip; PY_CMD=$(VENV)/bin/python; \
	else \
		PIP_CMD="$$VIRTUAL_ENV/bin/pip"; PY_CMD="$$VIRTUAL_ENV/bin/python"; \
	fi; \
	$$PY_CMD -m pip install -U pip; \
	$$PIP_CMD install -e .; \
	if [ -z "$$VIRTUAL_ENV" ]; then echo "To use the environment: source $(VENV)/bin/activate"; fi

build:
	$(PIP) install -U build twine
	rm -rf dist build *.egg-info
	$(PY) -m build

test:
	$(PIP) install -U -r requirements.txt
	$(PY) -m pytest -q --maxfail=1 --disable-warnings --cov=git_switch --cov-report=term-missing --cov-report=html

# Usage: make test-file FILE=tests/test_cli.py::test_name
test-file:
	@if [ -z "$(FILE)" ]; then echo "Usage: make test-file FILE=tests/test_cli.py[::test_name]"; exit 1; fi
	$(PY) -m pytest -q $(FILE)

