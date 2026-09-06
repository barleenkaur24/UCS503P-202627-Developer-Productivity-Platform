from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
}


def scan_repository(repository_path: str) -> list[str]:
    """
    Scan a repository and return supported source-code files.
    """

    root = Path(repository_path)

    if not root.exists():
        raise ValueError(f"Repository does not exist: {repository_path}")

    if not root.is_dir():
        raise ValueError(f"Path is not a directory: {repository_path}")

    files = []

    for file_path in root.rglob("*"):
        if any(part in IGNORED_DIRECTORIES for part in file_path.parts):
            continue

        if file_path.is_file() and file_path.suffix in SUPPORTED_EXTENSIONS:
            files.append(str(file_path.relative_to(root)))

    return sorted(files)