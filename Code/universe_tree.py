"""
universe_tree.py
----------------

Constructs a branching multiverse tree using the Quantized Rupture Cosmology.
Each universe runs a cycle, ruptures, and spawns N = 6m children.

Author: Paul Jarvis
"""

from rupture_simulation import UniverseCycle

class UniverseNode:
    def __init__(self, generation, inherited_entropy=0.0):
        self.generation = generation
        self.inherited_entropy = inherited_entropy
        self.children = []
        self.data = None

    def run_cycle(self):
        """Run the universe cycle and store results."""
        sim = UniverseCycle()
        result = sim.run()

        result["entropy_inherited"] = self.inherited_entropy
        result["entropy_dumped"] = (
            self.inherited_entropy + result["entropy_produced"]
        )

        self.data = result
        return result

    def spawn_children(self):
        """Create child universes based on rupture mode."""
        N = self.data["children"]
        dumped_entropy = self.data["entropy_dumped"]

        for _ in range(N):
            child = UniverseNode(
                generation=self.generation + 1,
                inherited_entropy=dumped_entropy
            )
            self.children.append(child)

        return self.children


def build_tree(generations=3):
    """Build a multiverse tree for a given number of generations."""
    root = UniverseNode(generation=0)
    frontier = [root]

    for _ in range(generations):
        next_frontier = []
        for node in frontier:
            node.run_cycle()
            next_frontier.extend(node.spawn_children())
        frontier = next_frontier

    return root
