class Node:
    def __init__(self, node_id, name, x, y, active_score, social_score, connection_count):
        self.id = int(node_id)
        self.name = str(name)
        self.x = int(x)
        self.y = int(y)
        self.active_score = float(active_score)
        self.social_score = int(social_score)
        self.connection_count = int(connection_count)

    def __repr__(self):
        return f"<Node {self.id}: {self.name}>"

class Edge:
    def __init__(self, source_node, target_node, weight):
        self.source = source_node
        self.target = target_node
        self.weight = float(weight)

    def __repr__(self):
        return f"Edge({self.source.id}->{self.target.id}, W={self.weight:.2f})"