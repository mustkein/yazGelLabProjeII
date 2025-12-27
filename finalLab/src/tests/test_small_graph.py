import unittest

# Test edilecek Graph sınıfının veya fonksiyonlarının burada import edildiğini varsayalım
# from my_graph_project import Graph, bfs

class TestSmallGraph(unittest.TestCase):
    def setUp(self):
        """
        Testlerden önce çalışır. 
        Küçük, kontrol edilebilir bir graf oluşturur.
        Yapı: A -> B -> C (ve A -> D)
        """
        # Örnek olarak basit bir sözlük (dictionary) yapısı kullanıyorum
        self.graph = {
            'A': ['B', 'D'],
            'B': ['C'],
            'C': [],
            'D': []
        }

    def test_node_count(self):
        """Düğüm sayısının doğruluğunu test eder."""
        expected_nodes = 4
        self.assertEqual(len(self.graph), expected_nodes, "Düğüm sayısı yanlış!")

    def test_path_existence(self):
        """A'dan C'ye bir yol olup olmadığını test eder (Basit mantık)."""
        # Bu kısım normalde senin yazdığın algoritmayı çağırır
        has_path = 'C' in self.graph['B']  # Basit bir kontrol örneği
        self.assertTrue(has_path, "B'den C'ye kenar olmalı.")

    def test_isolated_node(self):
        """D düğümünün çıkış kenarı olmadığını test eder."""
        self.assertEqual(len(self.graph['D']), 0, "D düğümü izole olmalı (çıkışı yok).")

if __name__ == '__main__':
    unittest.main()