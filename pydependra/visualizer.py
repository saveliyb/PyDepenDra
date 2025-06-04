from typing import Dict, List
from pathlib import Path
from pyvis.network import Network
import os


class GraphVisualizer:
    def __init__(self, dependencies: Dict[str, List[str]]):
        """
        Initializes the GraphVisualizer object.

        Args:
            dependencies (Dict[str, List[str]]): Dictionary of dependencies where keys are files,
            and values are lists of files they depend on.
        """
        self.dependencies = dependencies
        self.graph = Network(height="800px", width="100%", directed=True)
        self.graph.toggle_physics(True)

    def build_graph(self) -> None:
        """
        Builds the graph from dependencies, adding nodes and connections between them.
        """
        for filepath, deps in self.dependencies.items():
            # Use short filename
            file_node = Path(filepath).name
            self.graph.add_node(file_node, label=file_node, shape="box", color="#ADD8E6")

            for dep in deps:
                # Remove duplicate nodes even if they repeat
                self.graph.add_node(dep, label=dep, color="#90EE90")
                self.graph.add_edge(file_node, dep)

    def render(self, filename: str = "dependencies.html") -> None:
        """
        Saves the graph as an interactive HTML file.

        Args:
            filename (str): Filename to save the graph. Defaults to "dependencies.html".
        """
        if not filename.endswith(".html"):
            filename += ".html"
        self.graph.set_options("""
        {
          "physics": {
            "enabled": true,
            "stabilization": {
              "iterations": 1000,
              "updateInterval": 25
            }
          },
          "layout": {
            "improvedLayout": true
          }
        }
        """)
        self.graph.write_html(filename)
        print(f"Interactive graph saved to: {os.path.abspath(filename)}")
