"""
student_code.py

Implements SortableDigraph → TraversableDigraph → DAG
with DFS, BFS, topological sorting, and cycle–safe DAG edge insertion.
"""

from collections import deque


class SortableDigraph:
    """
    Base digraph class storing nodes with optional values,
    and adjacency list edges including optional weights.
    """

    def __init__(self):
        # nodes: dict of name → value
        self.nodes = {}
        # edges: dict of name → dict of child → weight
        self.edges = {}

    def add_node(self, name, value=None):
        """
        Add a node with optional metadata value.
        """
        self.nodes[name] = value
        if name not in self.edges:
            self.edges[name] = {}

    def add_edge(self, u, v, edge_weight=None):
        """
        Add a directed edge u → v with optional weight.
        """
        self.add_node(u)
        self.add_node(v)
        self.edges[u][v] = edge_weight

    def get_nodes(self):
        """
        Return a list of node names.
        """
        return list(self.nodes.keys())

    def get_node_value(self, name):
        """
        Return the stored value of node `name`.
        Raises KeyError if the node does not exist.
        """
        if name not in self.nodes:
            raise KeyError(f"Node '{name}' does not exist.")
        return self.nodes[name]

    def top_sort(self):
        """
        Perform topological sort on the digraph.
        Raises ValueError if a cycle is present.
        """
        indegree = {n: 0 for n in self.nodes}

        # Count indegree
        for parent in self.edges:
            for child in self.edges[parent]:
                indegree[child] += 1

        # Start with zero-indegree nodes
        queue = deque(sorted([n for n in indegree if indegree[n] == 0]))
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for nbr in self.edges.get(node, {}):
                indegree[nbr] -= 1
                if indegree[nbr] == 0:
                    queue.append(nbr)

        if len(result) != len(self.nodes):
            raise ValueError("Graph has a cycle; cannot topologically sort.")

        return result


class TraversableDigraph(SortableDigraph):
    """
    Adds DFS and BFS traversal methods to SortableDigraph.
    """

    def dfs(self, start):
        """
        Depth-first search traversal from `start`.
        Returns a list in DFS order, excluding start itself.
        """
        visited = set()
        order = []

        def _visit(node):
            for nbr in sorted(self.edges.get(node, {})):
                if nbr not in visited:
                    visited.add(nbr)
                    order.append(nbr)
                    _visit(nbr)

        _visit(start)
        return order

    def bfs(self, start):
        """
        Breadth-first search traversal from `start`.
        Yields nodes as visited, excluding start itself.
        """
        visited = set()
        queue = deque()

        visited.add(start)

        for nbr in sorted(self.edges.get(start, {})):
            queue.append(nbr)
            visited.add(nbr)

        while queue:
            node = queue.popleft()
            yield node
            for nbr in sorted(self.edges.get(node, {})):
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append(nbr)


class DAG(TraversableDigraph):
    """
    Directed acyclic graph — add_edge ensures no cycle.
    """

    def add_edge(self, u, v, edge_weight=None):
        """
        Add edge u → v only if it does not create a cycle.
        Raises ValueError if inserting the edge introduces a cycle.
        """
        self.add_node(u)
        self.add_node(v)

        # If v → ... → u already exists, adding u → v forms a cycle
        if self._has_path(v, u):
            raise ValueError(f"Adding edge {u} → {v} creates a cycle.")

        self.edges[u][v] = edge_weight

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
                for nbr in self.edges.get(node, {}):
                    stack.append(nbr)
        return False

