.PHONY: install test run clean

VENV := .venv
PORT = 8000

ifeq ($(OS),Windows_NT)
	PYTHON := $(VENV)/Scripts/python
	PIP := $(VENV)/Scripts/pip
else
	PYTHON := $(VENV)/bin/python
	PIP := $(VENV)/bin/pip
endif

install:
	@echo "➡️ Installing dependencies..."
	@poetry install

test:
	@echo "🧪 Running tests..."
	@poetry run pytest

run:
	@echo "🚀 Running example..."
	@poetry run uvicorn src.main:app --reload

clean:
	@echo "🧹 Cleaning up build artifacts..."
	@rm -rf $(VENV)
	@poetry clean