import tkinter as tk
from tkinter import messagebox, ttk
import math
import random
import json
import os
from .algorithms import AnalizMotoru
from .models import Mekan, Yol

class IstanbulUI:
    def __init__(self, root, graf):
        self.root = root
        self.graf = graf
        self.root.title("İstanbul Sosyal Ağ Analizi - Proje II")
        self.root.geometry("1300x850")

        # Sidebar (Sol Panel)
        self.sidebar = tk.Frame(self.root, width=300, bg="#97d8e8", padx=10, pady=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Ana Frame (Sağ Panel)
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Canvas (Graf Görselleştirme)
        self.canvas = tk.Canvas(self.main_frame, bg="white", highlightthickness=1)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Komşuluk Listesi Paneli (Sağ Alt)
        tk.Label(self.main_frame, text="Anlık Komşuluk Listesi / Matrisi", font=("Arial", 9, "bold")).pack(anchor="w", padx=10)
        self.txt_komsuluk = tk.Text(self.main_frame, height=10, bg="#f8f9fa", font=("Consolas", 9))
        self.txt_komsuluk.pack(fill=tk.X, padx=5, pady=5)

        self.otomatik_yerlesim_hesapla()
        self._arayuz_elemanlarini_olustur()
        self.grafi_ciz()
        self.update_adjacency_view()

    def _arayuz_elemanlarini_olustur(self):
        """İşlevsel isterlerin tüm butonlarını oluşturur."""
        # --- Düğüm ve Bağlantı Yönetimi ---
        tk.Label(self.sidebar, text="DÜĞÜM/BAĞLANTI YÖNETİMİ", font=("Arial", 10, "bold"), bg="#97d8e8").pack(pady=5)
        
        tk.Label(self.sidebar, text="ID, Ad, Aktiflik, Etkileşim, Bağ.Sayısı", bg="#97d8e8", font=("Arial", 8)).pack()
        self.ent_node_data = tk.Entry(self.sidebar)
        self.ent_node_data.insert(0, "6,Galata,0.8,500,3")
        self.ent_node_data.pack(fill=tk.X, pady=2)
        
        tk.Button(self.sidebar, text="Mekan Ekle / Güncelle", command=self.save_node).pack(fill=tk.X, pady=2)
        tk.Button(self.sidebar, text="Seçili ID'yi Sil", bg="#ff9999", command=self.delete_node).pack(fill=tk.X, pady=2)

        # --- Veri Aktarımı ---
        tk.Label(self.sidebar, text="VERİ İÇE/DIŞA AKTARIM", font=("Arial", 10, "bold"), bg="#97d8e8").pack(pady=(15, 5))
        tk.Button(self.sidebar, text="JSON Olarak Kaydet", command=self.export_json).pack(fill=tk.X, pady=2)
        
        # --- Algoritmalar ---
        tk.Label(self.sidebar, text="ALGORİTMA SEÇİMİ", font=("Arial", 10, "bold"), bg="#97d8e8").pack(pady=(15, 5))
        self.algo_choice = ttk.Combobox(self.sidebar, values=[
            "BFS Arama", "DFS Arama", "Dijkstra En Kısa Yol", "Welsh-Powell Boyama", "Merkezilik Analizi"
        ], state="readonly")
        self.algo_choice.current(0)
        self.algo_choice.pack(fill=tk.X, pady=5)
        
        tk.Label(self.sidebar, text="Başlangıç ID:", bg="#97d8e8").pack(anchor="w")
        self.ent_start = tk.Entry(self.sidebar); self.ent_start.insert(0, "1"); self.ent_start.pack(fill=tk.X)
        tk.Label(self.sidebar, text="Hedef ID:", bg="#97d8e8").pack(anchor="w")
        self.ent_end = tk.Entry(self.sidebar); self.ent_end.insert(0, "4"); self.ent_end.pack(fill=tk.X)
        
        tk.Button(self.sidebar, text="ALGORİTMAYI ÇALIŞTIR", bg="#4CAF50", fg="white", font=("Arial", 9, "bold"), command=self.execute_algo).pack(fill=tk.X, pady=15)

    def save_node(self):
        """Mekan ekleme ve güncelleme (Mükerrer kontrolü dahil)."""
        try:
            parts = self.ent_node_data.get().split(',')
            n_id = int(parts[0].strip())
            n_ad = parts[1].strip()
        
            # 1. ID Kontrolü: Aynı ID varsa eklemeyi engelle veya sor
            if n_id in self.graf.dugumler:
                messagebox.showerror("Hata", f"ID {n_id} zaten mevcut! Lütfen farklı bir ID kullanın.")
                return

            # 2. İsim Kontrolü: Aynı isimde başka bir mekan var mı?
            for mevcut_mekan in self.graf.dugumler.values():
                if mevcut_mekan.ad.lower() == n_ad.lower():
                    messagebox.showwarning("Uyarı", f"'{n_ad}' isimli bir mekan zaten var. Farklı bir isim veriniz.")
                    return
        
            # Ekleme işlemi
            yeni = Mekan(n_id, n_ad, parts[2], parts[3], parts[4])
            yeni.x, yeni.y = random.randint(150, 650), random.randint(150, 450)
            self.graf.dugumler[n_id] = yeni
            self.grafi_ciz()
            self.update_adjacency_view()
            messagebox.showinfo("Başarılı", f"{n_ad} başarıyla eklendi.")
        except Exception as e:
            messagebox.showerror("Hata", "Lütfen verileri ID, Ad, Aktiflik, Etkileşim, Bağlantı formatında girin.")

    def delete_node(self):
        """Düğüm ve ilgili tüm bağlantıları siler."""
        try:
            s_id = int(self.ent_node_data.get().split(',')[0])
            if s_id in self.graf.dugumler:
                del self.graf.dugumler[s_id]
                # Kenarları temizle
                self.graf.kenarlar = [y for y in self.graf.kenarlar if y.kaynak.id != s_id and y.hedef.id != s_id]
                self.grafi_ciz()
                self.update_adjacency_view()
                messagebox.showinfo("Silindi", f"ID {s_id} ve tüm bağlantıları silindi.")
            else:
                messagebox.showwarning("Hata", "Düğüm bulunamadı.")
        except: pass

    def on_canvas_click(self, event):
        """Düğme tıklanınca bilgi gösterme isteri."""
        for m in self.graf.dugumler.values():
            dist = math.sqrt((m.x - event.x)**2 + (m.y - event.y)**2)
            if dist < 25:
                info = f"Ad: {m.ad}\nID: {m.id}\nAktiflik: {m.aktiflik}\nEtkileşim: {m.etkilesim}\nBağlantı: {m.baglanti_sayisi}"
                messagebox.showinfo("Mekan Bilgisi", info)
                return

    def update_adjacency_view(self):
        """Sağ alt köşedeki komşuluk listesini günceller."""
        self.txt_komsuluk.delete("1.0", tk.END)
        self.txt_komsuluk.insert(tk.END, f"{'MEKAN':<20} | {'KOMŞULARI (ID)'}\n")
        self.txt_komsuluk.insert(tk.END, "-"*50 + "\n")
        for m in self.graf.dugumler.values():
            k_ids = [str(y.hedef.id) for y in self.graf.kenarlar if y.kaynak.id == m.id]
            self.txt_komsuluk.insert(tk.END, f"{m.ad:<20} | {', '.join(k_ids)}\n")

    def export_json(self):
        """JSON Dışa Aktarımı ve Komşuluk Listesi Çıktısı."""
        out = {"nodes": [], "adjacency_list": {}}
        for m in self.graf.dugumler.values():
            out["nodes"].append({"id": m.id, "ad": m.ad, "aktiflik": m.aktiflik})
            out["adjacency_list"][m.ad] = [self.graf.dugumler[y.hedef.id].ad for y in self.graf.kenarlar if y.kaynak.id == m.id]
        
        with open("data/cikti_verileri.json", "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Başarılı", "Veriler ve Komşuluk Listesi 'data/cikti_verileri.json' olarak kaydedildi.")

    def otomatik_yerlesim_hesapla(self):
        for m in self.graf.dugumler.values():
            m.x, m.y = random.randint(150, 650), random.randint(150, 450)

    def grafi_ciz(self, vurgu=None):
        self.canvas.delete("all")
        for y in self.graf.kenarlar:
            renk = "red" if vurgu and (y.kaynak, y.hedef) in vurgu else "#bbb"
            self.canvas.create_line(y.kaynak.x, y.kaynak.y, y.hedef.x, y.hedef.y, fill=renk, width=2)
            self.canvas.create_text((y.kaynak.x+y.hedef.x)/2, (y.kaynak.y+y.hedef.y)/2, text=f"{y.agirlik:.1f}", fill="blue", font=("Arial", 8))

            self.canvas.create_text(
                (y.kaynak.x + y.hedef.x) / 2, 
                (y.kaynak.y + y.hedef.y) / 2, 
                text=f"{y.agirlik:.1f}", 
                fill="blue", 
                font=("Arial", 8)
            )
        for m in self.graf.dugumler.values():
            r = 25
            renk = getattr(m, 'renk_kodu', "#ADD8E6")
            self.canvas.create_oval(m.x-r, m.y-r, m.x+r, m.y+r, fill=renk, outline="black")
            self.canvas.create_text(m.x, m.y, text=f"{m.id}\n{m.ad}", font=("Arial", 8, "bold"), justify=tk.CENTER)

    def execute_algo(self):
        sel = self.algo_choice.get()
        try:
            s_id = int(self.ent_start.get())
            if "BFS" in sel:
                res = AnalizMotoru.bfs(self.graf, s_id)
                messagebox.showinfo("BFS", f"Erişilenler: {[m.ad for m in res]}")
            elif "DFS" in sel:
                res = AnalizMotoru.dfs(self.graf, s_id)
                messagebox.showinfo("DFS", f"Erişilenler: {[m.ad for m in res]}")
            elif "Dijkstra" in sel:
                e_id = int(self.ent_end.get())
                yol, maliyet = AnalizMotoru.dijkstra(self.graf, s_id, e_id)
                vurgu = [(yol[i], yol[i+1]) for i in range(len(yol)-1)]
                self.grafi_ciz(vurgu)
                messagebox.showinfo("Rota", f"Maliyet: {maliyet:.2f}\n{' -> '.join([m.ad for m in yol])}")
            elif "Welsh" in sel:
                self.run_welsh_powell()
            elif "Merkezilik" in sel:
                self.run_centrality_table()
        except Exception as e:
            messagebox.showerror("Hata", f"İşlem Hatası: {e}")

    def run_welsh_powell(self):
        palet = ["#FFADAD", "#9BF6FF", "#CAFFBF", "#FDFFB6", "#FFD6A5"]
        sonuc = AnalizMotoru.welsh_powell(self.graf)
        top = tk.Toplevel(self.root)
        top.title("Boyama Tablosu")
        tree = ttk.Treeview(top, columns=("Mekan", "Grup"), show='headings')
        tree.heading("Mekan", text="Mekan"); tree.heading("Grup", text="Grup (Renk)")
        for d_id, r_id in sonuc.items():
            m = self.graf.dugumler[d_id]
            m.renk_kodu = palet[r_id % len(palet)]
            tree.insert("", "end", values=(m.ad, f"Grup {r_id}"))
        tree.pack(padx=10, pady=10); self.grafi_ciz()

    def run_centrality_table(self):
        etkililer = AnalizMotoru.merkezilik_analizi(self.graf)
        top = tk.Toplevel(self.root)
        top.title("Merkezilik - Top 5")
        tree = ttk.Treeview(top, columns=("Mekan", "Derece"), show='headings')
        tree.heading("Mekan", text="Mekan"); tree.heading("Derece", text="Bağlantı Derecesi")
        for m in etkililer: tree.insert("", "end", values=(m.ad, m.baglanti_sayisi))
        tree.pack(padx=10, pady=10)