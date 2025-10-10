.PHONY: venv deps deps-upgrade deps-add deps-add-dev lint format test watch watch-one

venv:
	uv venv --no-managed-python

deps:
	uv sync --dev --locked

deps-upgrade:
	uv lock --upgrade

deps-add:
	uv add "$(NAME)"

deps-add-dev:
	uv add --dev "$(NAME)" 

lint:
	ruff check . && pyrefly check .

format:
	ruff format .

test:
	pytest

watch:
	ptw -- -s -vv

watch-one:
	ptw -- -s -vv -k "$(NAME)"
