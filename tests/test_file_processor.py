import pytest
from pathlib import Path

from main import common_init, keyphrases_from_textfile
from src.infra.logger_stdout import LoggerStdout

logger = LoggerStdout()


@pytest.fixture(scope="session", autouse=True)
def setup_once():
    common_init(logger, ())


def test_pass_keyphrases_from_textfile_should_return_keyphrases():
    file_path = Path(__file__).parent / "fixtures/transforming_human_capital.md"

    assert [
        "P+P model",
        "competitive advantage",
        "effective organizational practices",
        "financial performers",
        "human capital",
        "shareholder returns",
        "talent development",
    ] == keyphrases_from_textfile(str(file_path), 7, logger)
