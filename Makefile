PY ?= python3
PIP ?= $(PY) -m pip
VENV ?= .venv

.PHONY: install build test test-file shell

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
	if [ -z "$$VIRTUAL_ENV" ]; then \
		if [ -z "$$NO_SHELL" ]; then \
			if [ -n "$$ZSH_NAME" ]; then SHELL_NAME=zsh; else SHELL_NAME=bash; fi; \
			echo "Launching interactive $$SHELL_NAME with venv activated. Exit to return."; \
			. $(VENV)/bin/activate; \
			exec $$SHELL_NAME -i; \
		else \
			echo "Virtual environment created at $(VENV). To activate: source $(VENV)/bin/activate"; \
		fi; \
	fi

# Start an interactive subshell with the venv activated
shell:
	@if [ ! -d "$(VENV)" ]; then $(PY) -m venv $(VENV); fi; \
	if [ -n "$$ZSH_NAME" ]; then \
		SHELL_NAME=zsh; \
	else \
		SHELL_NAME=bash; \
	fi; \
	echo "Launching $$SHELL_NAME with venv activated (. $(VENV)/bin/activate)"; \
	. $(VENV)/bin/activate; \
	$$SHELL_NAME -i

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

