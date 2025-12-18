# Dosya Adı: graph_manager.py

import math
import json
from model import Node, Edge # Node ve Edge sınıflarını model.py'den alıyoruz

class Graph:
    """
    Proje Dökümanı Madde 4.1 (Graph Sınıfı)
    Tüm düğümleri (nodes) ve kenarları (edges) yöneten ana sınıf.
    """
    def __init__(self):
        self.nodes = {}          # {node_id: NodeObjesi}
        self.adjacency_list = {} # {node_id: [EdgeObjesi, EdgeObjesi...]}

    # --- 1. CRUD İŞLEMLERİ (EKLEME/SİLME) ---
    
    def add_node(self, node):
        """Sisteme yeni bir düğüm ekler."""
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.adjacency_list[node.id] = []
        else:
            print(f"[UYARI] Node ID {node.id} zaten mevcut.")

    def remove_node(self, node_id):
        """Bir düğümü ve ona bağlı tüm yolları siler."""
        if node_id in self.nodes:
            # 1. Düğümü sözlükten sil
            del self.nodes[node_id]
            
            # 2. Düğümün kendi komşuluk listesini sil
            if node_id in self.adjacency_list:
                del self.adjacency_list[node_id]
            
            # 3. Diğer düğümlerin listelerinden bu düğüme giden yolları temizle
            for nid in self.adjacency_list:
                self.adjacency_list[nid] = [
                    edge for edge in self.adjacency_list[nid] 
                    if edge.target.id != node_id
                ]
            print(f"[INFO] Node {node_id} ve bağlantıları silindi.")

    def add_edge(self, id1, id2):
        """İki düğüm arasına formüle dayalı ağırlıklı yol ekler."""
        if id1 in self.nodes and id2 in self.nodes:
            node1 = self.nodes[id1]
            node2 = self.nodes[id2]

            # Formüle göre ağırlık hesapla
            weight = self._calculate_weight(node1, node2)

            # Edge nesnelerini oluştur (Yönsüz graf olduğu için çift yönlü)
            edge1 = Edge(node1, node2, weight)
            edge2 = Edge(node2, node1, weight)

            self.adjacency_list[id1].append(edge1)
            self.adjacency_list[id2].append(edge2)
        else:
            print("[ERROR] Node ID'leri bulunamadı, yol eklenemedi.")

    def remove_edge(self, id1, id2):
        """İki düğüm arasındaki bağlantıyı siler."""
        if id1 in self.adjacency_list:
            self.adjacency_list[id1] = [e for e in self.adjacency_list[id1] if e.target.id != id2]
        if id2 in self.adjacency_list:
            self.adjacency_list[id2] = [e for e in self.adjacency_list[id2] if e.target.id != id1]
        print(f"[INFO] Edge {id1}-{id2} silindi.")

    # --- 2. HESAPLAMA VE YARDIMCI METOTLAR ---

    def _calculate_weight(self, n1, n2):
        """
        Madde 4.3 Formülü: 1 + Kök((Fark1^2) + (Fark2^2) + ...)
        """
        diff_active = (n1.active_score - n2.active_score) ** 2
        diff_social = (n1.social_score - n2.social_score) ** 2
        diff_conn = (n1.connection_count - n2.connection_count) ** 2
        
        result = 1 + math.sqrt(diff_active + diff_social + diff_conn)
        return round(result, 2)

    def get_nodes(self):
        """Tüm düğüm nesnelerini liste olarak döner."""
        return self.nodes.values()

    def get_neighbors(self, node_id):
        """Bir düğümün komşularını (Edge listesi) döner."""
        return self.adjacency_list.get(node_id, [])

    # --- 3. VERİ İÇE/DIŞA AKTARIM (JSON) ---

    def to_json(self, filename="graph_data.json"):
        """Mevcut graf yapısını JSON dosyasına kaydeder."""
        data = {
            "nodes": [],
            "edges": []
        }
        # Node'ları serileştir
        for n in self.nodes.values():
            data["nodes"].append({
                "id": n.id, "name": n.name, "x": n.x, "y": n.y,
                "active": n.active_score, "social": n.social_score, "conn": n.connection_count
            })
        
        # Edge'leri serileştir (Çiftleri tekilleştirerek)
        saved_edges = set()
        for nid, edges in self.adjacency_list.items():
            for edge in edges:
                # (1,2) ile (2,1) aynıdır, sıralayıp set'e atıyoruz
                pair = tuple(sorted((nid, edge.target.id)))
                if pair not in saved_edges:
                    data["edges"].append({"source": nid, "target": edge.target.id})
                    saved_edges.add(pair)
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"[BASARILI] Veriler {filename} dosyasına kaydedildi.")
        except Exception as e:
            print(f"[HATA] Kaydetme başarısız: {e}")

    def load_from_json(self, filename="graph_data.json"):
        """JSON dosyasından verileri okur ve grafı yeniden oluşturur."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Mevcut veriyi temizle
            self.nodes = {}
            self.adjacency_list = {}
            
            # Node'ları oluştur
            for n_data in data["nodes"]:
                new_node = Node(
                    n_data["id"], n_data["name"], n_data["x"], n_data["y"], 
                    n_data["active"], n_data["social"], n_data["conn"]
                )
                self.add_node(new_node)
            
            # Edge'leri oluştur (add_edge zaten ağırlığı hesaplayacak)
            for e_data in data["edges"]:
                self.add_edge(e_data["source"], e_data["target"])
                
            print(f"[BASARILI] Veriler {filename} dosyasından yüklendi.")
        except FileNotFoundError:
            print("[HATA] Dosya bulunamadı.")
        except Exception as e:
            print(f"[HATA] Yükleme hatası: {e}")