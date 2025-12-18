# Dosya Adı: model.py

class Node:
    """
    Eski 'Mekan' sınıfı. Proje dökümanı Madde 4.1'e (Node) uyması için güncellendi.
    """
    def __init__(self, node_id, name, x, y, active_score, social_score, connection_count):
        self.id = node_id
        self.name = name
        self.x = x
        self.y = y
        
        # Özellikler (Madde 4.3 Formülü için gerekli)
        self.active_score = float(active_score)         # Aktiflik
        self.social_score = int(social_score)           # Etkileşim
        self.connection_count = int(connection_count)   # Bağlantı Sayısı

    def __repr__(self):
        return f"<Node: {self.name} (ID: {self.id})>"


class Edge:
    """
    Eski 'Yol' sınıfı. Proje dökümanı Madde 4.1'e (Edge) uyması için güncellendi.
    """
    def __init__(self, source_node, target_node, weight):
        self.source = source_node  # Kaynak Düğüm
        self.target = target_node  # Hedef Düğüm
        self.weight = weight       # Ağırlık (Maliyet)

    def __repr__(self):
        return f"Edge: {self.source.name} <--> {self.target.name} | Weight: {self.weight}"