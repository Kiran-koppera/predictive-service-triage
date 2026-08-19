.PHONY: setup lint test run clean

VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

lint:
	$(PY) -m ruff check src tests

test:
	$(PY) -m pytest tests -v

run:
	$(PY) -m src.pipeline

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache **/__pycache__
