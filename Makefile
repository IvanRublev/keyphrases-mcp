.PHONY: venv deps deps-upgrade deps-add deps-add-dev lint format test watch watch-one pypi-build pypi-publish-test

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
	ruff check . && pyrefly check src

format:
	ruff format .

test:
	pytest

watch:
	ptw -- -s -vv

watch-one:
	ptw -- -s -vv -k "$(NAME)"

pypi-build:
	uv sync
	uv build

pypi-publish-test:
	twine upload --verbose --repository testpypi dist/*
	@echo "test with: pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ -v keyphrases-mcp"
	@echo "then run 'keyphrases-mcp-server' in the directory shown by 'pip show keyphrases-mcp'"
	@echo " "
	@echo "also you can test with: uvx --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --from keyphrases-mcp keyphrases-mcp-server --help"
