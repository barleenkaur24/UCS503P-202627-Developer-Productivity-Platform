from pathlib import Path

from app.indexer.parser import parse_file
from app.indexer.repository import scan_repository


def index_repository(repository_path: str) -> list[dict]:
    """
    Scan a repository and parse all supported source files.
    """

    root = Path(repository_path)

    files = scan_repository(repository_path)

    indexed_files = []

    for file_path in files:
        full_path = root / file_path

        parsed = parse_file(str(full_path))

        parsed["file"] = file_path

        indexed_files.append(parsed)

    return indexed_files