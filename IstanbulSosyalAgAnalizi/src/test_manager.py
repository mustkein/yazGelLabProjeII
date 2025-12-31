import time
import os
import statistics
from graph_manager import Graph
from algorithms import (BFS, DFS, Dijkstra, AStar, 
                        FloydWarshall, DegreeCentrality, 
                        Coloring, ConnectedComponents)

class AdvancedPerformanceTester:
    def __init__(self):
        # Test edilecek senaryolar ve iterasyon sayısı
        self.scenarios = ["mekanlar_dusuk.csv", "mekanlar_orta.csv"]
        self.iterations = 10 
        self.report_lines = []

    def log(self, message):
        print(message)
        self.report_lines.append(message)

    def run_tests(self):
        self.log("  İSTANBUL SOSYAL AĞ ANALİZİ PERFORMANS TESTİ")
        self.log(f"Test Tarihi: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log(f"İterasyon Sayısı: {self.iterations} (10 iterasyon sonucunda ortalama değer alınmıştır.)")
        
        for csv_file in self.scenarios:
            g = Graph()
            g.load_from_csv(csv_file)
            
            if not g.nodes:
                self.log(f"\n> [HATA] {csv_file} yüklenemedi!")
                continue

            node_count = len(g.nodes)
            edge_count = sum(len(g.get_neighbors(nid)) for nid in g.nodes) // 2
            
            self.log(f"\n Senaryo: {csv_file}")
            self.log(f" Ölçek: {node_count} Düğüm, {edge_count} Bağlantı")
            self.log("\n| Algoritma | Durum | Ort. Süre (ms) | Standart Sapma | Sonuç Özeti |")

            # Dinamik Test Parametreleri
            node_ids = list(g.nodes.keys())
            s_id, t_id = node_ids[0], node_ids[-1]

            test_cases = [
                ("BFS ", BFS(), s_id, None),
                ("DFS ", DFS(), s_id, None),
                ("Dijkstra ", Dijkstra(), s_id, t_id),
                ("A* ", AStar(), s_id, t_id),
                ("Floyd-Warshall ", FloydWarshall(), s_id, t_id),
                ("Popülerlik", DegreeCentrality(), None, None),
                ("Welsh-Powell ", Coloring(), None, None),
                ("Bağlı Bileşen Tespiti", ConnectedComponents(), None, None)
            ]

            for name, algo, start, target in test_cases:
                times = []
                status = "BAŞARILI"
                summary = ""

                for _ in range(self.iterations):
                    start_time = time.perf_counter()
                    try:
                        if target is not None:
                            res = algo.execute(g, start, target)
                            path = res[0] if isinstance(res, tuple) else res
                            summary = f"Yol: {len(path)} durak"
                        else:
                            res = algo.execute(g, start) if start else algo.execute(g)
                            if isinstance(res, list): summary = f"{len(res)} öğe"
                            elif isinstance(res, dict): summary = f"{max(res.values())} renk"
                            else: summary = "İşlendi"
                    except Exception as e:
                        status = f"HATA ({type(e).__name__})"
                        break
                    
                    times.append((time.perf_counter() - start_time) * 1000)

                if status == "BAŞARILI":
                    avg_time = statistics.mean(times)
                    stdev = statistics.stdev(times) if len(times) > 1 else 0
                    self.log(f"| {name} | {status} | {avg_time:.4f} | {stdev:.4f} | {summary} |")
                else:
                    self.log(f"| {name} | {status} | - | - | - |")

        # Negatif Test Senaryosu
        self.log("\n Hatalı Veri Engelleme Kontrolü ")
        self.check_invalid_data(g)

        self.save_report()

    def check_invalid_data(self, graph):
        self.log("\n| Test Edilen Durum | Beklenen Davranış | Sonuç |")
        
        test_node = list(graph.nodes.values())[0]
        res = graph.add_node(test_node)
        self.log(f"| Çift Düğüm Ekleme | Engellenmeli | {'BAŞARILI' if not res else 'HATA'} |")

        try:
            Dijkstra().execute(graph, 9999, 8888)
            self.log("| Geçersiz ID Sorgusu | Güvenli Çıkış | BAŞARILI |")
        except:
            self.log("| Geçersiz ID Sorgusu | Güvenli Çıkış | HATA |")

    def save_report(self):
        filename = "Performans_Raporu.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(self.report_lines))
        print(f"\n[BİLGİ] Test Raporu Kaydedildi. {os.path.abspath(filename)}")

if __name__ == "__main__":
    AdvancedPerformanceTester().run_tests()
