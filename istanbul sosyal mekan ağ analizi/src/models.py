import math

class Mekan:
    """ Node """
    def __init__(self, id, ad, aktiflik, etkilesim, baglanti_sayisi, x=0, y=0):
        self.id = int(id)
        self.ad = ad
        self.aktiflik = float(aktiflik)      # Özellik I 
        self.etkilesim = float(etkilesim)    # Özellik II 
        self.baglanti_sayisi = int(baglanti_sayisi) # Özellik III 
        self.x = 0  # Görselleştirme ve A* için koordinat
        self.y = 0
        self.komsu_idleri = [] # CSV'den gelen ham liste
        self.renk = "add8e6"    # Welsh-Powell için


class Yol:
    """ Edge """
    def __init__(self, kaynak, hedef):
        self.kaynak = kaynak # Mekan nesnesi
        self.hedef = hedef   # Mekan nesnesi
        self.agirlik = self.dinamik_agirlik_hesapla()

    def dinamik_agirlik_hesapla(self):
        """formül: 1 + sqrt((A1-A2)^2 + (E1-E2)^2 + (B1-B2)^2)"""
        d_aktiflik = (self.kaynak.aktiflik - self.hedef.aktiflik) ** 2
        d_etkilesim = (self.kaynak.etkilesim - self.hedef.etkilesim) ** 2
        d_baglanti = (self.kaynak.baglanti_sayisi - self.hedef.baglanti_sayisi) ** 2
        
        # Farklar arttıkça maliyet artar, mesafe uzar.
        return 1 + math.sqrt(d_aktiflik + d_etkilesim + d_baglanti)