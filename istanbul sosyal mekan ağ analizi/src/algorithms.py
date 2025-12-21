import heapq
from collections import deque

class AnalizMotoru:
    """Graf üzerindeki tüm arama ve yol bulma algoritmalarını yönetir."""

    @staticmethod
    def dfs(graf, baslangic_id):
        """DFS algoritması ile erişilebilen tüm kullanıcıları bulma"""
        ziyaret_edilen = set()
        yigin = [baslangic_id]
        sonuc = []
        while yigin:
            dugum_id = yigin.pop()
            if dugum_id not in ziyaret_edilen:
                ziyaret_edilen.add(dugum_id)
                sonuc.append(graf.dugumler[dugum_id])
                # Komşuları yığına ekle
                for yol in graf.kenarlar:
                    if yol.kaynak.id == dugum_id:
                        yigin.append(yol.hedef.id)
        return sonuc
    
    @staticmethod
    def bfs(graf, baslangic_id):
        """BFS ile bir düğümden erişilebilen tüm kullanıcıları (mekanları) bulur."""
        ziyaret_edilen = set()
        kuyruk = deque([baslangic_id])
        sonuc = []

        while kuyruk:
            dugum_id = kuyruk.popleft()
            if dugum_id not in ziyaret_edilen:
                ziyaret_edilen.add(dugum_id)
                sonuc.append(graf.dugumler[dugum_id])
                
                # Komşuları kuyruğa ekle
                for yol in graf.kenarlar:
                    if yol.kaynak.id == dugum_id:
                        kuyruk.append(yol.hedef.id)
        return sonuc

    @staticmethod
    def dijkstra(graf, baslangic_id, hedef_id):
        """Dijkstra algoritması ile iki mekan arasındaki en kısa yolu bulur."""
        mesafeler = {id: float('inf') for id in graf.dugumler}
        mesafeler[baslangic_id] = 0
        onceki_dugumler = {id: None for id in graf.dugumler}
        
        pq = [(0, baslangic_id)] # (mesafe, dugum_id)

        while pq:
            mevcut_mesafe, u_id = heapq.heappop(pq)

            if u_id == hedef_id:
                break

            if mevcut_mesafe > mesafeler[u_id]:
                continue

            # Mevcut düğümden çıkan kenarları kontrol et
            for yol in graf.kenarlar:
                if yol.kaynak.id == u_id:
                    v_id = yol.hedef.id
                    yeni_mesafe = mevcut_mesafe + yol.agirlik # Dinamik ağırlık kullanılıyor 
                    
                    if yeni_mesafe < mesafeler[v_id]:
                        mesafeler[v_id] = yeni_mesafe
                        onceki_dugumler[v_id] = u_id
                        heapq.heappush(pq, (yeni_mesafe, v_id))

        # Yolu geri oluştur
        yol_sonucu = []
        su_an = hedef_id
        while su_an is not None:
            yol_sonucu.insert(0, graf.dugumler[su_an])
            su_an = onceki_dugumler[su_an]
            
        return yol_sonucu, mesafeler[hedef_id]

    @staticmethod
    def welsh_powell(graf):
        """Graf renklendirme algoritması."""
        # 1. Düğümleri derecelerine göre azalan sırada diz 
        dugumler = list(graf.dugumler.values())
        dugumler.sort(key=lambda x: x.baglanti_sayisi, reverse=True)
        
        renk_haritasi = {} # dugum_id: renk_id
        mevcut_renk = 0
        
        boyanmamislar = dugumler[:]
        
        while boyanmamislar:
            mevcut_renk += 1
            gecici_boyananlar = []
            
            for d in boyanmamislar[:]:
                # Komşularıyla aynı renkte değilse boya
                komsu_renkleri = []
                for yol in graf.kenarlar:
                    if yol.kaynak.id == d.id and yol.hedef.id in renk_haritasi:
                        komsu_renkleri.append(renk_haritasi[yol.hedef.id])
                
                if mevcut_renk not in komsu_renkleri:
                    renk_haritasi[d.id] = mevcut_renk
                    d.renk = f"Renk-{mevcut_renk}" # Görselleştirme için
                    boyanmamislar.remove(d)
                    gecici_boyananlar.append(d)
            
        return renk_haritasi