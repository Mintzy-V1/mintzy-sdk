.PHONY: install test lint typecheck build clean

install:
	pip install -e '.[dev]'

test:
	pytest

lint:
	ruff check .

typecheck:
	mypy src/mintzy

build:
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache .ruff_cache .mypy_cache
