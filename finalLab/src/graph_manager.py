import math
import json
import csv
import os
import random
from model import Node, Edge

class Graph:
    def __init__(self):
        self.nodes = {}
        self.adjacency_list = {}
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(os.path.dirname(current_dir), 'data')
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def add_node(self, node):
        """Graf yapısına Node sınıfından bir nesne ekler."""
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.adjacency_list[node.id] = []
        else:
            # Düğüm zaten varsa bilgilerini güncelle
            self.nodes[node.id] = node

    def add_edge(self, id1, id2):
        """İki düğüm arasında dinamik ağırlıklı ve yönsüz bir kenar oluşturur."""
        try:
            id1, id2 = int(id1), int(id2)
            if id1 == id2: return

            if id1 in self.nodes and id2 in self.nodes:
                # Aynı kenarın tekrar eklenmesini engelle
                mevcut_komsular = [e.target.id for e in self.adjacency_list[id1]]
                if id2 in mevcut_komsular: return

                node1 = self.nodes[id1]
                node2 = self.nodes[id2]
                
                # Formüle uygun ağırlık hesapla
                weight = self._calculate_weight(node1, node2)
                
                # Yönsüz graf için çift taraflı ekleme
                self.adjacency_list[id1].append(Edge(node1, node2, weight))
                self.adjacency_list[id2].append(Edge(node2, node1, weight))
        except (ValueError, KeyError):
            pass

    def save_to_json_path(self, file_path):
        """Graf verilerini kullanıcı tarafından seçilen konuma JSON olarak kaydeder."""
        try:
            data = {"nodes": [], "edges": []}
            for n in self.nodes.values():
                data["nodes"].append(n.__dict__)
            
            saved_edges = set()
            for nid, edges in self.adjacency_list.items():
                for edge in edges:
                    pair = tuple(sorted((nid, edge.target.id)))
                    if pair not in saved_edges:
                        data["edges"].append({"source": nid, "target": edge.target.id})
                        saved_edges.add(pair)
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"JSON Yazma Hatası: {e}")
            return False

    def _calculate_weight(self, n1, n2):
        """
        Dinamik ağırlık formülü: 
        1 + (Aktiflik farkı * 100) + (Sosyal Skor farkı * 0.1) + (Bağlantı Sayısı farkı * 5)
        """
        diff_active = abs(n1.active_score - n2.active_score) * 100
        diff_social = abs(n1.social_score - n2.social_score) * 0.1
        diff_conn = abs(n1.connection_count - n2.connection_count) * 5
        
        cost = 1 + (diff_active + diff_social + diff_conn)
        return round(cost, 2)

    def load_from_csv(self, filename):
        """CSV'den verileri okur ve Node nesnelerini belirtilen isimlendirmelerle oluşturur."""
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            print(f"[HATA] Dosya bulunamadı: {path}")
            return

        try:
            self.nodes = {}
            self.adjacency_list = {}
            temp_neighbors = {} # Tüm düğümler yüklenene kadar bağlantıları beklet

            with open(path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    node_id = int(row["ID"])
                    
                    # Node sınıfı parametrelerine tam uyumlu oluşturma
                    new_node = Node(
                        node_id=node_id,
                        name=row["Name"],
                        x=int(row["X"]),
                        y=int(row["Y"]),
                        active_score=float(row["Active"]),
                        social_score=int(row["Social"]),
                        connection_count=int(row["Connection"])
                    )
                    self.add_node(new_node)
                    
                    # 'Neighbors' sütunundaki ID'leri ayır
                    if "Neighbors" in row and row["Neighbors"]:
                        temp_neighbors[node_id] = row["Neighbors"].split(';')

            # Düğümler oluştuktan sonra kenarları/bağlantıları kur
            for src_id, neighbors in temp_neighbors.items():
                for target_id in neighbors:
                    if target_id.strip():
                        self.add_edge(src_id, target_id)

            print(f"[BAŞARILI] {filename} yüklendi. Toplam {len(self.nodes)} mekan hazır.")
        except Exception as e:
            print(f"[HATA] CSV Okuma hatası: {e}")

    def get_nodes(self):
        """Graf içerisindeki tüm düğüm nesnelerini döndürür."""
        return self.nodes.values()

    def get_neighbors(self, node_id):
        """Belirli bir düğümün komşuluk (Edge nesnesi) listesini döndürür."""
        return self.adjacency_list.get(node_id, [])

    def update_node(self, node_id, name=None):
        """Mevcut bir düğümün ismini günceller."""
        if node_id in self.nodes:
            if name: self.nodes[node_id].name = name
            return True
        return False

    def remove_node(self, node_id):
        """Düğümü ve ona bağlı tüm kenarları siler."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            if node_id in self.adjacency_list:
                del self.adjacency_list[node_id]
            # Diğer düğümlerin komşuluk listelerinden temizle
            for nid in self.adjacency_list:
                self.adjacency_list[nid] = [e for e in self.adjacency_list[nid] if e.target.id != node_id]
            return True
        return False

    def to_json(self, filename="kaydedilen_veriler.json"):
        """Mevcut graf yapısını JSON olarak kaydeder."""
        path = os.path.join(self.data_dir, filename)
        data = {"nodes": [], "edges": []}
        for n in self.nodes.values():
            data["nodes"].append(n.__dict__)
        
        saved_edges = set()
        for nid, edges in self.adjacency_list.items():
            for edge in edges:
                pair = tuple(sorted((nid, edge.target.id)))
                if pair not in saved_edges:
                    data["edges"].append({"source": nid, "target": edge.target.id})
                    saved_edges.add(pair)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[BASARILI] JSON kaydedildi: {path}")

    def export_adjacency_matrix(self, filename="komsuluk_matrisi.txt"):
        """Grafın komşuluk matrisini TXT dosyası olarak dışa aktarır."""
        path = os.path.join(self.data_dir, filename)
        sorted_ids = sorted(self.nodes.keys())
        size = len(sorted_ids)
        matrix = [[0] * size for _ in range(size)]
        id_map = {node_id: idx for idx, node_id in enumerate(sorted_ids)}

        for nid, edges in self.adjacency_list.items():
            for edge in edges:
                matrix[id_map[nid]][id_map[edge.target.id]] = 1

        with open(path, "w", encoding="utf-8") as f:
            f.write("    " + " ".join([str(i).rjust(3) for i in sorted_ids]) + "\n")
            for i in range(size):
                row = " ".join([str(x).rjust(3) for x in matrix[i]])
                f.write(f"{sorted_ids[i]:<3} {row}\n")
        print(f"[BASARILI] Matris şuraya çıkarıldı: {path}")