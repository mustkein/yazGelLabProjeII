import unittest
import random

class TestMediumGraph(unittest.TestCase):
    def setUp(self):
        """
        Testlerden önce çalışır.
        Otomatik olarak orta ölçekli (örneğin 50 düğümlü) bir graf oluşturur.
        """
        self.node_count = 50
        self.graph = {i: [] for i in range(self.node_count)}
        
        # Rastgele kenarlar ekleyelim (Her düğümden rastgele 2 başka düğüme)
        for i in range(self.node_count):
            targets = random.sample(range(self.node_count), 2)
            for t in targets:
                if t != i: # Kendine dönmesin
                    self.graph[i].append(t)

    def test_graph_size(self):
        """Grafiğin doğru boyutta oluşturulduğunu test eder."""
        self.assertEqual(len(self.graph), 50, "Medium graf 50 düğümlü olmalı.")

    def test_connections_not_empty(self):
        """Grafiğin tamamen boş olmadığını test eder."""
        total_edges = sum(len(edges) for edges in self.graph.values())
        self.assertGreater(total_edges, 0, "Grafikte hiç kenar (edge) yok, bağlantı oluşmamış.")

    def test_data_integrity(self):
        """Düğümlerin integer olup olmadığını kontrol eder."""
        for node in self.graph:
            self.assertIsInstance(node, int, "Düğüm isimleri tam sayı olmalı.")

if __name__ == '__main__':
    unittest.main()