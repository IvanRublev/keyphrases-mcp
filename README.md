# 🔤 Keyphrases-MCP

*Empowering LLMs with authentic keyphrase Extraction*

*Available in:*

<a href="https://glama.ai/mcp/servers/@IvanRublev/keyphrases-mcp">
  Glama.ai<br><img width="380" height="200" src="https://glama.ai/mcp/servers/@IvanRublev/keyphrases-mcp/badge" />
</a>

*Built with the following tools and technologies:*

<img src="https://img.shields.io/badge/MCP-6A5ACD.svg?style=default&logo=data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjNkE1QUNEIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiI+PHJlY3Qgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2IiByeD0iNCIvPjx0ZXh0IHg9IjgiIHk9IjExIiBmb250LXNpemU9IjgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IndoaXRlIj5NQ1A8L3RleHQ+PC9zdmc+" alt="MCP"> <img src="https://img.shields.io/badge/PyTorch-EE4C2C.svg?style=default&logo=PyTorch&logoColor=white" alt="PyTorch"> <img src="https://img.shields.io/badge/Python-3776AB.svg?style=default&logo=Python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/uv-DE5FE9.svg?style=default&logo=uv&logoColor=white" alt="uv">

---

## Overview

This Keyphrases MCP Server is a **natural language interface** designed for agentic applications to extract keyphrasess from provided text. It integrates seamlessly with **MCP (Model Content Protocol) clients**, enabling AI-driven workflows to extract keyphrases more accurately and with higher relevance using the BERT machine learning model. It works directly with your local files in the allowed directories saving the context tokens for your agentic LLM. The application ensures secure document processing by exposing only extracted keyphrases to the MCP client, not the original file content.

Using this MCP Server, you can ask the following questions:

- "Extract 7 keyphrases from the file. [ABSOLUTE_FILE_PATH]"
- "Extract 3 keyphrases from the given file ignoring the stop words. Stop words: former, due, amount, [OTHER_STOP_WORDS]. File: [ABSOLUTE_FILE_PATH]"

Keyphrases help users quickly grasp the main topics and themes of a document without reading it in full and enable the following applications:

1. tags or metadata for documents, improving organization and discoverability in digital libraries
2. emerging trends, sentiment, identified from customer reviews, social media, or news articles 
3. features or inputs for other tasks, such as text classification, clustering


## Reasoning for keyphrases-mcp

Autoregressive LLM models such as in Claude or ChatGPT process text sequentially, which—not only limits their ability to fully contextualize keyphrases across the entire document—but also suffers from context degradation as the input length increases, causing earlier keyphrases to receive diluted attention.

Bidirectional models like BERT, by considering both left and right context and maintaining more consistent attention across the sequence, generally extract existing keyphrases from texts more accurately and with higher relevance especially when no domain-specific fine-tuning is applied. 

However, as autoregressive models adopt longer context windows and techniques such as input chunking, their performance in keyphrase extraction is improving, narrowing the gap with BERT. And domain-specific fine-tuning can make autoregressive LLM model to outperform the BERT solution.

This MCP server combines BERT for keyphrase extraction with an autoregressive LLM for text generation or refinement, enabling seamless text processing.

## How it works

The server uses a KeyBERT framework for the multi-step extraction pipeline combining spaCy NLP preprocessing with BERT embeddings:

1. **Candidate Generation**: **KeyphraseCountVectorizer** identifies meaningful keyphrase candidates using spaCy's **en_core_web_trf** 
[model](https://spacy.io/models/en/#en_core_web_trf) and discarding stop words
2. **Semantic Encoding**: Candidates and document are embedded using **paraphrase-multilingual-MiniLM-L12-v2** sentence transformer
3. **Relevance Ranking**: **KeyBERT** calculates cosine similarity between candidate keyphrase and document embeddings
4. **Diversity Selection**: **Maximal Marginal Relevance (MMR)** ensures diverse, non-redundant keyphrases
5. **Final Output**: Top N most relevant and diverse keyphrases are selected and sorted alphabetically

There are various [pretrained embedding models](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)
for BERT. The `"paraphrase-multilingual-MiniLM-L12-v2"` for multi-lingual documents or any other language that is used by default. 

You can specify `"all-MiniLM-L6-v2"` model for English documents by exporting `MCP_KEYPHRASES_EMBEDDINGS_MODEL`
environment variable (see the `src/config.py` for details). 



## Integration

### OpenAI

Run the keyphrases-mcp server locally and expose it to the internet via `ngrok`:

```sh
uvx --from git+https://github.com/IvanRublev/keyphrases-mcp.git start-mcp-server --allowed-dir <path_to_documents> --http
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

### With Docker

You can use a dockerized deployment of this server to provide access via Streamable HTTP transport to MCP clients as follows:

Build the image, it will take ~10 GB of the disk space.

```sh
docker build -f Dockerfile-deploy -t keyphrases-mcp .
```

Run the container exposing ports, temporary directory to store the embeddings model, and documents directory.

```sh
docker run --rm --name keyphrases-mcp-server -i -v <tmp_directory_path>/embedding_model:/app/embedding_model -v <path_to_documents>:/app/documents -p 8000:8000 keyphrases-mcp:latest
````

### OpenAI Agents SDK

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


### Claude Desktop

Run the following command once to download embeddings model.

```sh
<path_to_uvx>/bin/uvx --from git+https://github.com/IvanRublev/keyphrases-mcp.git keyphrases-mcp-server --download-embeddings
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
            "--from", "git+https://github.com/IvanRublev/keyphrases-mcp.git",
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

## Development

Build from the source and intsall dependencies:

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

## License
This project is licensed under the **MIT License**.

## Contact
For questions or support, reach out via [GitHub Issues](https://github.com/redis/mcp-redis/issues).
