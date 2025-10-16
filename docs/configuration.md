# Configuration

[← Back to README](../README.md)

## Environment Variables

> **Note:** All variables below are optional. If not set, the server will use the default values shown.

| Variable                             | Description                                    | Default Value                           |
|--------------------------------------|------------------------------------------------|-----------------------------------------|
| MCP_KEYPHRASES_EMBEDDINGS_MODEL      | BERT embeddings model                          | `paraphrase-multilingual-MiniLM-L12-v2` |
| MCP_KEYPHRASES_SPACY_TOKENIZER_MODEL | spaCy tokenizer model                          | `en_core_web_trf`                       |
| MCP_KEYPHRASES_LOG_LEVEL             | Log lever                                      | `INFO`                                  |
| MCP_KEYPHRASES_MAX_TEXT_LEN          | Maximal length of the input text in characters | `6000`                                  |
| MCP_KEYPHRASES_MAX_KEYPHRASES_COUNT  | Maximal number of keyphrases to extract        | `elastic`                               |
| PORT                                 | HTTP port for MCP server                       | `apple_health_data`                     |


There are various [pretrained embedding models](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)
for BERT. The `"paraphrase-multilingual-MiniLM-L12-v2"` for multi-lingual documents or any other language that is used by default. You can specify `"all-MiniLM-L6-v2"` model for English documents.

The are various spaCy [pretrained models](https://spacy.io/models/en/#en_core_web_trf).

