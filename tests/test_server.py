import pytest
import tempfile
import shutil
from pathlib import Path

from fastmcp.exceptions import ToolError
from fastmcp import Client

from main import common_init
from src.server import mcp
from src.infra.logger_stdout import LoggerStdout


@pytest.fixture(scope="session")
def session_tmp_path():
    """Create a temporary directory for the test session and ensure cleanup on exit."""
    tmp_dir = tempfile.mkdtemp(prefix="keyphrases_mcp_test_")
    tmp_path = Path(tmp_dir)

    yield tmp_path

    # Cleanup: remove the temporary directory and all its contents
    if tmp_path.exists():
        shutil.rmtree(tmp_path)


@pytest.fixture(scope="session", autouse=True)
def client(session_tmp_path):
    common_init(LoggerStdout(), (str(session_tmp_path),))
    return Client(mcp)


@pytest.fixture(scope="session")
def capital_md_path(session_tmp_path):
    file_path = Path(__file__).parent / "fixtures/transforming_human_capital.md"
    target_path = session_tmp_path / file_path.name
    shutil.copy(file_path, target_path)
    return target_path


@pytest.fixture
def temp_text_file(session_tmp_path):
    def _create_file(text):
        file_path = session_tmp_path / "temp_text_file.txt"
        file_path.write_text(text, encoding="utf-8")
        return file_path

    return _create_file


@pytest.mark.asyncio
async def test_pass_extract_keyphrases_tool_is_available(mocker, client):
    async with client:
        await client.ping()

        tools = await client.list_tools()

        assert len(tools) == 1
        tool = tools[0]
        assert "extract_keyphrases" == tool.name


@pytest.mark.asyncio
async def test_pass_extract_keyphrases_given_empty_text_returns_empty_list(client, temp_text_file):
    path = temp_text_file("")
    async with client:
        result = await client.call_tool("extract_keyphrases", {"file_path": path, "keyphrases_count": 7})
        assert [] == result.data


@pytest.mark.asyncio
async def test_fail_extract_keyphrases_given_nonexisting_file_path(client, session_tmp_path):
    file_path = session_tmp_path / "nonexisting-path.txt"
    async with client:
        with pytest.raises(ToolError) as e:
            await client.call_tool("extract_keyphrases", {"file_path": file_path, "keyphrases_count": 7})

        assert "is not pointing to a file" in str(e.value)


@pytest.mark.asyncio
async def test_fail_extract_keyphrases_given_path_pointing_to_direcotry(client, session_tmp_path):
    directory_path = session_tmp_path / "directory"
    directory_path.mkdir()

    async with client:
        with pytest.raises(ToolError) as e:
            await client.call_tool("extract_keyphrases", {"file_path": directory_path, "keyphrases_count": 7})

        assert "is not pointing to a file" in str(e.value)


@pytest.mark.asyncio
async def test_fail_extract_keyphrases_given_file_path_out_of_allowed_directory(client):
    file_path = "some/other/path"
    async with client:
        with pytest.raises(ToolError) as e:
            await client.call_tool("extract_keyphrases", {"file_path": file_path, "keyphrases_count": 7})

        assert "is not in allowed directories" in str(e.value)


@pytest.mark.asyncio
async def test_pass_extract_keyphrases_return_keyphrases(client, capital_md_path):
    async with client:
        keyphrases = await client.call_tool("extract_keyphrases", {"file_path": capital_md_path, "keyphrases_count": 7})

        assert [
            "P+P model",
            "competitive advantage",
            "effective organizational practices",
            "financial performers",
            "human capital",
            "shareholder returns",
            "talent development",
        ] == keyphrases.data


@pytest.mark.asyncio
async def test_pass_extract_keyphrases_given_stop_words_respects_them(client, capital_md_path):
    async with client:
        keyphrases = await client.call_tool(
            "extract_keyphrases", {"file_path": capital_md_path, "keyphrases_count": 7, "stop_words": ["P+P"]}
        )

        assert [
            "competitive advantage",
            "effective organizational practices",
            "financial performers",
            "higher job satisfaction",
            "human capital",
            "shareholder returns",
            "talent development",
        ] == keyphrases.data


@pytest.mark.asyncio
async def test_pass_extract_keyphrases_given_empty_stop_words_discards_them(client, mocker, capital_md_path):
    mock_extract = mocker.patch("src.server._do_extract_keyphrases", return_value=["mocked"])

    async with client:
        result = await client.call_tool(
            "extract_keyphrases", {"file_path": capital_md_path, "keyphrases_count": 7, "stop_words": ["P+P", ""]}
        )

        assert ["mocked"] == result.data
        mock_extract.assert_called_once()
        assert mock_extract.call_args[0][2] == ["P+P"]


@pytest.mark.asyncio
async def test_fail_extract_keyphrases_given_invalid_stop_word(client, capital_md_path):
    async with client:
        with pytest.raises(ToolError) as e:
            await client.call_tool(
                "extract_keyphrases", {"file_path": capital_md_path, "keyphrases_count": 7, "stop_words": ["P+P word"]}
            )

        assert str(e.value) == "Stop word can't contain spaces (P+P word)."


@pytest.mark.asyncio
async def test_fail_extract_keyphrases_given_text_longer_6K_chars(client, temp_text_file):
    long_text = "a" * 6_001
    file_path = temp_text_file(long_text)

    async with client:
        with pytest.raises(ToolError) as e:
            await client.call_tool("extract_keyphrases", {"file_path": file_path, "keyphrases_count": 7})

        assert (
            str(e.value)
            == "The input text can't be longer than 6000 characters. Split the text and call the tool several times."
        )


@pytest.mark.asyncio
async def test_fail_extract_keyphrases_given_invalid_number_of_keyphrases(client, capital_md_path):
    async with client:
        with pytest.raises(ToolError) as e:
            await client.call_tool("extract_keyphrases", {"file_path": capital_md_path, "keyphrases_count": 0})

        assert str(e.value) == "The keyphrases count should be in 1..200 range (0)."

    async with client:
        with pytest.raises(ToolError) as e:
            await client.call_tool("extract_keyphrases", {"file_path": capital_md_path, "keyphrases_count": 201})

        assert str(e.value) == "The keyphrases count should be in 1..200 range (201)."


@pytest.mark.asyncio
async def test_fail_extract_keyphrases_given_text_same_to_stopwords(client, temp_text_file):
    file_path = temp_text_file("hello world")

    async with client:
        with pytest.raises(ToolError) as e:
            await client.call_tool(
                "extract_keyphrases", {"file_path": file_path, "keyphrases_count": 7, "stop_words": ["hello", "world"]}
            )

        assert str(e.value) == "No keyphrases found in input text. Text is empty or only contain stop words."
