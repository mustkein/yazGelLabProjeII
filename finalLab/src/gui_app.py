import tkinter as tk
from tkinter import messagebox, ttk
import time
import random
import os
from model import Node
from graph_manager import Graph
from algorithms import BFS, DFS, Dijkstra, AStar, DegreeCentrality, Coloring, ConnectedComponents
from tkinter import filedialog

class TuristRehberiUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("İstanbul Sosyal Ağ Analizi")
        self.root.geometry("1400x900")
        self.graph = Graph()

        # --- ARAYÜZ
        self._setup_layout()
        self.create_ui_controls()
        self.create_result_table()

        # --- BAŞLANGIÇ VERİSİNİ YÜKLE ---
        # default düşük ölçek
        self.load_scenario("mekanlar_dusuk.csv")

    def _setup_layout(self):
        """Ana düzeni ve Canvas yapısını kurar."""
        self.main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # Sol Panel
        self.left_panel = tk.Frame(self.main_paned, width=350, bg="#f0f0f0", padx=5, pady=5)
        self.main_paned.add(self.left_panel)

        # Sağ Panel
        self.right_frame = tk.Frame(self.main_paned, bg="white")
        self.main_paned.add(self.right_frame)

        self.right_paned = tk.PanedWindow(self.right_frame, orient=tk.VERTICAL)
        self.right_paned.pack(fill=tk.BOTH, expand=True)

        # Tablo Alanı
        self.table_frame = tk.Frame(self.right_paned, height=200)
        self.right_paned.add(self.table_frame)

        # Harita Alanı
        self.canvas = tk.Canvas(self.right_paned, bg="white", height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def load_scenario(self, filename):
        """CSV dosyasını yükler ve görselleştirir."""
        try:
            self.graph = Graph()
            self.graph.load_from_csv(filename)
            
            if not self.graph.nodes:
                messagebox.showwarning("Uyarı", f"{filename} içinde veri bulunamadı!")
                return
            
            self.draw_map()
            if hasattr(self, 'lbl_perf'):
                self.lbl_perf.config(text=f"Senaryo Yüklendi: {filename}", fg="green")
            print(f"[LOG] {len(self.graph.nodes)} düğüm haritaya yerleştirildi.")
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Dosya: {filename}\nHata: {e}")

    def create_ui_controls(self):
        """Tüm butonları ve giriş alanlarını eksiksiz oluşturur."""
        
        #  TEST SENARYOLARI (ÖLÇEK SEÇİMİ)
        frm_scene = tk.LabelFrame(self.left_panel, text="Test Senaryoları (Ölçek)", padx=5, pady=5, bg="#fff0f5")
        frm_scene.pack(fill=tk.X, pady=5)
        
        tk.Button(frm_scene, text="Küçük Ölçek (20 Node)", 
                  command=lambda: self.load_scenario("mekanlar_dusuk.csv"), bg="#ffb6c1").pack(fill=tk.X, pady=2)
        
        tk.Button(frm_scene, text="Orta Ölçek (50 Node)", 
                  command=lambda: self.load_scenario("mekanlar_orta.csv"), bg="#ff69b4").pack(fill=tk.X, pady=2)

        # 1. DOSYA İŞLEMLERİ
        frm_file = tk.LabelFrame(self.left_panel, text="Dosya ve Veri İşlemleri", padx=5, pady=5)
        frm_file.pack(fill=tk.X, pady=5)
        
        tk.Button(frm_file, text="JSON Kaydet", command=self.save_json, bg="#e1f5fe").grid(row=0, column=0, padx=2, sticky="ew")
        tk.Button(frm_file, text="JSON Yükle", command=self.load_json, bg="#e1f5fe").grid(row=0, column=1, padx=2, sticky="ew")
        tk.Button(frm_file, text="CSV Kaydet", command=self.save_csv, bg="#fff9c4").grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        tk.Button(frm_file, text="Matris Çıkar", command=self.export_matrix, bg="#e0e0e0").grid(row=1, column=1, padx=2, sticky="ew")

        # 2. DÜĞÜM YÖNETİMİ (CRUD)
        frm_crud = tk.LabelFrame(self.left_panel, text="Düğüm Yönetimi", padx=5, pady=5)
        frm_crud.pack(fill=tk.X, pady=5)

        tk.Label(frm_crud, text="ID:").grid(row=0, column=0)
        self.ent_id = tk.Entry(frm_crud, width=5); self.ent_id.grid(row=0, column=1)
        tk.Label(frm_crud, text="Ad:").grid(row=0, column=2)
        self.ent_name = tk.Entry(frm_crud, width=10); self.ent_name.grid(row=0, column=3)

        tk.Button(frm_crud, text="Ekle", command=self.add_node_ui, bg="lightgreen").grid(row=1, column=0, columnspan=2, sticky="ew", pady=2)
        tk.Button(frm_crud, text="Güncelle", command=self.update_node_ui, bg="orange").grid(row=1, column=2, columnspan=2, sticky="ew", pady=2)
        tk.Button(frm_crud, text="Seçili ID Sil", command=self.delete_node_ui, bg="#ffcccc").grid(row=2, column=0, columnspan=4, sticky="ew", pady=2)

        # 3. KENAR YÖNETİMİ
        frm_edge = tk.LabelFrame(self.left_panel, text="Bağlantı (Kenar) Yönetimi", padx=5, pady=5)
        frm_edge.pack(fill=tk.X, pady=5)
        self.ent_src = tk.Entry(frm_edge, width=5); self.ent_src.pack(side=tk.LEFT)
        tk.Label(frm_edge, text=" <-> ").pack(side=tk.LEFT)
        self.ent_dst = tk.Entry(frm_edge, width=5); self.ent_dst.pack(side=tk.LEFT)
        tk.Button(frm_edge, text="Bağla", command=self.add_edge_ui, bg="#d1c4e9").pack(side=tk.LEFT, padx=5)

        # 4. ALGORİTMALAR
        frm_algo = tk.LabelFrame(self.left_panel, text="Algoritmalar & Analiz", padx=5, pady=5)
        frm_algo.pack(fill=tk.X, pady=10)

        self.algo_var = tk.StringVar(value="BFS")
        options = ["BFS", "DFS", "Dijkstra", "A*", "Degree Centrality", "Coloring", "Connected Components"]
        self.cmb_algo = ttk.Combobox(frm_algo, textvariable=self.algo_var, values=options, state="readonly")
        self.cmb_algo.pack(fill=tk.X, pady=2)

        frm_prm = tk.Frame(frm_algo)
        frm_prm.pack(fill=tk.X, pady=5)
        tk.Label(frm_prm, text="Başlangıç:").pack(side=tk.LEFT)
        self.ent_start = tk.Entry(frm_prm, width=5); self.ent_start.pack(side=tk.LEFT, padx=2)
        tk.Label(frm_prm, text="Hedef:").pack(side=tk.LEFT)
        self.ent_end = tk.Entry(frm_prm, width=5); self.ent_end.pack(side=tk.LEFT, padx=2)

        tk.Button(frm_algo, text="ALGORİTMAYI ÇALIŞTIR", bg="#4fc3f7", font=("Arial", 9, "bold"), 
                  command=self.run_algorithm, height=2).pack(fill=tk.X, pady=5)

        # 5. PERFORMANS ETİKETİ
        self.lbl_perf = tk.Label(self.left_panel, text="Süre: 0.000 ms", font=("Consolas", 10, "bold"), fg="blue")
        self.lbl_perf.pack(pady=10)

    def create_result_table(self):
        """Treeview sonuç tablosunu oluşturur."""
        tk.Label(self.table_frame, text="Analiz Sonuç Tablosu", font=("Arial", 10, "bold")).pack(anchor="w")
        self.tree_scroll = tk.Scrollbar(self.table_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(self.table_frame, columns=("C1", "C2", "C3"), show='headings', yscrollcommand=self.tree_scroll.set)
        self.tree.heading("C1", text="Veri/Sıra"); self.tree.heading("C2", text="Düğüm/Mekan"); self.tree.heading("C3", text="Detay/Renk")
        self.tree.column("C1", width=100); self.tree.column("C2", width=250); self.tree.column("C3", width=200)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.tree.yview)

    def draw_map(self, highlight_path=None, color_map=None):
        """Grafı Canvas üzerine çizer ve renklendirir."""
        self.canvas.delete("all")
        
        # Kenarları Çiz
        drawn_edges = set()
        for node in self.graph.get_nodes():
            for edge in self.graph.get_neighbors(node.id):
                pair = tuple(sorted((node.id, edge.target.id)))
                if pair not in drawn_edges:
                    color = "#cccccc"
                    width = 1
                    # Yol Vurgulama (Dijkstra/BFS)
                    if highlight_path and node.id in highlight_path and edge.target.id in highlight_path:
                        idx1, idx2 = highlight_path.index(node.id), highlight_path.index(edge.target.id)
                        if abs(idx1 - idx2) == 1:
                            color = "red"; width = 3
                    
                    self.canvas.create_line(node.x, node.y, edge.target.x, edge.target.y, fill=color, width=width)
                    # Küçük graflarda ağırlık göster
                    if len(self.graph.nodes) < 100:
                        mx, my = (node.x + edge.target.x)/2, (node.y + edge.target.y)/2
                        self.canvas.create_text(mx, my, text=f"{int(edge.weight)}", fill="blue", font=("Arial", 7))
                    drawn_edges.add(pair)

        # Düğümleri Çiz
        palette = ["#FFADAD", "#9BF6FF", "#CAFFBF", "#FDFFB6", "#FFD6A5", "#99FFFF", "#E0E0E0", "#D4FC79"]
        for node in self.graph.get_nodes():
            fill_color = "orange"
            if color_map and node.id in color_map:
                fill_color = palette[(color_map[node.id] - 1) % len(palette)]
            elif highlight_path and node.id in highlight_path:
                fill_color = "#32CD32" # Yol üzerindekiler

            r = 15 if len(self.graph.nodes) < 30 else 10
            self.canvas.create_oval(node.x-r, node.y-r, node.x+r, node.y+r, fill=fill_color, outline="black")
            self.canvas.create_text(node.x, node.y, text=str(node.id), font=("Arial", 8, "bold"))
            
            if len(self.graph.nodes) < 30:
                self.canvas.create_text(node.x, node.y+22, text=node.name, font=("Arial", 7, "bold"))

    def on_click_node(self, event):
        """Düğüm tıklandığında detayları gösterir."""
        for node in self.graph.get_nodes():
            distance = ((node.x - event.x)**2 + (node.y - event.y)**2)**0.5
            if distance <= 15:
                neighbors = [str(e.target.id) for e in self.graph.get_neighbors(node.id)]
                info = (f"Mekan: {node.name}\nID: {node.id}\n"
                        f"Sosyal Skor: {node.social_score}\n"
                        f"Komşular: {', '.join(neighbors)}")
                messagebox.showinfo("Düğüm Bilgisi", info)
                # Formu doldur
                self.ent_id.delete(0, tk.END); self.ent_id.insert(0, str(node.id))
                self.ent_name.delete(0, tk.END); self.ent_name.insert(0, node.name)
                break

    def run_algorithm(self):
        """Seçilen algoritmayı çalıştırır ve sonuçları tabloya aktarır."""
        algo = self.algo_var.get()
        # Giriş alanlarından ID'leri al
        try:
            sid = int(self.ent_start.get()) if self.ent_start.get() else None
            tid = int(self.ent_end.get()) if self.ent_end.get() else None
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli sayısal ID değerleri girin.")
            return

        # Mevcut tabloyu temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        start_time = time.perf_counter()
        result, color_map = None, None

        try:
            if algo == "BFS":
                # BFS sadece gezinme sırasını döndürür
                result = BFS().execute(self.graph, sid, tid)
                if result:
                    for idx, nid in enumerate(result, 1):
                        name = self.graph.nodes[nid].name
                        # Tabloya ekle
                        self.tree.insert("", tk.END, values=(f"Sıra {idx}", name, f"ID: {nid}"))
                else:
                    messagebox.showinfo("Bilgi", "Yol bulunamadı.")
                
                if algo == "Dijkstra":
                    # Dijkstra yol ve maliyet hesapla
                    result, cost = Dijkstra().execute(self.graph, sid, tid)
                    if result:
                      path_names = " -> ".join([self.graph.nodes[n].name for n in result])
                      self.tree.insert("", tk.END, values=("EN KISA ROTA", path_names, f"Toplam Maliyet: {cost:.2f}"))
                    else:
                      messagebox.showinfo("Bilgi", "Hedefe ulaşan bir yol bulunamadı.")

                
                elif algo == "Degree Centrality":
                    # En popüler 5 mekan
                    res = DegreeCentrality().execute(self.graph)
                    for idx, (nid, name, count) in enumerate(res, 1):
                        # Tabloya ekle
                        self.tree.insert("", tk.END, values=(f"Top {idx}", name, f"Bağlantı Sayısı: {count}"))

                elif algo == "Coloring":
                     # Coloring düğüm:renk haritası döndürür
                     color_map = Coloring().execute(self.graph)
                     for nid in sorted(color_map.keys()):
                        name = self.graph.nodes[nid].name
                        self.tree.insert("", tk.END, values=(f"ID: {nid}", name, f"Renk Grubu: {color_map[nid]}"))

                # Süre ölçümünü güncelle
                exec_time = (time.perf_counter() - start_time) * 1000
                self.lbl_perf.config(text=f"Süre: {exec_time:.4f} ms")

                # Haritayı güncelle (Yolu vurgula veya Renklendir)
                self.draw_map(highlight_path=result if isinstance(result, list) else None, color_map=color_map)  

        except Exception as e:
            messagebox.showerror("Algoritma Hatası", f"İşlem başarısız: {e}")

    # --- CRUD VE DOSYA İŞLEMLERİ ---
    def add_node_ui(self):
        try:
            nid = int(self.ent_id.get())
            name = self.ent_name.get()
            new_node = Node(nid, name, random.randint(100, 1000), random.randint(100, 600), 0.5, 500, 1)
            self.graph.add_node(new_node)
            self.draw_map(); messagebox.showinfo("Başarılı", "Düğüm eklendi.")
        except: messagebox.showerror("Hata", "Geçerli ID ve Ad girin.")

    def update_node_ui(self):
        try:
            nid = int(self.ent_id.get())
            self.graph.update_node(nid, name=self.ent_name.get())
            self.draw_map(); messagebox.showinfo("Başarılı", "Güncellendi.")
        except: pass

    def delete_node_ui(self):
        try:
            nid = int(self.ent_id.get())
            self.graph.remove_node(nid)
            self.draw_map()
        except: pass

    def add_edge_ui(self):
        try:
            u, v = int(self.ent_src.get()), int(self.ent_dst.get())
            self.graph.add_edge(u, v)
            self.draw_map()
        except: pass

    def save_json(self): self.graph.to_json(); messagebox.showinfo("Bilgi", "JSON Kaydedildi.")
    def load_json(self): self.graph.load_from_json(); self.draw_map()
    def save_csv(self): self.graph.save_to_csv(); messagebox.showinfo("Bilgi", "CSV Kaydedildi.")
    def export_matrix(self): self.graph.export_adjacency_matrix(); messagebox.showinfo("Bilgi", "Matris Çıkarıldı.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TuristRehberiUygulamasi(root)
    root.mainloop()
 
    def save_json(self):
        """Güncel düğüm yapısını bilgisayara bir dosya olarak kaydeder."""
        # Kullanıcıya nereye kaydetmek istediğini soran pencereyi aç
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Güncel Graf Yapısını Kaydet"
        )
        
        if file_path:
            success = self.graph.save_to_json_path(file_path)
            if success:
                messagebox.showinfo("Başarılı", f"Güncel düğüm yapısı başarıyla kaydedildi:\n{file_path}")
            else:
                messagebox.showerror("Hata", "Dosya kaydedilirken bir sorun oluştu.")

    def load_json(self):
        """Bilgisayardan bir JSON dosyası seçerek yükler."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Yüklenecek Graf Dosyasını Seçin"
        )
        
        if file_path:
            try:
                self.graph.load_from_json(file_path)
                self.draw_map()
                messagebox.showinfo("Başarılı", "Düğüm yapısı yüklendi.")
            except Exception as e:
                messagebox.showerror("Hata", f"Yükleme başarısız: {e}")