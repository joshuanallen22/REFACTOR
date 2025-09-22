.PHONY: format lint type test ci

format:
black src tests

lint:
ruff check src tests

type:
mypy src

test:
pytest

ci: format lint type test
