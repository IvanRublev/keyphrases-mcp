# Integration

[← Back to README](../README.md)

## OpenAI

Run the keyphrases-mcp server locally and expose it to the internet via `ngrok`:

> [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
 
> [ngrok Installation Guide](https://ngrok.com/docs/getting-started)

```sh
uvx --from git+https://github.com/IvanRublev/keyphrases-mcp.git keyphrases-mcp-server --allowed-dir <path_to_documents> --http
ngrok http 8000
```

Note the public URL (e.g., https://your-server.ngrok.io) for the next steps.

Add to ChatGPT with the following:
​
1. Enable Developer Mode
   Open ChatGPT and go to Settings → Connectors
   Under Advanced, toggle Developer Mode to enabled
​
2. Create Connector
   In Settings → Connectors, click Create
   Enter:
      Name: Keyphrases-MCP
      Server URL: https://your-server.ngrok.io/mcp/
    Check I trust this provider
    Click Create

Use in Chat

1. Start a new chat

2. Click the + button → More → Developer Mode
   Enable your MCP server connector (required - the connector must be explicitly added to each chat)

Now you can use the tool.

## With Docker

You can use a dockerized deployment of this server to provide access via Streamable HTTP transport to MCP clients as follows:

Build the image, it will take ~10 GB of the disk space.

```sh
docker build -f Dockerfile -t keyphrases-mcp .
```

Run the container exposing ports and documents directory (replace path_to_documents with appropriate path on your system)
to validate it's starting properly.

```sh
docker run --rm --name keyphrases-mcp-server -i -v <path_to_documents>:/app/documents -p 8000:8000 keyphrases-mcp:latest
```

To provide CUDA GPU acceleration to the app, add the `--gpus all` flag to the command above.

Add the following configuration to your MCP client settings with validated paths:

```json
{
    "mcpServers": {
        "docker-keyphrases-mcp-server": {
            "command": "docker",
            "args": [
            "run",
            "--rm",
            "--name", "keyphrases-mcp-server",
            "-i",
            "-v", "<path_to_documents>:/app/documents",
            "-p", "8000:8000",
            "keyphrases-mcp:latest"
            ]
        }
    }
}
```


## OpenAI Agents SDK

Integrate this MCP Server with the OpenAI Agents SDK. Read the [documents](https://openai.github.io/openai-agents-python/mcp/) to learn more about the integration of the SDK with MCP.

Install the Python SDK.

```sh
pip install openai-agents
```

Configure the OpenAI token:

```sh
export OPENAI_API_KEY="<openai_token>"
```

And run the [application](./openai_agents_sdk/keyphrases_assistant.py).

```sh
cd openai_agents_sdk && python keyphrases_assistant.py --allowed-dir <path_to_documents>
```

You can troubleshoot your agent workflows using the [OpenAI dashboard](https://platform.openai.com/traces/).


## Claude Desktop

Run the following command once to download embeddings and spaCy models.

> [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

```sh
<path_to_uvx>/bin/uvx --from git+https://github.com/IvanRublev/keyphrases-mcp.git keyphrases-mcp-server --download-models
```

Update the Claude configuration file on macOS: `~/Library/Application Support/Claude/claude_desktop_config.json` on windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add the kyphrases-mcp server configuration to run it from pypi org with `uvx`:
```json
{
  "mcpServers": {
    "keyphrases-mcp-server": {
        "type": "stdio",
        "command": "<path_to_uvx>/bin/uvx",
        "args": [
            "--from", "keyphrases-mcp",
            "keyphrases-mcp-server",
            "--allowed-dir", "<path_to_documents>"
        ]
    }
  }
}
```

Start the application. It will take some time do download ~1 GB of dependencies on the first launch.

Alternatively, you can clone the source code from the GitHub repository and start the server using `uv`. This is usually desired for development.
```json
{
  "mcpServers": {
    "keyphrases-mcp-server": {
        "type": "stdio",
        "command": "<path_to_uv>/bin/uv",
        "args": [
            "run",
            "--directory", "<path_to_keyphrases-mcp>/src",
            "-m", "main",
            "--allowed-dir", "<path_to_documents>"
        ]
    }
  }
}
```

