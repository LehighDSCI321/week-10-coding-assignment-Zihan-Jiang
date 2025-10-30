
from collections import deque


class SortableDigraph:
    """
    Minimal parent class placeholder.
    We assume the real class already supports:
       - self.nodes: set
       - self.edges: dict of {u : set of neighbors}
       - add_node()
       - add_edge()       (will be overridden in DAG)
       - topological sort
    """

    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes.add(name)
            self.edges[name] = set()

    def add_edge(self, u, v):
        """Normal directed edge insertion — overridden in DAG."""
        self.add_node(u)
        self.add_node(v)
        self.edges[u].add(v)


# =====================================================
# TraversableDigraph
# =====================================================

class TraversableDigraph(SortableDigraph):

    def dfs(self, start):
        """
        Depth-first search – returns a list of visited nodes.
        (Based on Listing 5-5 from Python Algorithms.)
        """
        visited = set()
        res = []

        def _visit(node):
            if node not in visited:
                visited.add(node)
                res.append(node)
                for nbr in self.edges.get(node, []):
                    _visit(nbr)

        _visit(start)
        return res

    def bfs(self, start):
        """
        Breadth-first search – should YIELD visited nodes.
        Uses deque per assignment.
        """
        visited = set()
        queue = deque([start])

        visited.add(start)

        while queue:
            node = queue.popleft()
            yield node      # REQUIRED by assignment

            for nbr in self.edges.get(node, []):
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append(nbr)


# =====================================================
# DAG
# =====================================================

class DAG(TraversableDigraph):
    """
    Directed acyclic graph.
    Overrides add_edge so cycles are never introduced.
    """

    def add_edge(self, u, v):
        """
        Checks if adding u -> v creates a cycle.
        If yes → raise Exception.
        Else → perform the insertion.
        """
        self.add_node(u)
        self.add_node(v)

        # If v can reach u, then adding u->v forms a cycle.
        if self._has_path(v, u):
            raise Exception(f"Adding edge {u} -> {v} creates a cycle!")

        # Safe to add
        self.edges[u].add(v)

    def _has_path(self, start, goal):
        """
        Helper DFS test – is there a path start → … → goal?
        """
        visited = set()
        stack = [start]

        while stack:
            node = stack.pop()
            if node == goal:
                return True
            if node not in visited:
                visited.add(node)
                for nbr in self.edges.get(node, []):
                    stack.append(nbr)

        return False
