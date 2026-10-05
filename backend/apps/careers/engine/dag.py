from collections import defaultdict, deque
from typing import Dict, List, Set, Any, Tuple

class CyclicDependencyError(Exception):
    """Raised when a circular prerequisite dependency is detected."""
    pass

class DirectedAcyclicGraph:
    """
    Directed Acyclic Graph engine for Career Skills.
    Guarantees prerequisite integrity and resolves optimal learning milestone sequences.
    """

    def __init__(self):
        # adj[u] = list of nodes v that depend on u (u is prerequisite of v)
        self.adj: Dict[str, List[str]] = defaultdict(list)
        # in_degree[v] = count of prerequisites v requires
        self.in_degree: Dict[str, int] = defaultdict(int)
        self.nodes: Set[str] = set()

    def add_node(self, node_id: str) -> None:
        self.nodes.add(node_id)
        if node_id not in self.in_degree:
            self.in_degree[node_id] = 0

    def add_edge(self, prerequisite_id: str, skill_id: str) -> None:
        """
        Adds dependency: prerequisite_id -> skill_id
        (prerequisite_id must be completed BEFORE skill_id)
        """
        if prerequisite_id == skill_id:
            raise CyclicDependencyError(f"Self-dependency detected: {skill_id} cannot depend on itself.")

        self.add_node(prerequisite_id)
        self.add_node(skill_id)

        self.adj[prerequisite_id].append(skill_id)
        self.in_degree[skill_id] += 1

    def detect_cycle(self) -> bool:
        """
        Returns True if the graph contains a cycle.
        Uses Kahn's algorithm (topological traversal).
        """
        in_deg = self.in_degree.copy()
        queue = deque([node for node in self.nodes if in_deg[node] == 0])
        visited_count = 0

        while queue:
            curr = queue.popleft()
            visited_count += 1
            for neighbor in self.adj[curr]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

        return visited_count < len(self.nodes)

    def topological_sort(self) -> List[str]:
        """
        Returns a flat list of node IDs in valid prerequisite order.
        Raises CyclicDependencyError if graph contains a cycle.
        """
        in_deg = self.in_degree.copy()
        queue = deque([node for node in self.nodes if in_deg[node] == 0])
        ordered: List[str] = []

        while queue:
            curr = queue.popleft()
            ordered.append(curr)
            for neighbor in self.adj[curr]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

        if len(ordered) < len(self.nodes):
            remaining = [node for node in self.nodes if node not in ordered]
            raise CyclicDependencyError(f"Cycle detected involving nodes: {remaining}")

        return ordered

    def resolve_milestone_levels(self) -> List[List[str]]:
        """
        Groups skills into progressive milestone tiers:
        - Tier 0: Skills with no prerequisites (immediately unlockable).
        - Tier N: Skills whose prerequisites are all in Tier < N.
        """
        in_deg = self.in_degree.copy()
        current_tier = deque([node for node in self.nodes if in_deg[node] == 0])
        milestones: List[List[str]] = []
        visited = 0

        while current_tier:
            next_tier = deque()
            tier_nodes: List[str] = []

            for _ in range(len(current_tier)):
                curr = current_tier.popleft()
                tier_nodes.append(curr)
                visited += 1

                for neighbor in self.adj[curr]:
                    in_deg[neighbor] -= 1
                    if in_deg[neighbor] == 0:
                        next_tier.append(neighbor)

            milestones.append(tier_nodes)
            current_tier = next_tier

        if visited < len(self.nodes):
            raise CyclicDependencyError("Cannot resolve milestone levels due to a cycle in dependencies.")

        return milestones
