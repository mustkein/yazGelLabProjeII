# Dosya Adı: gui_app.py

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from model import Node
from graph_manager import Graph
from algorithms import BFS, DFS, Dijkstra, AStar, DegreeCentrality, Coloring, ConnectedComponents

class TuristRehberiUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Project - Interactive Manager")
        self.root.geometry("1200x800")

        self.graph = Graph()
        self.load_initial_data() # Başlangıç verisi

        # --- ANA DÜZEN (Sol: Kontrol, Sağ: Canvas) ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # SOL PANEL (Scrollable yapılabilir ama basit tutuyoruz)
        self.left_panel = tk.Frame(self.main_frame, width=300, bg="#f0f0f0", padx=10, pady=10)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        # SAĞ PANEL (Canvas)
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click_node)

        # --- ARAYÜZ ELEMANLARI ---
        self.create_ui_controls()
        self.draw_map()

    def load_initial_data(self):
        # Varsayılan İstanbul verisi
        nodes = [
            Node(1, "Suleymaniye", 150, 250, 0.8, 400, 3),
            Node(2, "Sultanahmet", 200, 300, 0.9, 600, 4),
            Node(3, "Grand Bazaar", 180, 200, 0.95, 350, 5),
            Node(4, "Galata Tower", 400, 150, 0.95, 950, 3),
        ]
        for n in nodes: self.graph.add_node(n)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(1, 4)

    def create_ui_controls(self):
        # 1. DOSYA İŞLEMLERİ (JSON)
        lbl_file = tk.Label(self.left_panel, text="Dosya İşlemleri", font=("Arial", 10, "bold"), bg="#f0f0f0")
        lbl_file.pack(anchor="w", pady=(0, 5))
        
        frm_file = tk.Frame(self.left_panel)
        frm_file.pack(fill=tk.X, pady=5)
        tk.Button(frm_file, text="Kaydet (JSON)", command=self.save_json, bg="#dddddd").pack(side=tk.LEFT, padx=2)
        tk.Button(frm_file, text="Yükle (JSON)", command=self.load_json, bg="#dddddd").pack(side=tk.LEFT, padx=2)

        tk.Frame(self.left_panel, height=2, bg="grey").pack(fill=tk.X, pady=10)

        # 2. DÜĞÜM/KENAR YÖNETİMİ (CRUD)
        lbl_crud = tk.Label(self.left_panel, text="Düzenleme (CRUD)", font=("Arial", 10, "bold"), bg="#f0f0f0")
        lbl_crud.pack(anchor="w")

        # Ekleme Alanı
        self.ent_node_name = tk.Entry(self.left_panel)
        self.ent_node_name.insert(0, "Mekan İsmi")
        self.ent_node_name.pack(fill=tk.X, pady=2)
        
        btn_add_node = tk.Button(self.left_panel, text="+ Yeni Düğüm Ekle (Rastgele Konum)", command=self.add_node_ui)
        btn_add_node.pack(fill=tk.X, pady=2)

        # Silme Alanı
        frm_del = tk.Frame(self.left_panel)
        frm_del.pack(fill=tk.X, pady=5)
        self.ent_del_id = tk.Entry(frm_del, width=5)
        self.ent_del_id.pack(side=tk.LEFT)
        tk.Button(frm_del, text="ID Sil", command=self.delete_node_ui).pack(side=tk.LEFT, padx=5)

        # Kenar Ekleme
        frm_edge = tk.Frame(self.left_panel)
        frm_edge.pack(fill=tk.X, pady=5)
        self.ent_edge_src = tk.Entry(frm_edge, width=5); self.ent_edge_src.pack(side=tk.LEFT)
        tk.Label(frm_edge, text="->").pack(side=tk.LEFT)
        self.ent_edge_dst = tk.Entry(frm_edge, width=5); self.ent_edge_dst.pack(side=tk.LEFT)
        tk.Button(frm_edge, text="Bağla", command=self.add_edge_ui).pack(side=tk.LEFT, padx=5)

        tk.Frame(self.left_panel, height=2, bg="grey").pack(fill=tk.X, pady=10)

        # 3. ALGORİTMALAR
        lbl_algo = tk.Label(self.left_panel, text="Algoritmalar", font=("Arial", 10, "bold"), bg="#f0f0f0")
        lbl_algo.pack(anchor="w")

        # Seçenekler
        self.algo_var = tk.StringVar(value="BFS")
        options = ["BFS", "DFS", "Dijkstra", "A*", "Degree Centrality", "Coloring", "Connected Components"]
        self.cmb_algo = ttk.Combobox(self.left_panel, textvariable=self.algo_var, values=options, state="readonly")
        self.cmb_algo.pack(fill=tk.X, pady=5)

        # Parametreler (Start / Target)
        frm_params = tk.Frame(self.left_panel)
        frm_params.pack(fill=tk.X)
        tk.Label(frm_params, text="Start ID:").pack(side=tk.LEFT)
        self.ent_start = tk.Entry(frm_params, width=5); self.ent_start.pack(side=tk.LEFT, padx=2)
        tk.Label(frm_params, text="End ID:").pack(side=tk.LEFT)
        self.ent_target = tk.Entry(frm_params, width=5); self.ent_target.pack(side=tk.LEFT, padx=2)

        # Çalıştır Butonu
        btn_run = tk.Button(self.left_panel, text="ALGORİTMAYI ÇALIŞTIR", bg="lightblue", command=self.run_algorithm)
        btn_run.pack(fill=tk.X, pady=10)

        # SONUÇ EKRANI (Text Area)
        lbl_res = tk.Label(self.left_panel, text="Sonuçlar:", font=("Arial", 10, "bold"), bg="#f0f0f0")
        lbl_res.pack(anchor="w")
        self.txt_result = tk.Text(self.left_panel, height=10, width=30)
        self.txt_result.pack(fill=tk.X)

    # --- UI EVENTLERİ ---
    def add_node_ui(self):
        try:
            name = self.ent_node_name.get()
            # Otomatik ID ve Rastgele Koordinat
            new_id = max(self.graph.nodes.keys(), default=0) + 1
            import random
            x, y = random.randint(50, 600), random.randint(50, 600)
            
            # Varsayılan değerlerle ekle (Kullanıcı bunları güncelleyebilmeli ama şimdilik hızlı ekleme)
            n = Node(new_id, name, x, y, 0.5, 100, 1)
            self.graph.add_node(n)
            self.draw_map()
            messagebox.showinfo("Başarılı", f"Düğüm Eklendi: ID {new_id}")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def delete_node_ui(self):
        try:
            nid = int(self.ent_del_id.get())
            self.graph.remove_node(nid)
            self.draw_map()
        except:
            messagebox.showerror("Hata", "Geçerli bir ID girin.")

    def add_edge_ui(self):
        try:
            u, v = int(self.ent_edge_src.get()), int(self.ent_edge_dst.get())
            self.graph.add_edge(u, v)
            self.draw_map()
        except:
             messagebox.showerror("Hata", "ID'leri kontrol edin.")

    def save_json(self):
        self.graph.to_json("graph_data.json")
        messagebox.showinfo("Bilgi", "graph_data.json olarak kaydedildi.")

    def load_json(self):
        self.graph.load_from_json("graph_data.json")
        self.draw_map()

    def run_algorithm(self):
        algo_name = self.algo_var.get()
        start_id = self.ent_start.get()
        target_id = self.ent_target.get()
        
        # ID dönüşümleri
        sid = int(start_id) if start_id else None
        tid = int(target_id) if target_id else None

        result_text = ""
        color_map = None

        try:
            if algo_name == "BFS":
                alg = BFS()
                res = alg.execute(self.graph, start_id=sid)
                result_text = f"BFS Gezinme Sırası:\n{res}"
            
            elif algo_name == "DFS":
                alg = DFS()
                res = alg.execute(self.graph, start_id=sid)
                result_text = f"DFS Gezinme Sırası:\n{res}"

            elif algo_name == "Dijkstra":
                alg = Dijkstra()
                path, cost = alg.execute(self.graph, start_id=sid, target_id=tid)
                result_text = f"En Kısa Yol: {path}\nMaliyet: {cost:.2f}"

            elif algo_name == "A*":
                alg = AStar()
                path, cost = alg.execute(self.graph, start_id=sid, target_id=tid)
                result_text = f"A* Yolu: {path}\nMaliyet: {cost:.2f}"

            elif algo_name == "Degree Centrality":
                alg = DegreeCentrality()
                res = alg.execute(self.graph)
                result_text = "En Popüler 5 Mekan:\n"
                for count, name, nid in res:
                    result_text += f"{name} (ID:{nid}) - Bağ: {count}\n"

            elif algo_name == "Coloring":
                alg = Coloring()
                color_map = alg.execute(self.graph)
                result_text = "Harita Renklendirildi.\nGörsele bakın."

            elif algo_name == "Connected Components":
                alg = ConnectedComponents()
                comps = alg.execute(self.graph)
                result_text = f"Ayrık Topluluk Sayısı: {len(comps)}\n"
                for i, comp in enumerate(comps, 1):
                    result_text += f"Topluluk {i}: {comp}\n"

            # Sonucu Yazdır
            self.txt_result.delete(1.0, tk.END)
            self.txt_result.insert(tk.END, result_text)
            
            # Haritayı (varsa renklendirme ile) güncelle
            self.draw_map(color_map)

        except Exception as e:
            messagebox.showerror("Algoritma Hatası", f"Hata: {str(e)}\nInputları kontrol edin.")

    def draw_map(self, color_map=None):
        self.canvas.delete("all")
        
        # Kenarlar
        drawn_edges = set()
        for node in self.graph.get_nodes():
            for edge in self.graph.get_neighbors(node.id):
                pair = tuple(sorted((node.id, edge.target.id)))
                if pair not in drawn_edges:
                    self.canvas.create_line(node.x, node.y, edge.target.x, edge.target.y, fill="gray", width=2)
                    mid_x, mid_y = (node.x + edge.target.x)/2, (node.y + edge.target.y)/2
                    self.canvas.create_text(mid_x, mid_y, text=str(int(edge.weight)), fill="red", font=("Arial", 8))
                    drawn_edges.add(pair)

        # Düğümler
        for node in self.graph.get_nodes():
            color = "orange"
            if color_map and node.id in color_map:
                palette = ["#FF9999", "#99FF99", "#9999FF", "#FFFF99", "#FF99FF", "#99FFFF"]
                idx = (color_map[node.id] - 1) % len(palette)
                color = palette[idx]

            r = 20
            self.canvas.create_oval(node.x-r, node.y-r, node.x+r, node.y+r, fill=color, outline="black")
            self.canvas.create_text(node.x, node.y, text=str(node.id), font=("Arial", 10, "bold"))
            self.canvas.create_text(node.x, node.y+30, text=node.name, font=("Arial", 8))

    def on_click_node(self, event):
        x, y = event.x, event.y
        for node in self.graph.get_nodes():
            if ((node.x - x)**2 + (node.y - y)**2)**0.5 <= 20:
                info = f"ID: {node.id}\nName: {node.name}\nActive: {node.active_score}\nSocial: {node.social_score}"
                messagebox.showinfo("Node Info", info)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = TuristRehberiUygulamasi(root)
    root.mainloop()