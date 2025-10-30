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
        # edges: dict of name → dict of (child → weight)
        self.edges = {}

    def add_node(self, name, value=None):
        """
        Add a node with optional value.
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
        Return list of node names.
        """
        return list(self.nodes.keys())

    def get_node_value(self, name):
        """
        Return node's stored value.
        """
        if name not in self.nodes:
            raise KeyError(f"Node '{name}' does not exist.")
        return self.nodes[name]

    def get_edge_weight(self, u, v):
        """
        Return stored edge weight for u → v.
        """
        if u not in self.edges or v not in self.edges[u]:
            raise KeyError(f"Edge '{u} → {v}' does not exist.")
        return self.edges[u][v]

    def successors(self, name):
        """
        Return sorted list of nodes reachable from `name` directly.
        """
        if name not in self.edges:
            return []
        return sorted(self.edges[name].keys())

    def predecessors(self, name):
        """
        Return sorted list of nodes that point directly to `name`.
        """
        result = []
        for parent, children in self.edges.items():
            if name in children:
                result.append(parent)
        return sorted(result)

    def top_sort(self):
        """
        Topological sort. Raises ValueError if cycle exists.
        """
        indegree = {node: 0 for node in self.nodes}
        for parent, children in self.edges.items():
            for child in children:
                indegree[child] += 1

        queue = deque(sorted([n for n, d in indegree.items() if d == 0]))
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for child in sorted(self.edges.get(node, {}).keys()):
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)

        if len(order) != len(self.nodes):
            raise ValueError("Graph has a cycle; cannot topologically sort.")

        return order


class TraversableDigraph(SortableDigraph):
    """
    Adds DFS and BFS traversal methods.
    """

    def dfs(self, start):
        """
        DFS traversal (excluding start from returned list).
        """
        visited = set()
        order = []

        def _visit(node):
            for nbr in sorted(self.edges.get(node, {}).keys()):
                if nbr not in visited:
                    visited.add(nbr)
                    order.append(nbr)
                    _visit(nbr)

        _visit(start)
        return order

    def bfs(self, start):
        """
        BFS traversal (excluding start).
        """
        visited = {start}
        queue = deque()

        for nbr in sorted(self.edges.get(start, {}).keys()):
            queue.append(nbr)
            visited.add(nbr)

        while queue:
            node = queue.popleft()
            yield node
            for nbr in sorted(self.edges.get(node, {}).keys()):
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append(nbr)


class DAG(TraversableDigraph):
    """
    DAG that prevents insertion of cycle–creating edges.
    """

    def add_edge(self, u, v, edge_weight=None):
        """
        Add u → v only if it does not create a cycle.
        Raises ValueError on cycle.
        """
        self.add_node(u)
        self.add_node(v)

        if self._has_path(v, u):
            raise ValueError(f"Adding edge {u} → {v} creates a cycle.")

        self.edges[u][v] = edge_weight

    def _has_path(self, start, goal):
        """
        True if path start → ... → goal exists.
        """
        stack = [start]
        visited = set()

        while stack:
            node = stack.pop()
            if node == goal:
                return True
            if node not in visited:
                visited.add(node)
                for nbr in self.edges.get(node, {}).keys():
                    stack.append(nbr)
        return False
