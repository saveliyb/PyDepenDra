# PyDepenDra - Python Dependency Analysis Toolkit

**PyDepenDra** is a static analysis tool that maps and visualizes dependencies in Python projects. It helps maintain clean architecture by revealing import patterns and circular dependencies.

## 🌟 Key Features

- Dependency graph generation with various visualization options
- Circular dependency detection with detailed reporting
- Configurable module exclusion patterns
- Support for both application and library projects
- Export results in multiple formats (HTML, JSON)

## 📦 Installation

```
git clone https://github.com/saveliyb/pydependra
cd pydependra
pip install -r requirements.txt
```

## 🚀 Quick Start

Analyze your project:

```
python -m pydependra.cli --root "your/root/dir/project" --config ""your/root/dir/project/pydependra.yaml" --visualize --output ""your/root/dir/project/vizual"
```

##  ⚙️ Configuration

Create `PyDepenDra.yaml` in your project root:

```
ignore:
  files:
    - "venv/**"
    - "**/tests/**"
    - "**/venv/**"
    - "main.py"
    - "**/lib/**"
    - "lib/**"
  dependencies:
    - "pytest"
```

## 📊 Sample Output

![image](https://github.com/user-attachments/assets/12d8e9b0-92e0-46bf-bacd-58977725fe9b)

### Text report example:

```
Dependencies:
{'\your\root\dir\projectPyDepenDra\\pydependra\\analyzer.py': ['DiGraph', 'items', 'add_node', 'add_edge', 'list', 'simple_cycles'], '\your\root\dir\projectPyDepenDra\\pydependra\\cli.py': ['iterdir', 'is_ignored', 'str', 'resolve', 'debug', 'is_dir', 'extend', 'collect_python_files', 'append', 'ArgumentParser', 'add_argument', 'add_argument', 'add_argument', 'add_argument', 'add_argument', 'add_argument', 'parse_args', 'resolve', 'Path', 'is_dir', 'print', 'Config', 'extend', 'split', 'PythonParser', 'collect_python_files', 'parse_file', 'str', 'DependencyAnalyzer', 'build_graph', 'resolve', 'Path', 'open', 'write', 'write', 'write', 'write', 'get_cycles', 'print', 'print', 'GraphVisualizer', 'build_graph', 'render', 'main'], '\your\root\dir\projectPyDepenDra\\pydependra\\config.py': ['_find_config', '_load_config', 'rglob', 'cwd', 'str', 'open', 'safe_load', 'debug', 'get', 'get', 'debug', 'get', 'get', 'resolve', 'Path', 'resolve', 'cwd', 'relative_to', 'lower', 'replace', 'str', 'debug', 'lower', 'replace', 'debug', 'fnmatch', 'debug', 'debug'], '\your\root\dir\projectPyDepenDra\\pydependra\\parser.py': ['open', 'detect', 'read', 'get', 'resolve', 'Path', 'is_ignored', 'str', 'debug', 'detect_encoding', 'open', 'parse', 'read', 'warning', 'FunctionCallVisitor', 'visit', 'str', 'info', 'len', 'find_spec', 'isinstance', 'append', 'isinstance', 'append', 'generic_visit', 'iterdir', 'resolve', 'is_ignored', 'str', 'debug', 'is_dir', 'extend', 'collect_python_files', 'append', 'warning'], '\your\root\dir\projectPyDepenDra\\pydependra\\visualizer.py': ['Network', 'toggle_physics', 'items', 'Path', 'add_node', 'add_node', 'add_edge', 'endswith', 'set_options', 'write_html', 'print', 'abspath'], '\your\root\dir\projectPyDepenDra\\pydependra\\__init__.py': []}

Cycles:
[]
```

## 🌐 Viewing HTML Reports

After generating the HTML visualization, you can quickly view it using Python's built-in HTTP server:

### Start HTTP server (in the same directory)

```
python -m http.server 8000
```

### Open in browser:

```
http://localhost:8000/deps_graph.html
```
