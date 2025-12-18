# Dosya Adı: main.py

from model import Node
from graph_manager import Graph
# Güncellenen algorithms.py dosyasındaki tüm sınıfları çağırıyoruz
from algorithms import BFS, DFS, Dijkstra, AStar, DegreeCentrality, Coloring

def main():
    print("\n=== PROJECT II: ISTANBUL GUIDE (FULL TEST) ===\n")

    # 1. Graph Manager Başlat (Artık 'Graph' sınıfı)
    istanbul_graph = Graph()

    # 2. Node'ları Oluştur (Artık 'Node' sınıfı)
    # Parametreler: (id, name, x, y, active, social, connection)
    
    # --- FATİH (Historic) ---
    n1 = Node(1, "Suleymaniye", 100, 300, 0.8, 400, 3)
    n2 = Node(2, "Sultanahmet", 120, 320, 0.9, 600, 4) 
    n3 = Node(3, "Grand Bazaar", 110, 280, 0.95, 350, 5)

    # --- BEYOĞLU (Modern) ---
    n4 = Node(4, "Galata Tower", 300, 200, 0.95, 950, 3) 
    n5 = Node(5, "Istiklal St", 320, 180, 1.0, 800, 5) 

    # --- BEŞİKTAŞ (Bosphorus) ---
    n6 = Node(6, "Dolmabahce", 400, 150, 0.7, 700, 2)
    n7 = Node(7, "Ortakoy", 450, 120, 0.8, 900, 2)

    print(">>> Loading Nodes into Graph...")
    nodes = [n1, n2, n3, n4, n5, n6, n7]
    for n in nodes:
        istanbul_graph.add_node(n) # Artık 'add_node' kullanıyoruz

    # 3. Bağlantıları Kur (Edges)
    print(">>> Calculating Edge Weights (Tourism Similarity)...")

    # Fatih Bölgesi
    istanbul_graph.add_edge(1, 2) # Suleymaniye <-> Sultanahmet
    istanbul_graph.add_edge(2, 3) # Sultanahmet <-> Grand Bazaar

    # Köprü (Fatih -> Beyoğlu)
    istanbul_graph.add_edge(1, 4) # Suleymaniye <-> Galata

    # Beyoğlu Bölgesi
    istanbul_graph.add_edge(4, 5) # Galata <-> Istiklal

    # Beşiktaş Bölgesi
    istanbul_graph.add_edge(5, 6) # Istiklal -> Dolmabahce
    istanbul_graph.add_edge(6, 7) # Dolmabahce -> Ortakoy

    # --- TESTLER (ALGORITHMS) ---

    print("\n-------------------------------------------")
    print("--- TEST 1: BFS (Traversal) ---")
    print("-------------------------------------------")
    bfs = BFS()
    # 'execute' metodu kullanıyoruz (calistir yerine)
    path_bfs = bfs.execute(istanbul_graph, start_id=1)
    print(f"Start: Suleymaniye (ID:1)")
    print(f"Visited Order: {path_bfs}")

    print("\n-------------------------------------------")
    print("--- TEST 2: DIJKSTRA (Shortest Path) ---")
    print("-------------------------------------------")
    # Sultanahmet(2) -> Ortakoy(7)
    dijkstra = Dijkstra()
    path_dijkstra, cost = dijkstra.execute(istanbul_graph, start_id=2, target_id=7)
    
    # ID listesini isme çevirelim
    name_path = [istanbul_graph.nodes[nid].name for nid in path_dijkstra]
    
    print(f"Route: Sultanahmet -> Ortakoy")
    print(f"Path (Names): {' -> '.join(name_path)}")
    print(f"Total Discrepancy Cost: {cost:.2f}")

    print("\n-------------------------------------------")
    print("--- TEST 3: DEGREE CENTRALITY (Popularity) ---")
    print("-------------------------------------------")
    centrality = DegreeCentrality()
    top_nodes = centrality.execute(istanbul_graph)
    
    print("Top 5 Most Connected Nodes:")
    for idx, (count, name, nid) in enumerate(top_nodes, 1):
        print(f"{idx}. {name} (Connections: {count})")

    print("\n-------------------------------------------")
    print("--- TEST 4: A* (A-Star) ALGORITHM ---")
    print("-------------------------------------------")
    astar = AStar()
    path_astar, cost_astar = astar.execute(istanbul_graph, start_id=2, target_id=7)
    print(f"A* Path IDs: {path_astar}")
    print(f"A* Cost: {cost_astar:.2f}")

    print("\n-------------------------------------------")
    print("--- TEST 5: COLORING (Welsh-Powell) ---")
    print("-------------------------------------------")
    coloring = Coloring()
    color_map = coloring.execute(istanbul_graph)
    
    print("Node Colors (Neighbors have different colors):")
    for nid, color in color_map.items():
        node_name = istanbul_graph.nodes[nid].name
        print(f" - {node_name:<15} : Color Group {color}")

if __name__ == "__main__":
    main()