from pathlib import Path

from app.indexer.repository import scan_repository
from app.indexer.parser import parse_file
from app.indexer.index import index_repository


def test_scan_repository():
    files = scan_repository(".")

    assert "app\\main.py" in files
    assert "app\\indexer\\parser.py" in files
    assert all(".venv" not in file for file in files)


def test_parse_file():
    test_file = Path("test_parser_sample.py")

    test_file.write_text(
        "def add(a, b):\n"
        "    return a + b\n"
    )

    result = parse_file(str(test_file))

    assert result["root_node"] == "module"
    assert result["symbols"][0]["name"] == "add"
    assert result["symbols"][0]["type"] == "function"
    assert result["symbols"][0]["start_line"] == 1

    test_file.unlink()


def test_index_repository():
    result = index_repository(".")

    assert len(result) > 0
    assert any(
        file["file"] == "app\\indexer\\parser.py"
        for file in result
    )