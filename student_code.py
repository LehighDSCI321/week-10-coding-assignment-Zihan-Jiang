"""
student_code.py

Implements SortableDigraph → TraversableDigraph → DAG
with DFS, BFS, and cycle–safe DAG edge insertion.
"""

from collections import deque


class SortableDigraph:
    """
    Base digraph class storing nodes with optional values,
    and adjacency list edges.
    """

    def __init__(self):
        # nodes: dict of name → value
        self.nodes = {}
        # edges: dict of name → set of children
        self.edges = {}

    def add_node(self, name, value=None):
        """
        Add a node with optional metadata value.
        """
        self.nodes[name] = value
        if name not in self.edges:
            self.edges[name] = set()

    def add_edge(self, u, v):
        """
        Add a directed edge u → v.
        (Will be overridden in DAG)
        """
        self.add_node(u)
        self.add_node(v)
        self.edges[u].add(v)

    def get_nodes(self):
        """
        Return a list of node names.
        """
        return list(self.nodes.keys())


class TraversableDigraph(SortableDigraph):
    """
    Adds DFS and BFS traversal methods to SortableDigraph.
    """

    def dfs(self, start):
        """
        Depth-first search traversal from `start`.
        Returns a list in DFS order.
        """
        visited = set()
        order = []

        def _visit(node):
            if node not in visited:
                visited.add(node)
                order.append(node)
                for nbr in self.edges.get(node, []):
                    _visit(nbr)

        _visit(start)
        return order

    def bfs(self, start):
        """
        Breadth-first search traversal from `start`.
        Yields nodes as visited.
        """
        visited = set([start])
        queue = deque([start])

        while queue:
            node = queue.popleft()
            yield node
            for nbr in self.edges.get(node, []):
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append(nbr)


class DAG(TraversableDigraph):
    """
    Directed acyclic graph.
    Overrides add_edge to prevent cycle creation.
    """

    def add_edge(self, u, v):
        """
        Add edge u → v only if it does not create a cycle.
        Raises ValueError if inserting the edge introduces a cycle.
        """
        self.add_node(u)
        self.add_node(v)

        # If v → ... → u already exists, adding u → v forms a cycle
        if self._has_path(v, u):
            raise ValueError(f"Adding edge {u} → {v} creates a cycle.")

        self.edges[u].add(v)

    def _has_path(self, start, goal):
        """
        Return True if there is a path start → ... → goal.
        DFS is used.
        """
        stack = [start]
        visited = set()

        while stack:
            node = stack.pop()
            if node == goal:
                return True
            if node not in visited:
                visited.add(node)
                for nbr in self.edges.get(node, []):
                    stack.append(nbr)
        return False

