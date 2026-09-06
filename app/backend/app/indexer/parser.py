from tree_sitter import Language, Parser
import tree_sitter_python
import tree_sitter_javascript


PYTHON_LANGUAGE = Language(tree_sitter_python.language())
JAVASCRIPT_LANGUAGE = Language(tree_sitter_javascript.language())


def get_language(file_path: str) -> Language | None:
    """Return the Tree-sitter language for a supported file."""

    if file_path.endswith(".py"):
        return PYTHON_LANGUAGE

    if file_path.endswith((".js", ".jsx", ".ts", ".tsx")):
        return JAVASCRIPT_LANGUAGE

    return None


def parse_file(file_path: str) -> dict:
    """Parse a source file and extract important code structures."""

    language = get_language(file_path)

    if language is None:
        raise ValueError(f"Unsupported file type: {file_path}")

    parser = Parser(language)

    with open(file_path, "rb") as file:
        source_code = file.read()

    tree = parser.parse(source_code)

    symbols = []

    def extract_symbols(node):
        if node.type in {"function_definition", "class_definition"}:
            name_node = node.child_by_field_name("name")

            symbols.append({
                "type": "function" if node.type == "function_definition" else "class",
                "name": source_code[name_node.start_byte:name_node.end_byte].decode("utf-8"),
                "start_line": node.start_point.row + 1,
                "end_line": node.end_point.row + 1,
            })

        for child in node.children:
            extract_symbols(child)

    extract_symbols(tree.root_node)

    return {
        "file": file_path,
        "root_node": tree.root_node.type,
        "symbols": symbols,
    }