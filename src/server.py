from anyio import to_thread
import logging
import os
from pathlib import Path
import time
import toml
import uvicorn

from mcp.types import ToolAnnotations
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from starlette.middleware.cors import CORSMiddleware

from src.config import PROJECT_ROOT, MAX_TEXT_LEN, MAX_KEYPHRASES_COUNT, HTTP_PORT, get_allowed_dirs
from src.core.extractor import extract_keyphrases as _extract_keyphrases

toml_path = PROJECT_ROOT / "pyproject.toml"
with open(toml_path, "r") as file:
    _pyproject_content = toml.load(file)


mcp = FastMCP("Keyphrases MCP Server", version=_pyproject_content["project"]["version"])
_logger = logging.getLogger(__name__)


def run_server_stdio():
    mcp.run(show_banner=False)


def run_server_streamable_http():
    app = mcp.http_app()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["mcp-session-id", "mcp-protocol-version"],
        max_age=86400,
    )
    uvicorn.run(app, host="0.0.0.0", port=HTTP_PORT, log_level="info")


@mcp.tool(
    annotations=ToolAnnotations(
        title="Extract Keyphrases",
        readOnlyHint=True,
        idempotentHint=True,
        openWorldHint=False,
    )
)
async def extract_keyphrases(file_path: str, keyphrases_count: int, stop_words: list[str] = []) -> list[str]:
    """
    Extracts keyphrases from the given text, excluding specified stop words.

    Args:
        file_path: The path to the input text file in the allowed directories from which to extract keyphrases.
        stop_words: A list of words to exclude from keyphrase extraction.
        keyphrases_count: The number of keyphrases to return.

    Returns:
        A list of extracted keyphrases.
    """
    file_path = str(Path(file_path).resolve())
    allowed_dirs = get_allowed_dirs()
    if not any(os.path.commonpath([file_path, allowed_dir]) == allowed_dir for allowed_dir in allowed_dirs):
        raise ToolError(
            f"File path '{file_path}' is not in allowed directories. "
            "Configure allowed directories with server launch parameters."
        )

    if not os.path.isfile(file_path):
        raise ToolError(f"File path '{file_path}' does not exist or is not pointing to a file.")

    text = ""
    try:
        text = open(file_path, "r").read()
    except Exception as e:
        raise ToolError(f"Extraction failed. {str(e)}")

    if len(text) > MAX_TEXT_LEN:
        raise ToolError(
            f"The input text can't be longer than {MAX_TEXT_LEN} characters. "
            + "Split the text and call the tool several times."
        )

    if keyphrases_count not in range(1, MAX_KEYPHRASES_COUNT):
        raise ToolError(f"The keyphrases count should be in 1..{MAX_KEYPHRASES_COUNT} range ({keyphrases_count}).")

    stop_words = list(filter(lambda item: len(item) > 0, stop_words))

    for word in stop_words:
        if " " in word:
            raise ToolError(f"Stop word can't contain spaces ({word}).")

    try:
        _logger.info(f"Extracting keywords from text of {len(text)} characters.")
        start_time = time.time()

        keyphrases = await _do_extract_keyphrases(text, keyphrases_count, stop_words)

        elapsed_time = time.time() - start_time
        _logger.info(f"Done in {elapsed_time:.2f} seconds.")

        return keyphrases
    except ValueError as e:
        if "Empty keyphrases" in str(e):
            raise ToolError("No keyphrases found in input text. Text is empty or only contain stop words.")
        else:
            raise ToolError(str(e))


async def _do_extract_keyphrases(text: str, keyphrases_count: int, stop_words: list[str] = []) -> list[str]:
    return await to_thread.run_sync(_extract_keyphrases, text, stop_words, keyphrases_count)
