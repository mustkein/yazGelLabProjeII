import csv
import os
from .models import Mekan, Yol

class IstanbulGraf:
    """Graf yapısını ve veri yönetimini kontrol eder. """
    def __init__(self):
        self.dugumler = {} # ID -> Mekan Nesnesi
        self.kenarlar = []

    def mekan_ekle(self, mekan):
        if mekan.id not in self.dugumler:
            self.dugumler[mekan.id] = mekan
        else:
            raise ValueError(f"Düğüm {mekan.id} zaten mevcut!") # [cite: 73]

    def csv_den_yukle(self, dosya_yolu):
        """CSV'den veri okur ve nesneleri oluşturur. [cite: 31, 49]"""
        if not os.path.exists(dosya_yolu):
            print("Dosya bulunamadı!")
            return

        with open(dosya_yolu, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                m = Mekan(
                    row['DugumId'], row['MekanAdi'], 
                    row['Aktiflik'], row['Etkilesim'], row['Baglanti_Sayisi']
                )
                # Komşu stringini listeye çevir (Örn: "2,3" -> [2, 3]) [cite: 56]
                m.komsu_idleri = [int(i.strip()) for i in row['Komsular'].split(',')]
                self.mekan_ekle(m)
        
        self.baglantilari_kur()

    def baglantilari_kur(self):
        """Mekan nesneleri arasındaki Yol (Edge) bağlantılarını oluşturur."""
        self.kenarlar = []
        for mekan in self.dugumler.values():
            for k_id in mekan.komsu_idleri:
                if k_id in self.dugumler:
                    yeni_yol = Yol(mekan, self.dugumler[k_id])
                    self.kenarlar.append(yeni_yol)