# Dosya Adı: algorithms.py

from abc import ABC, abstractmethod
import heapq
import math

# --- SOYUTLAMA (Madde 4.1'e uygun) ---
class Algorithm(ABC):
    @abstractmethod
    def execute(self, graph, start_id=None, target_id=None):
        pass

# --- RENKLENDİRME (Coloring Class) ---
class Coloring(Algorithm):
    """Welsh-Powell Algoritması"""
    def execute(self, graph, start_id=None, target_id=None):
        # Derecesine göre düğümleri sırala
        sorted_nodes = sorted(
            graph.nodes.keys(),
            key=lambda x: len(graph.get_neighbors(x)),
            reverse=True
        )
        
        colors = {}
        current_color = 0

        for node_id in sorted_nodes:
            if node_id in colors:
                continue

            current_color += 1
            colors[node_id] = current_color
            
            for candidate_id in sorted_nodes:
                if candidate_id in colors:
                    continue
                
                is_neighbor = False
                for edge in graph.get_neighbors(candidate_id):
                    if colors.get(edge.target.id) == current_color:
                        is_neighbor = True
                        break
                
                if not is_neighbor:
                    colors[candidate_id] = current_color
        return colors

# --- GEZİNME ALGORİTMALARI ---
class BFS(Algorithm):
    def execute(self, graph, start_id, target_id=None):
        visited = set()
        queue = [start_id]
        path = []
        visited.add(start_id)

        while queue:
            current_id = queue.pop(0)
            path.append(current_id)

            for edge in graph.get_neighbors(current_id):
                neighbor_id = edge.target.id
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append(neighbor_id)
        return path

class DFS(Algorithm):
    def execute(self, graph, start_id, target_id=None):
        visited = set()
        stack = [start_id]
        path = []

        while stack:
            current_id = stack.pop()
            if current_id not in visited:
                visited.add(current_id)
                path.append(current_id)
                
                for edge in graph.get_neighbors(current_id):
                    stack.append(edge.target.id)
        return path

# --- EN KISA YOL ALGORİTMALARI ---
class Dijkstra(Algorithm):
    def execute(self, graph, start_id, target_id=None):
        distances = {nid: float('inf') for nid in graph.nodes}
        distances[start_id] = 0
        pq = [(0, start_id)]
        previous = {nid: None for nid in graph.nodes}

        while pq:
            curr_dist, curr_id = heapq.heappop(pq)
            
            if target_id and curr_id == target_id:
                break
            
            if curr_dist > distances[curr_id]:
                continue

            for edge in graph.get_neighbors(curr_id):
                neighbor = edge.target
                new_dist = curr_dist + edge.weight
                
                if new_dist < distances[neighbor.id]:
                    distances[neighbor.id] = new_dist
                    previous[neighbor.id] = curr_id
                    heapq.heappush(pq, (new_dist, neighbor.id))
        
        if target_id:
            path = []
            curr = target_id
            while curr is not None:
                path.insert(0, curr)
                curr = previous[curr]
            return path, distances[target_id]
        return distances

class AStar(Algorithm):
    def execute(self, graph, start_id, target_id):
        if target_id is None: return None
        
        target_node = graph.nodes[target_id]

        def heuristic(nid):
            n = graph.nodes[nid]
            return math.sqrt((n.x - target_node.x)**2 + (n.y - target_node.y)**2)

        g_score = {nid: float('inf') for nid in graph.nodes}
        g_score[start_id] = 0
        f_score = {nid: float('inf') for nid in graph.nodes}
        f_score[start_id] = heuristic(start_id)
        
        previous = {nid: None for nid in graph.nodes}
        pq = [(f_score[start_id], start_id)]

        while pq:
            _, curr_id = heapq.heappop(pq)
            if curr_id == target_id: break

            for edge in graph.get_neighbors(curr_id):
                neighbor = edge.target
                temp_g = g_score[curr_id] + edge.weight
                
                if temp_g < g_score[neighbor.id]:
                    previous[neighbor.id] = curr_id
                    g_score[neighbor.id] = temp_g
                    f_score[neighbor.id] = temp_g + heuristic(neighbor.id)
                    heapq.heappush(pq, (f_score[neighbor.id], neighbor.id))

        path = []
        curr = target_id
        while curr is not None:
            path.insert(0, curr)
            curr = previous[curr]
        return path, g_score[target_id]

# --- ANALİZ ---
class DegreeCentrality(Algorithm):
    def execute(self, graph, start_id=None, target_id=None):
        scores = []
        for node in graph.nodes.values():
            count = len(graph.get_neighbors(node.id))
            scores.append((count, node.name, node.id))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:5]
    # Dosya: algorithms.py (En alta ekle)

class ConnectedComponents(Algorithm):
    """
    Bağlı Bileşenleri (Ayrık Toplulukları) Bulur.
    İster: 3.2. Bağlı bileşenlerin tespit edilmesi.
    """
    def execute(self, graph, start_id=None, target_id=None):
        visited = set()
        components = []

        for node_id in graph.nodes:
            if node_id not in visited:
                # Yeni bir bileşen bulduk, BFS/DFS ile bu adayı keşfet
                component = []
                queue = [node_id]
                visited.add(node_id)
                while queue:
                    curr = queue.pop(0)
                    component.append(curr)
                    for edge in graph.get_neighbors(curr):
                        neighbor = edge.target.id
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                components.append(component)
        return components