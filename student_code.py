"""
student_code.py
Implement TraversableDigraph and DAG
"""

from collections import deque


class SortableDigraph:
    """
    Base digraph: stores nodes + edges; supports topological sorting.
    """

    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, name, value=None):
        """
        Add a node with optional stored value.
        """
        self.nodes[name] = value
        if name not in self.edges:
            self.edges[name] = set()

    def add_edge(self, u, v):
        """
        Add directed edge u -> v.
        (Will be overridden in DAG)
        """
        self.add_node(u)
        self.add_node(v)
        self.edges[u].add(v)


class TraversableDigraph(SortableDigraph):
    """
    Adds DFS + BFS traversal methods.
    """

    def dfs(self, start):
        """
        Depth-first search, returning list of visited nodes
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
        Breadth-first search, yielding nodes as visited.
        """
        from collections import deque

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
    Directed acyclic graph — add_edge ensures no cycle.
    """

    def add_edge(self, u, v):
        """
        Add edge u → v, but only if it does not create a cycle.
        """
        self.add_node(u)
        self.add_node(v)

        # If v can reach u, then u->v creates a cycle
        if self._has_path(v, u):
            raise ValueError(f"Adding edge {u} → {v} creates a cycle.")

        self.edges[u].add(v)

    def _has_path(self, start, goal):
        """
        Return True if a path exists start → ... → goal
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
