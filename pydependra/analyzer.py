from typing import Dict, List
import networkx as nx


class DependencyAnalyzer:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, dependencies: Dict[str, List[str]]) -> None:
        """
        Builds a dependency graph based on the provided dependencies dictionary.

        Args:
            dependencies (Dict[str, List[str]]): A dictionary where keys are files,
            and values are lists of files they depend on.
        """
        for file, calls in dependencies.items():
            self.graph.add_node(file)
            for callee in calls:
                self.graph.add_edge(file, callee)

    def get_cycles(self) -> List[List[str]]:
        """
        Finds cycles in the dependency graph.

        Returns:
            List[List[str]]: A list of cycles, where each cycle is represented as a list of files.
        """
        return list(nx.simple_cycles(self.graph))
