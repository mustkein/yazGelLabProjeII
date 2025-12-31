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

        queue = deque([start_id])
        visited = set([start_id])
        
        
        parent = {start_id: None}
        
      
        traversal_order = []

        while queue:
            current = queue.popleft()
            traversal_order.append(current)

            if target_id is not None and current == target_id:
               
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]

            neighbors = sorted(
                graph.get_neighbors(current),
                key=lambda e: e.target.id
            )

            for edge in neighbors:
                nid = edge.target.id
                if nid not in visited:
                    visited.add(nid)
                    parent[nid] = current
                    queue.append(nid)

        if target_id is not None:
            return []

        return traversal_order


class DFS(Algorithm):
    def execute(self, graph, start_id, target_id=None):
        if start_id not in graph.nodes:
            return []

        if target_id is None:
            visited = set()
            stack = [start_id]
            traversal_order = []

            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                
                visited.add(current)
                traversal_order.append(current)

                neighbors = sorted(
                    graph.get_neighbors(current),
                    key=lambda e: e.target.id,
                    reverse=True
                )
                
                for edge in neighbors:
                    nid = edge.target.id
                    if nid not in visited:
                        stack.append(nid)
            return traversal_order

        else:
            visited = set()
            stack = [start_id]
            parent = {start_id: None}

            while stack:
                current = stack.pop()

                if current == target_id:
                    break

                if current in visited:
                    continue
                
                visited.add(current)

                neighbors = sorted(
                    graph.get_neighbors(current),
                    key=lambda e: e.target.id,
                    reverse=True
                )

                for edge in neighbors:
                    nid = edge.target.id
                    if nid not in visited:
                        parent[nid] = current
                        stack.append(nid)
            
            if target_id in parent or target_id == start_id:
                if current != target_id: 
                    return []

                path = []
                while current is not None:
                    path.append(current)
                    current = parent.get(current)
                return path[::-1]
            
            return []
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
            return math.hypot(a.x - b.x, a.y - b.y) * 0.1

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


class FloydWarshall(Algorithm):
    def execute(self, graph, start_id, target_id):
        # Tüm düğüm ID'lerini al
        nodes = list(graph.nodes.keys())
        
        # Mesafe (dist) ve Yol (next_node) matrislerini başlat
        dist = {i: {j: float('inf') for j in nodes} for i in nodes}
        next_node = {i: {j: None for j in nodes} for i in nodes}

        # Kendisine olan uzaklık 0'dır
        for i in nodes:
            dist[i][i] = 0

        # Mevcut kenarları matrise ekle
        for u in nodes:
            for edge in graph.get_neighbors(u):
                v = edge.target.id
                weight = edge.weight
                dist[u][v] = weight
                next_node[u][v] = v
        
        # Floyd-Warshall Algoritması (O(N^3))
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]

        # Eğer hedef belirtilmemişse veya yol yoksa boş dön
        if start_id is None or target_id is None:
             return [], 0
        
        if dist[start_id][target_id] == float('inf'):
            return [], 0
            
        # Yolu yeniden oluştur (Path Reconstruction)
        path = []
        if next_node[start_id][target_id] is None:
            return path, 0
        
        curr = start_id
        while curr != target_id:
            path.append(curr)
            curr = next_node[curr][target_id]
        path.append(target_id)
        
        return path, dist[start_id][target_id]


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
    