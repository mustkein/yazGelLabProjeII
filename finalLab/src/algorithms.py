from abc import ABC, abstractmethod
import heapq
import math
from collections import deque


class Algorithm(ABC):
    @abstractmethod
    def execute(self, graph, start_id=None, target_id=None):
        pass


class BFS(Algorithm):
    def execute(self, graph, start_id, target_id=None):
        if start_id not in graph.nodes:
            return []

        visited = set([start_id])
        queue = deque([start_id])
        path = []

        while queue:
            current = queue.popleft()
            path.append(current)

            if target_id is not None and current == target_id:
                break

            neighbors = sorted(
                graph.get_neighbors(current),
                key=lambda e: e.target.id
            )

            for edge in neighbors:
                nid = edge.target.id
                if nid not in visited:
                    visited.add(nid)
                    queue.append(nid)

        return path


class DFS(Algorithm):
    def execute(self, graph, start_id, target_id=None):
        if start_id not in graph.nodes:
            return []

        visited = set()
        stack = [start_id]
        path = []

        while stack:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)
            path.append(current)

            if target_id is not None and current == target_id:
                break

            neighbors = sorted(
                graph.get_neighbors(current),
                key=lambda e: e.target.id,
                reverse=True
            )

            for edge in neighbors:
                nid = edge.target.id
                if nid not in visited:
                    stack.append(nid)

        return path


class Dijkstra(Algorithm):
    def execute(self, graph, start_id, target_id=None):
        if start_id not in graph.nodes:
            return [], 0

        dist = {nid: float("inf") for nid in graph.nodes}
        prev = {nid: None for nid in graph.nodes}
        dist[start_id] = 0

        pq = [(0, start_id)]

        while pq:
            curr_dist, curr = heapq.heappop(pq)

            if curr_dist > dist[curr]:
                continue

            if target_id is not None and curr == target_id:
                break

            for edge in graph.get_neighbors(curr):
                nid = edge.target.id
                new_dist = curr_dist + edge.weight

                if new_dist < dist[nid]:
                    dist[nid] = new_dist
                    prev[nid] = curr
                    heapq.heappush(pq, (new_dist, nid))

        if target_id is None:
            return dist

        if dist[target_id] == float("inf"):
            return [], 0

        path = []
        cur = target_id
        while cur is not None:
            path.insert(0, cur)
            cur = prev[cur]

        return path, dist[target_id]


class AStar(Algorithm):
    def execute(self, graph, start_id, target_id):
        if start_id not in graph.nodes or target_id not in graph.nodes:
            return [], 0

        def h(nid):
            a = graph.nodes[nid]
            b = graph.nodes[target_id]
            return math.hypot(a.x - b.x, a.y - b.y)

        g = {nid: float("inf") for nid in graph.nodes}
        f = {nid: float("inf") for nid in graph.nodes}
        prev = {nid: None for nid in graph.nodes}

        g[start_id] = 0
        f[start_id] = h(start_id)

        pq = [(f[start_id], start_id)]

        while pq:
            _, curr = heapq.heappop(pq)

            if curr == target_id:
                break

            for edge in graph.get_neighbors(curr):
                nid = edge.target.id
                temp_g = g[curr] + edge.weight

                if temp_g < g[nid]:
                    g[nid] = temp_g
                    f[nid] = temp_g + h(nid)
                    prev[nid] = curr
                    heapq.heappush(pq, (f[nid], nid))

        if g[target_id] == float("inf"):
            return [], 0

        path = []
        cur = target_id
        while cur is not None:
            path.insert(0, cur)
            cur = prev[cur]

        return path, g[target_id]


class DegreeCentrality(Algorithm):
    def execute(self, graph, start_id=None, target_id=None):
        result = []

        for node in graph.nodes.values():
            degree = len(graph.get_neighbors(node.id))
            result.append((node.id, node.name, degree))

        result.sort(key=lambda x: x[2], reverse=True)
        return result[:5]


class Coloring(Algorithm):
    def execute(self, graph, start_id=None, target_id=None):
        nodes = sorted(
            graph.nodes.values(),
            key=lambda n: len(graph.get_neighbors(n.id)),
            reverse=True
        )

        colors = {}

        for node in nodes:
            used = set()
            for edge in graph.get_neighbors(node.id):
                nid = edge.target.id
                if nid in colors:
                    used.add(colors[nid])

            color = 1
            while color in used:
                color += 1

            colors[node.id] = color

        return colors


class ConnectedComponents(Algorithm):
    def execute(self, graph, start_id=None, target_id=None):
        visited = set()
        components = []

        for nid in sorted(graph.nodes.keys()):
            if nid in visited:
                continue

            comp = []
            queue = deque([nid])
            visited.add(nid)

            while queue:
                curr = queue.popleft()
                comp.append(curr)

                for edge in graph.get_neighbors(curr):
                    next_id = edge.target.id
                    if next_id not in visited:
                        visited.add(next_id)
                        queue.append(next_id)

            comp.sort()
            components.append(comp)

        return components
