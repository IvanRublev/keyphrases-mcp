# Development and testing

[← Back to README](../README.md)

## Development

Build from the source and install dependencies:

```sh
git clone https://github.com/IvanRublev/keyphrases-mcp.git
cd keyphrases-mcp
asdf install
uv venv --no-managed-python
uv sync --dev --locked
```

Run linters and tests with:

```sh
ruff check . 
pyrefly check .
pytest
```

## Integration testing

You can use the [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) for visual debugging of this MCP Server.

```sh
npx @modelcontextprotocol/inspector uv run src/main.py --allowed-dir <path_to_documents>
```

## Contributing
1. Fork the repo
2. Create a new branch (`feature-branch`)
3. Run linters and tests
4. Commit your changes
5. Push to your branch and submit a PR!

