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

    