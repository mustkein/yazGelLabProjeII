from model import Node
from graph_manager import Graph
from algorithms import BFS, DFS, Dijkstra, AStar, DegreeCentrality, Coloring, ConnectedComponents

def main():
    print("\n=== İstanbul Sosyal Ağ Analizi: KONSOL TEST MODU ===\n")

    # 1. GRAF YÖNETİCİSİNİ BAŞLAT
    istanbul_graph = Graph()

    # 2. MEKANLARI (DÜĞÜMLERİ) OLUŞTUR
    print(">>> Düğümler (Mekanlar) Yükleniyor...")
    
    nodes = [
        Node(1, "Süleymaniye Camii", 100, 300, 0.8, 400, 3),
        Node(2, "Sultanahmet Meydanı", 120, 320, 0.9, 600, 4),
        Node(3, "Kapalı Çarşı", 110, 280, 0.95, 350, 5),
        Node(4, "Galata Kulesi", 300, 200, 0.95, 950, 3),
        Node(5, "İstiklal Caddesi", 320, 180, 1.0, 800, 5),
        Node(6, "Dolmabahçe Sarayı", 400, 150, 0.7, 700, 2),
        Node(7, "Ortaköy Sahili", 450, 120, 0.8, 900, 2)
    ]

    for n in nodes:
        istanbul_graph.add_node(n)

    # 3. BAĞLANTILARI (KENARLARI) KUR
    # Ağırlıklar yeni formüle göre otomatik hesapla
    print(">>> Bağlantılar Kuruluyor ve Ağırlıklar Hesaplanıyor...")
    
    edges = [
        (1, 2), # Süleymaniye <-> Sultanahmet
        (2, 3), # Sultanahmet <-> Kapalıçarşı
        (1, 4), # Köprü Geçişi
        (4, 5), # Galata <-> İstiklal
        (5, 6), # İstiklal <-> Dolmabahçe
        (6, 7)  # Dolmabahçe <-> Ortaköy
    ]
    
    for u, v in edges:
        istanbul_graph.add_edge(u, v)

    # 4. ALGORİTMA TESTLERİ
    print("\n-------------------------------------------")
    print("--- TEST 1: BFS (Gezinme Sırası) ---")
    start_node = 1
    bfs = BFS()
    path_bfs = bfs.execute(istanbul_graph, start_id=start_node)
    
    # ID listesini isim listesine çevirerek yazdır
    names = [istanbul_graph.nodes[nid].name for nid in path_bfs]
    print(f"Başlangıç: {istanbul_graph.nodes[start_node].name}")
    print(f"Rota: {names}")

    print("\n-------------------------------------------")
    print("--- TEST 2: Dijkstra (En Kısa Yol & Maliyet) ---")
    start, target = 2, 7 # Sultanahmet -> Ortaköy
    dijkstra = Dijkstra()
    path_dij, cost = dijkstra.execute(istanbul_graph, start_id=start, target_id=target)
    
    names_dij = [istanbul_graph.nodes[nid].name for nid in path_dij]
    print(f"Hedef: {istanbul_graph.nodes[start].name} -> {istanbul_graph.nodes[target].name}")
    print(f"En Uygun Rota: {' -> '.join(names_dij)}")
    print(f"Toplam Uyumsuzluk Maliyeti: {cost:.2f}")

    print("\n-------------------------------------------")
    print("--- TEST 3: Degree Centrality (Popülerlik) ---")
    centrality = DegreeCentrality()
    top_nodes = centrality.execute(istanbul_graph)
    
    print("En Çok Bağlantısı Olan İlk 5 Mekan:")
    for idx, (count, name, nid) in enumerate(top_nodes, 1):
        print(f"{idx}. {name} (Bağlantı Sayısı: {count})")

    print("\n-------------------------------------------")
    print("--- TEST 4: Graph Coloring (Welsh-Powell) ---")
    coloring = Coloring()
    color_map = coloring.execute(istanbul_graph)
    
    print("Mekan Renk Atamaları (Komşular Farklı Renkte):")
    for nid, color in color_map.items():
        print(f" - {istanbul_graph.nodes[nid].name:<20} : Renk Grubu {color}")

    print("\n-------------------------------------------")
    print("--- TEST 5: Connected Components (Ayrık Topluluklar) ---")
    
    cc = ConnectedComponents()
    comps = cc.execute(istanbul_graph)
    print(f"Toplam Ayrık Topluluk Sayısı: {len(comps)}")
    for i, comp in enumerate(comps, 1):
        comp_names = [istanbul_graph.nodes[nid].name for nid in comp]
        print(f"Topluluk {i}: {comp_names}")

    print("\n-------------------------------------------")
    print("--- TEST 6: Dosya Kayıt Testi (CSV & JSON) ---")
    # CSV Kaydet
    istanbul_graph.save_to_csv("test_mekanlar.csv")
    # JSON Kaydet
    istanbul_graph.to_json("test_veriler.json")
    print("[OK] Dosyalar 'data' klasörüne başarıyla kaydedildi.")

if __name__ == "__main__":
    main()