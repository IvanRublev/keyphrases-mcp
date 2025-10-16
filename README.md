# 🔤 Keyphrases-MCP

*Empowering LLMs with authentic keyphrase Extraction*

*Available in:*

<a href="https://glama.ai/mcp/servers/@IvanRublev/keyphrases-mcp">
  Glama.ai<br><img width="380" height="200" src="https://glama.ai/mcp/servers/@IvanRublev/keyphrases-mcp/badge" />
</a> 

[![smithery badge](https://smithery.ai/badge/@IvanRublev/keyphrases-mcp)](https://smithery.ai/server/@IvanRublev/keyphrases-mcp)

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

1. **Candidate Generation**: **KeyphraseCountVectorizer** identifies meaningful keyphrase candidates using spaCy's **en_core_web_trf** model and discarding stop words
2. **Semantic Encoding**: Candidates and document are embedded using **paraphrase-multilingual-MiniLM-L12-v2** sentence transformer
3. **Relevance Ranking**: **KeyBERT** calculates cosine similarity between candidate keyphrase and document embeddings
4. **Diversity Selection**: **Maximal Marginal Relevance (MMR)** ensures diverse, non-redundant keyphrases
5. **Final Output**: Top N most relevant and diverse keyphrases are selected and sorted alphabetically

See configuration document for details.

## Documentation

- **[🚀 Integration](docs/integration.md)** - How to integrate server with your MCP client or LLM
- **[🔧 Configuration](docs/configuration.md)** - Environment variables and settings
- **[🛠️ MCP Tools](docs/mcp-tools.md)** - All available tools
- **[🪵 Development and testing](docs/roadmap.md)** - Guide on how to contribute to the project

## License
This project is licensed under the **MIT License**.

## Contact
For questions or support, reach out via [GitHub Issues](https://github.com/redis/mcp-redis/issues).
