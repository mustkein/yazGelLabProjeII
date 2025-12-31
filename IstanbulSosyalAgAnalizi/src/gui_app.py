import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import time
import random
import os
from model import Node
from graph_manager import Graph
from algorithms import BFS, DFS, Dijkstra, AStar, DegreeCentrality, Coloring, ConnectedComponents, FloydWarshall

class TuristRehberiUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("İstanbul Sosyal Ağ Analizi")
        self.root.geometry("1400x900")
        self.graph = Graph()

        self._setup_layout()
        self.create_ui_controls()
        self.create_result_table()

        self.load_scenario("mekanlar_dusuk.csv")

    def _setup_layout(self):
        self.main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        self.left_panel = tk.Frame(self.main_paned, width=350, bg="#f0f0f0", padx=5, pady=5)
        self.main_paned.add(self.left_panel)

        self.right_frame = tk.Frame(self.main_paned, bg="white")
        self.main_paned.add(self.right_frame)

        self.right_paned = tk.PanedWindow(self.right_frame, orient=tk.VERTICAL)
        self.right_paned.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.right_paned, bg="white", height=600)
        self.right_paned.add(self.canvas)
        self.canvas.bind("<Button-1>", self.on_click_node)

        self.table_frame = tk.Frame(self.right_paned, height=250)
        self.right_paned.add(self.table_frame)

    def load_scenario(self, filename):
        try:
            self.graph = Graph()
            self.graph.load_from_csv(filename)
            if not self.graph.nodes:
                messagebox.showwarning("Uyarı", f"{filename} içinde veri bulunamadı!")
                return
            self.draw_map()
            self.update_matrix_view() 
            if hasattr(self, 'lbl_perf'):
                self.lbl_perf.config(text=f"Senaryo Yüklendi: {filename}", fg="green")
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Dosya: {filename}\nHata: {e}")

    def create_ui_controls(self):
        frm_scene = tk.LabelFrame(self.left_panel, text="Test Senaryoları (Ölçek)", padx=5, pady=5, bg="#fff0f5")
        frm_scene.pack(fill=tk.X, pady=5)
        tk.Button(frm_scene, text="Küçük Ölçek (20 Node)", command=lambda: self.load_scenario("mekanlar_dusuk.csv"), bg="#ffb6c1").pack(fill=tk.X, pady=2)
        tk.Button(frm_scene, text="Orta Ölçek (50 Node)", command=lambda: self.load_scenario("mekanlar_orta.csv"), bg="#ff69b4").pack(fill=tk.X, pady=2)

        frm_file = tk.LabelFrame(self.left_panel, text="Dosya İşlemleri", padx=5, pady=5)
        frm_file.pack(fill=tk.X, pady=5)
        tk.Button(frm_file, text="JSON Farklı Kaydet", command=self.save_json, bg="#e1f5fe").grid(row=0, column=0, padx=2, sticky="ew")
        tk.Button(frm_file, text="JSON Yükle", command=self.load_json, bg="#e1f5fe").grid(row=0, column=1, padx=2, sticky="ew")
        tk.Button(frm_file, text="Matris Dosyaya Çıkar", command=self.export_matrix, bg="#e0e0e0").grid(row=1, column=0, columnspan=2, sticky="ew", pady=2)

        frm_crud = tk.LabelFrame(self.left_panel, text="Düğüm Yönetimi", padx=5, pady=5)
        frm_crud.pack(fill=tk.X, pady=5)
        tk.Label(frm_crud, text="ID:").grid(row=0, column=0); self.ent_id = tk.Entry(frm_crud, width=5); self.ent_id.grid(row=0, column=1)
        tk.Label(frm_crud, text="Ad:").grid(row=0, column=2); self.ent_name = tk.Entry(frm_crud, width=10); self.ent_name.grid(row=0, column=3)
        tk.Button(frm_crud, text="Ekle", command=self.add_node_ui, bg="lightgreen").grid(row=1, column=0, columnspan=2, sticky="ew", pady=2)
        tk.Button(frm_crud, text="Güncelle", command=self.update_node_ui, bg="orange").grid(row=1, column=2, columnspan=2, sticky="ew", pady=2)
        tk.Button(frm_crud, text="Seçili ID Sil", command=self.delete_node_ui, bg="#ffcccc").grid(row=2, column=0, columnspan=4, sticky="ew", pady=2)

        frm_edge = tk.LabelFrame(self.left_panel, text="Bağlantı Yönetimi", padx=5, pady=5)
        frm_edge.pack(fill=tk.X, pady=5)
        self.ent_src = tk.Entry(frm_edge, width=5); self.ent_src.pack(side=tk.LEFT)
        tk.Label(frm_edge, text=" <-> ").pack(side=tk.LEFT)
        self.ent_dst = tk.Entry(frm_edge, width=5); self.ent_dst.pack(side=tk.LEFT)
        tk.Button(frm_edge, text="Bağla", command=self.add_edge_ui, bg="#d1c4e9").pack(side=tk.LEFT, padx=5)

        frm_algo = tk.LabelFrame(self.left_panel, text="Algoritmalar & Analiz", padx=5, pady=5)
        frm_algo.pack(fill=tk.X, pady=10)
        self.algo_var = tk.StringVar(value="BFS")
        
        algo_options = ["BFS", "DFS", "Dijkstra", "A*", "Floyd-Warshall", "Degree Centrality", "Coloring", "Connected Components"]
        ttk.Combobox(frm_algo, textvariable=self.algo_var, values=algo_options, state="readonly").pack(fill=tk.X, pady=2)
        
        frm_prm = tk.Frame(frm_algo); frm_prm.pack(fill=tk.X, pady=5)
        tk.Label(frm_prm, text="Baş:").pack(side=tk.LEFT); self.ent_start = tk.Entry(frm_prm, width=5); self.ent_start.pack(side=tk.LEFT, padx=2)
        tk.Label(frm_prm, text="Hed:").pack(side=tk.LEFT); self.ent_end = tk.Entry(frm_prm, width=5); self.ent_end.pack(side=tk.LEFT, padx=2)
        tk.Button(frm_algo, text="ALGORİTMAYI ÇALIŞTIR", bg="#4fc3f7", font=("Arial", 9, "bold"), command=self.run_algorithm, height=2).pack(fill=tk.X, pady=5)
        self.lbl_perf = tk.Label(self.left_panel, text="Süre: 0.000 ms", font=("Consolas", 10, "bold"), fg="blue"); self.lbl_perf.pack(pady=10)

    def create_result_table(self):
        self.tree_frame = tk.Frame(self.table_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.tree_frame, text="Analiz Sonuçları", font=("Arial", 10, "bold")).pack(anchor="w")
        self.tree = ttk.Treeview(self.tree_frame, columns=("C1", "C2", "C3"), show='headings', height=4)
        self.tree.heading("C1", text="Veri/Sıra"); self.tree.heading("C2", text="Mekan Adı"); self.tree.heading("C3", text="Detay")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.matrix_visible = True
        self.matrix_header_frame = tk.Frame(self.table_frame)
        self.matrix_header_frame.pack(fill=tk.X)
        tk.Label(self.matrix_header_frame, text="Anlık Komşuluk Matrisi", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.btn_toggle = tk.Button(self.matrix_header_frame, text="[-] Daralt", command=self.toggle_matrix, width=10)
        self.btn_toggle.pack(side=tk.RIGHT, padx=5)

        self.matrix_container = tk.Frame(self.table_frame)
        self.matrix_container.pack(fill=tk.BOTH, expand=True)

        x_scroll = tk.Scrollbar(self.matrix_container, orient=tk.HORIZONTAL)
        y_scroll = tk.Scrollbar(self.matrix_container, orient=tk.VERTICAL)
        self.txt_matrix = tk.Text(self.matrix_container, height=8, bg="#f8f9fa", font=("Consolas", 9), wrap=tk.NONE,
                                  xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        x_scroll.config(command=self.txt_matrix.xview)
        y_scroll.config(command=self.txt_matrix.yview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_matrix.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def toggle_matrix(self):
        if self.matrix_visible:
            self.matrix_container.pack_forget()
            self.btn_toggle.config(text="[+] Genişlet")
            self.matrix_visible = False
        else:
            self.matrix_container.pack(fill=tk.BOTH, expand=True)
            self.btn_toggle.config(text="[-] Daralt")
            self.matrix_visible = True

def update_matrix_view(self):
        if not hasattr(self.graph, 'get_adjacency_matrix_data'): return
        ids, matrix = self.graph.get_adjacency_matrix_data()
        self.txt_matrix.delete("1.0", tk.END)
        header = "    " + " ".join([f"{str(i):>3}" for i in ids]) + "\n"
        self.txt_matrix.insert(tk.END, header)
        self.txt_matrix.insert(tk.END, "-" * len(header) + "\n")
        for i, row_id in enumerate(ids):
            row_str = f"{str(row_id):<3}|" + " ".join([f"{str(x):>3}" for x in matrix[i]]) + "\n"
            self.txt_matrix.insert(tk.END, row_str)

    def draw_map(self, highlight_path=None, color_map=None):
        self.canvas.delete("all")
        drawn_edges = set()
        for node in self.graph.get_nodes():
            for edge in self.graph.get_neighbors(node.id):
                pair = tuple(sorted((node.id, edge.target.id)))
                if pair not in drawn_edges:
                    color, width = "#cccccc", 1
                    if highlight_path and node.id in highlight_path and edge.target.id in highlight_path:
                        idx1, idx2 = highlight_path.index(node.id), highlight_path.index(edge.target.id)
                        if abs(idx1 - idx2) == 1: color = "red"; width = 3
                    self.canvas.create_line(node.x, node.y, edge.target.x, edge.target.y, fill=color, width=width)
                    mx, my = (node.x + edge.target.x)/2, (node.y + edge.target.y)/2
                    self.canvas.create_text(mx, my, text=f"{int(edge.weight)}", fill="blue", font=("Arial", 7))
                    drawn_edges.add(pair)

        palette = ["#FFADAD", "#9BF6FF", "#CAFFBF", "#FDFFB6", "#FFD6A5", "#99FFFF", "#E0E0E0"]
        for node in self.graph.get_nodes():
            fill_color = palette[(color_map[node.id] - 1) % len(palette)] if color_map and node.id in color_map else "orange"
            if highlight_path and node.id in highlight_path: fill_color = "#32CD32"
            self.canvas.create_oval(node.x-12, node.y-12, node.x+12, node.y+12, fill=fill_color, outline="black")
            self.canvas.create_text(node.x, node.y, text=str(node.id), font=("Arial", 8, "bold"))
            self.canvas.create_text(node.x, node.y+22, text=node.name, font=("Arial", 7, "bold"))

    def run_algorithm(self):
        algo = self.algo_var.get()
        try:
            sid = int(self.ent_start.get()) if self.ent_start.get() else None
            tid = int(self.ent_end.get()) if self.ent_end.get() else None
        except: return
        
        for item in self.tree.get_children(): self.tree.delete(item)
        
        start_time = time.perf_counter()
        result, color_map = None, None
        
        try:
            if algo == "BFS":
                result = BFS().execute(self.graph, sid, tid)
                for idx, nid in enumerate(result, 1):
                    self.tree.insert("", tk.END, values=(f"Sıra {idx}", self.graph.nodes[nid].name, f"ID: {nid}"))
            
            elif algo == "DFS":
                result = DFS().execute(self.graph, sid, tid)
                if not result:
                    messagebox.showinfo("Bilgi", "Yol bulunamadı veya gezilemedi.")
                else:
                    header = "ROTA (DFS)" if tid else "GEZİNME (DFS)"
                    if tid: 
                        path_names = " -> ".join([self.graph.nodes[n].name for n in result])
                        self.tree.insert("", tk.END, values=(header, path_names, f"Adım: {len(result)}"))
                    else:
                        for idx, nid in enumerate(result, 1):
                            self.tree.insert("", tk.END, values=(f"Sıra {idx}", self.graph.nodes[nid].name, f"ID: {nid}"))
            
            elif algo == "Dijkstra":
                result, cost = Dijkstra().execute(self.graph, sid, tid)
                if result:
                    path_names = " -> ".join([self.graph.nodes[n].name for n in result])
                    self.tree.insert("", tk.END, values=("ROTA (Dijkstra)", path_names, f"Maliyet: {cost:.2f}"))

            elif algo == "A*":
                result, cost = AStar().execute(self.graph, sid, tid)
                if result:
                    path_names = " -> ".join([self.graph.nodes[n].name for n in result])
                    self.tree.insert("", tk.END, values=("ROTA (A*)", path_names, f"Maliyet: {cost:.2f}"))
            
            elif algo == "Floyd-Warshall":
                result, cost = FloydWarshall().execute(self.graph, sid, tid)
                if result:
                    path_names = " -> ".join([self.graph.nodes[n].name for n in result])
                    self.tree.insert("", tk.END, values=("ROTA (Floyd-W)", path_names, f"Maliyet: {cost:.2f}"))
            
            elif algo == "Degree Centrality":
                res = DegreeCentrality().execute(self.graph)
                self.tree.insert("", tk.END, values=("SONUÇ", "En Popüler 5 Mekan", ""))
                for idx, (nid, name, count) in enumerate(res, 1):
                    self.tree.insert("", tk.END, values=(f"Top {idx}", name, f"Bağlantı Sayısı: {count}"))
            
            elif algo == "Coloring":
                color_map = Coloring().execute(self.graph)
                for nid in sorted(color_map.keys()):
                    self.tree.insert("", tk.END, values=(f"ID: {nid}", self.graph.nodes[nid].name, f"Renk Grubu: {color_map[nid]}"))
            
            elif algo == "Connected Components":
                comps = ConnectedComponents().execute(self.graph)
                self.tree.insert("", tk.END, values=("SONUÇ", f"{len(comps)} Ayrık Topluluk Bulundu", ""))
                for i, comp in enumerate(comps, 1):
                    self.tree.insert("", tk.END, values=(f"Topluluk {i}", f"{len(comp)} Mekan Var", "-"*10))
                    for nid in comp:
                        node_name = self.graph.nodes[nid].name
                        self.tree.insert("", tk.END, values=("", node_name, f"ID: {nid}"))

            self.lbl_perf.config(text=f"Süre: {(time.perf_counter() - start_time)*1000:.4f} ms")
            self.draw_map(highlight_path=result if isinstance(result, list) else None, color_map=color_map)
        
        except Exception as e: messagebox.showerror("Hata", str(e))

    def on_click_node(self, event):
        for node in self.graph.get_nodes():
            distance = ((node.x - event.x)**2 + (node.y - event.y)**2)**0.5
            if distance <= 15:
                neighbors = [str(e.target.id) for e in self.graph.get_neighbors(node.id)]
                info = (
                    f"  MEKAN BİLGİLERİ  \n"
                    f"ID: {node.id}\n"
                    f"Ad: {node.name}\n"
                    f"Koordinat: ({node.x}, {node.y})\n\n"
                    f" ~ ANALİZ SKORLARI\n"
                    f"Aktiflik Skoru: {node.active_score}\n"
                    f"Sosyal Skor: {node.social_score}\n"
                    f"Bağlantı Sayısı: {node.connection_count}\n\n"
                    f" ~ KOMŞULUKLAR\n"
                    f"Bağlı Mekanlar (ID): {', '.join(neighbors) if neighbors else 'Yok'}"
                )
                messagebox.showinfo(f"Mekan Detayı: {node.name}", info)
                self.ent_id.delete(0, tk.END); self.ent_id.insert(0, str(node.id))
                self.ent_name.delete(0, tk.END); self.ent_name.insert(0, node.name)
                break

    def save_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path and self.graph.save_to_json_path(file_path):
            messagebox.showinfo("Başarılı", "Düğüm yapısı indirildi.")

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.graph.load_from_json(file_path)
            self.draw_map(); self.update_matrix_view(); messagebox.showinfo("Başarılı", "Yüklendi.")

    def add_node_ui(self):
        try:
            new_id_str = self.ent_id.get().strip()
            new_name = self.ent_name.get().strip()
            if not new_id_str or not new_name: messagebox.showwarning("Eksik Bilgi", "Lütfen ID ve Ad alanlarını doldurun."); return
            new_id = int(new_id_str)
            if new_id in self.graph.nodes: messagebox.showerror("Hata", f"ID {new_id} zaten mevcut!"); return
            current_names = [n.name.lower() for n in self.graph.get_nodes()]
            if new_name.lower() in current_names: messagebox.showerror("Hata", f"'{new_name}' isimli bir mekan zaten kayıtlı!"); return
            
            x, y = random.randint(100, 1100), random.randint(100, 550)
            new_node = Node(node_id=new_id, name=new_name, x=x, y=y, active_score=0.5, social_score=500, connection_count=0)
            self.graph.add_node(new_node)
            self.draw_map(); self.update_matrix_view()
            messagebox.showinfo("Başarılı", f"'{new_name}' eklendi."); self.ent_id.delete(0, tk.END); self.ent_name.delete(0, tk.END)
        except ValueError: messagebox.showerror("Geçersiz Giriş", "ID tam sayı olmalı!")

    def update_node_ui(self):
        try:
            if self.graph.update_node(int(self.ent_id.get()), self.ent_name.get()):
                self.draw_map(); self.update_matrix_view(); messagebox.showinfo("Başarılı", "Güncellendi.")
        except: pass

    def delete_node_ui(self):
        try:
            if self.graph.remove_node(int(self.ent_id.get())):
                self.draw_map(); self.update_matrix_view(); messagebox.showinfo("Başarılı", "Silindi.")
        except: pass

    def add_edge_ui(self):
        try:
            self.graph.add_edge(int(self.ent_src.get()), int(self.ent_dst.get()))
            self.draw_map(); self.update_matrix_view()
        except: pass

    def export_matrix(self): self.graph.export_adjacency_matrix(); messagebox.showinfo("Bilgi", "Matris dosyaya çıkarıldı.")
    def save_csv(self): self.graph.save_to_csv(); messagebox.showinfo("Bilgi", "CSV Kaydedildi.")
