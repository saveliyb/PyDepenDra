import ast
from typing import Dict, List
import importlib.util
import chardet
from pathlib import Path
import logging


def detect_encoding(file_path: str) -> str:
    """
    Detects file encoding using the chardet library.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Detected file encoding or 'utf-8' as default.
    """
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result.get("encoding", "utf-8") or "utf-8"


class PythonParser:
    def __init__(self, config):
        self.config = config
        self.dependencies: Dict[str, List[str]] = {}

    def parse_file(self, file_path: str) -> None:
        """
        Parses the specified Python file and extracts function calls.

        Args:
            file_path (str): Path to the file to parse.
        """
        file_path = Path(file_path).resolve()

        if self.config.is_ignored(str(file_path)):
            logging.debug(f"[IGNORED] {file_path}")
            return

        try:
            encoding = detect_encoding(file_path)
            with open(file_path, "r", encoding=encoding) as f:
                tree = ast.parse(f.read())
        except (UnicodeDecodeError, SyntaxError) as e:
            logging.warning(f"[ERROR] Failed to parse {file_path}: {e}")
            return

        visitor = FunctionCallVisitor()
        visitor.visit(tree)
        self.dependencies[str(file_path)] = visitor.calls
        logging.info(f"[PARSED] {file_path} — found {len(visitor.calls)} calls")

    def is_external(self, module_name: str) -> bool:
        """
        Checks if a module is external (installed via site-packages).

        Args:
            module_name (str): Module name to check.

        Returns:
            bool: True if the module is external, False otherwise.
        """
        if module_name in self.config.ignore_deps:
            return True

        try:
            spec = importlib.util.find_spec(module_name)
            return spec.origin is None or "site-packages" in spec.origin
        except ImportError:
            return False


class FunctionCallVisitor(ast.NodeVisitor):
    """
    AST NodeVisitor class for extracting function calls.
    """
    def __init__(self):
        self.calls: List[str] = []

    def visit_Call(self, node):
        """
        Processes function call nodes in the AST.

        Args:
            node: Function call node.
        """
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.append(node.func.attr)
        self.generic_visit(node)


def collect_python_files(config, base_dir: Path) -> List[Path]:
    """
    Recursively collects all Python files (.py) from the specified directory,
    ignoring files and directories listed in the configuration.

    Args:
        config: Configuration object containing ignore rules.
        base_dir (Path): Root directory to start the search from.

    Returns:
        List[Path]: List of paths to found Python files.
    """
    py_files = []
    for path in base_dir.iterdir():
        try:
            full_path = path.resolve()
            if config.is_ignored(str(full_path)):
                logging.debug(f"[IGNORED DIR/FILE] {path}")
                continue
            if path.is_dir():
                py_files.extend(collect_python_files(config, path))
            elif path.suffix == ".py":
                py_files.append(path)
        except Exception as e:
            logging.warning(f"[SKIPPED] {path}: {e}")
    return py_files
