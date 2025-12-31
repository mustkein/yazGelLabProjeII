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


