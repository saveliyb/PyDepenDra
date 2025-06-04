import argparse
from pathlib import Path
import logging

try:
    from .config import Config
    from .parser import PythonParser, collect_python_files
    from .analyzer import DependencyAnalyzer
    from .visualizer import GraphVisualizer
except ImportError:
    from config import Config
    from parser import PythonParser, collect_python_files
    from analyzer import DependencyAnalyzer
    from visualizer import GraphVisualizer


def collect_python_files(config: Config, base_dir: Path):
    """
    Recursively collects all Python files (.py) from the specified directory,
    ignoring files and directories listed in the configuration.

    Args:
        config (Config): Configuration object containing ignore rules.
        base_dir (Path): Root directory to start the search from.

    Returns:
        List[Path]: List of paths to the found Python files.
    """
    py_files = []
    for path in base_dir.iterdir():
        if config.is_ignored(str(path.resolve())):
            logging.debug(f"[IGNORED DIR/FILE] {path}")
            continue
        if path.is_dir():
            py_files.extend(collect_python_files(config, path))
        elif path.suffix == ".py":
            py_files.append(path)
    return py_files


def main():
    parser = argparse.ArgumentParser(description="PyDependra: Python code dependency analyzer.")
    parser.add_argument("--config", help="Path to config file (default looks for pydependra.yaml).")
    parser.add_argument("--ignore", help="Additional files to ignore (comma-separated).")
    parser.add_argument("--visualize", action="store_true", help="Generate dependency graph.")
    parser.add_argument("--root", default=".", help="Root directory for analysis (default: current directory).")
    parser.add_argument("--output", default="dependencies", help="Output filename or path for the graph.")
    parser.add_argument("--file", default="output.txt", help="File to save analysis results.")
    args = parser.parse_args()

    root_dir = Path(args.root).resolve()
    if not root_dir.is_dir():
        print(f"Error: Specified root directory '{root_dir}' does not exist or is not a directory.")
        return

    config = Config(args.config)
    if args.ignore:
        config.ignore_files.extend(args.ignore.split(","))

    parser = PythonParser(config)
    for py_file in collect_python_files(config, root_dir):
        parser.parse_file(str(py_file))

    analyzer = DependencyAnalyzer()
    analyzer.build_graph(parser.dependencies)

    output_file = Path(args.file).resolve()

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Dependencies:\n")
        file.write(f"{parser.dependencies}\n\n")
        file.write("Cycles:\n")
        file.write(f"{analyzer.get_cycles()}\n")

    print(f"Results saved to file: {output_file}")

    if args.visualize:
        print(parser.dependencies)
        visualizer = GraphVisualizer(parser.dependencies)
        visualizer.build_graph()
        visualizer.render("my_graph.html")


if __name__ == "__main__":
    main()
