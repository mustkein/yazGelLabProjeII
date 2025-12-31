# İstanbul Sosyal Ağ Analizi



**Proje Adı:** İstanbul Turistik Mekanların Sosyal Ağ Analizi ve Görselleştirme Sistemi

**Ekip Üyeleri:** 
- Ceyda Özmen - 221307058
- Yusuf Can Müştekin - 231307082


**Proje Tarihi:20 Kasım 2025**

**Kocaeli Üniversitesi, Bilişim Sistemleri Mühendisliği**

---

## 1. Giriş

### 1.1 Problemin Tanımı

Günümüz modern şehirlerinde turistik mekanlar arasındaki ilişkiler; ziyaretçi hareketleri, mekansal yakınlıklar ve popülerlik etkileşimleri doğrultusunda karmaşık ve çok boyutlu bir ağ yapısı oluşturmaktadır. Özellikle İstanbul gibi tarihsel, kültürel ve turistik açıdan yüksek öneme sahip metropollerde bu ilişkilerin analizi; sürdürülebilir turizm planlaması, ziyaretçi deneyiminin iyileştirilmesi ve kentsel karar destek sistemlerinin geliştirilmesi açısından kritik bir rol oynamaktadır.

Bu proje kapsamında, İstanbul’da yer alan en popüler 50 turistik mekan bir graf (graph) yapısı olarak modellenmiştir. Mekanlar, düğümler (nodes) şeklinde temsil edilirken aralarındaki ilişkiler coğrafi yakınlık, ziyaretçi etkileşim yoğunluğu ve popülerlik düzeyi gibi kriterler doğrultusunda tanımlanan ağırlıklı kenarlar (weighted edges) ile ifade edilmiştir. Böylece karmaşık turistik ilişkiler matematiksel ve algoritmik olarak analiz edilebilir bir yapıya dönüştürülmüştür.

### 1.2 Projenin Amacı

Bu çalışmanın temel amacı, İstanbul’un sembolik ve yoğun ilgi gören turistik lokasyonlarını matematiksel ve algoritmik yöntemler kullanarak analiz etmek ve kentsel turizm ağının yapısal özelliklerini ortaya koymaktır. Bu doğrultuda proje aşağıdaki hedefleri kapsamaktadır:

1. **Graf Teorisi Uygulaması:** Gerçek dünya turizm verilerinin graf teorisi prensipleri kullanılarak dijital bir graf veri yapısına dönüştürülmesi.
   
3. **Algoritma Analizi:** BFS, DFS, Dijkstra, A*, Floyd–Warshall gibi klasik graf algoritmalarının uygulanması ve performanslarının analiz edilmesi.
   
5. **Sosyal Ağ Analizi:** Merkezilik ölçütleri kullanılarak ağ içerisindeki en etkili ve popüler turistik mekanların tespit edilmesi.
   
7. **Topluluk Tespiti:** Bağlı bileşenler analizi yoluyla turistik mekanların oluşturduğu grupların ve ayrık alt yapıların belirlenmesi.
   
9. **Graf Renklendirme:** Welsh–Powell algoritması kullanılarak grafın optimal biçimde renklendirilmesi ve çakışmaların önlenmesi.
    
11. **Görselleştirme:** Oluşturulan ağ yapısının kullanıcı dostu, interaktif ve anlaşılır basit bir biçimde görselleştirilmesi.

   
### 1.3 Projenin Kapsamı

Proje kapsamında:
- Küçük ve orta ölçekli senaryoları temsil etmek amacıyla 20 ve 50 turistik mekan ayrı ayrı düğümler olarak modellenmiştir.
  
- Mekanlar arasındaki ilişkiler, yönsüz ve ağırlıklı kenarlar şeklinde tanımlanmıştır.
  
- Kenar ağırlıkları; mekanların aktiflik düzeyi, sosyal etkileşim yoğunluğu ve bağlantı sayısı gibi parametreler dikkate alınarak aşağıda verilen formül ile hesaplanmıştır.
  
 $$Agirlik_{i,j} = \frac{1}{1 + \sqrt{(Aktiflik_i - Aktiflik_j)^2 + (Etkilesim_i - Etkilesim_j)^2 + (Baglanti_i - Baglanti_j)^2}}$$
 
- Temel graf algoritmalarının tamamı sistem içerisinde gerçeklenmiş ve farklı senaryolar üzerinde test edilmiştir.
  
- Yazılım mimarisi, nesne yönelimli programlama prensipleri doğrultusunda modüler bir yapı olacak şekilde tasarlanmıştır.

---

## 2. Kullanılan Teknolojiler

- **Programlama Dili:** Python
- **Görselleştirme:** Tkinter
- **Veri Formatı:** CSV, JSON

---

## 3. Algoritmalar

### 3.1 Breadth-First Search (BFS) - Genişlik Öncelikli Arama


BFS algoritması, bir başlangıç düğümünden itibaren grafı katman katman gezerek en yakın komşulardan başlayacak şekilde tüm erişilebilir düğümleri keşfeder.Çekirdek yapısında FIFO (First-In-First-Out) mantığına dayalı bir kuyruk (queue) veri yapısı kullanır. Algoritma, ağırlıksız graflarda en kısa yol bulma problemi için optimal bir çözüm sunar.

Turistik mekanlar arasındaki erişilebilirlik analizinde ve başlangıç noktasından itibaren ağın katmanlı yapısının keşfedilmesinde ve en az adımda ulaşılabilecek mekanların tespitinde kullanılmıştır.

```mermaid

graph TD
  
    classDef startEnd fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px,color:#1b5e20;
    classDef process fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1;
    classDef decision fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#f57f17;

    A([Başlat]):::startEnd --> B[Kuyruğu ve Ziyaret<br/>Edilenleri Başlat]:::process
    B --> C{Kuyruk Boş mu?}:::decision
    
    C -- Evet --> D([Boş Liste Döndür]):::startEnd
    
    C -- Hayır --> E[Kuyruğun Başından<br/>Eleman Çıkar]:::process
    E --> F{Hedef Düğüm mü?}:::decision
    
    F -- Evet --> G[Ebeveyn Takibi ile<br/>Yolu Oluştur]:::process
    G --> H([Yolu Döndür]):::startEnd
    
    F -- Hayır --> I[Komşuları ID'ye Göre Sırala]:::process
    I --> J{Ziyaret Edilmemiş<br/>Komşu Var mı?}:::decision
    
    J -- Evet --> K[Ziyaret Edildi İşaretle,<br/>Ebeveyni Kaydet ve<br/>Kuyruğa Ekle]:::process
    K --> J
    
    J -- Hayır --> C

 
    linkStyle default stroke:#666,stroke-width:1px;

```


#### Karmaşıklık Analizi

- **Zaman Karmaşıklığı:** O(V + E)
  - V: Düğüm sayısı
  - E: Kenar sayısı
  - Her düğüm ve kenar bir kez işlenir.

- **Alan Karmaşıklığı:** O(V)
  - Kuyruk en kötü durumda tüm düğümleri içerebilir.
  - Ziyaret durumu dizisi V eleman içerir.


---

### 3.2 Depth-First Search (DFS) - Derinlik Öncelikli Arama


DFS algoritması, bir başlangıç düğümünden itibaren mümkün olduğunca derine inerek grafı gezmeye çalışır. Bir yolun sonuna geldiğinde geri döner ve diğer yolları keşfeder. Algoritma bir yığın (stack) yapısı kullanır veya özyinelemeli (recursive) olarak gerçeklenir.

Turistik ağ içerisindeki döngüsel yolların tespiti ve ağın topolojik yapısının derinlemesine incelenmesi için kullanılmıştır.


```mermaid
graph TD
   
    classDef startEnd fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px,color:#1b5e20;
    classDef process fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#01579b;
    classDef decision fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#f57f17;
    classDef error fill:#ffcdd2,stroke:#c62828,stroke-width:2px,color:#b71c1c;

    A([Başlat]):::startEnd --> B{Başlangıç ID<br/>Graf İçinde mi?}:::decision
    B -- Hayır --> C([Boş Liste Döndür]):::error
    B -- Evet --> D{Hedef ID<br/>Belirtilmiş mi?}:::decision

    %% Sol Kol: Gezinme
    D -- Hayır --> E[Stack'i Başlat ve<br/>Başlangıcı Ekle]:::process
    E --> F{Stack Boş mu?}:::decision
    F -- Evet --> G([Gezinme Sırasını Döndür]):::startEnd
    F -- Hayır --> H[Stack'ten Son Elemanı Çıkar]:::process
    H --> I{Daha Önce<br/>Ziyaret Edildi mi?}:::decision
    I -- Evet --> F
    I -- Hayır --> J[Ziyaret Edildi İşaretle ve<br/>Gezinme Listesine Ekle]:::process
    J --> K[Komşuları ID'ye göre<br/>Ters Sırada Al]:::process
    K --> L[Ziyaret Edilmeyen<br/>Komşuları Stack'e Ekle]:::process
    L --> F

    %% Sağ Kol: Arama
    D -- Evet --> M[Stack ve Parent<br/>Sözlüğünü Başlat]:::process
    M --> N{Stack Boş mu?}:::decision
    N -- Evet --> O([Boş Liste Döndür]):::error
    N -- Hayır --> P[Stack'ten Son Elemanı Çıkar]:::process
    P --> Q{Mevcut == Hedef?}:::decision
    Q -- Evet --> R[Parent Sözlüğü ile<br/>Yolu Geriye Doğru Oluştur]:::process
    R --> S([Yolu Döndür]):::startEnd
    Q -- Hayır --> T{Ziyaret Edildi mi?}:::decision
    T -- Evet --> N
    T -- Hayır --> U[Ziyaret Edildi İşaretle]:::process
    U --> V[Komşuları ID'ye göre<br/>Ters Sırada Al]:::process
    V --> W[Komşular için Parent<br/>Kaydet ve Stack'e Ekle]:::process
    W --> N

```

#### Karmaşıklık Analizi

- **Zaman Karmaşıklığı:** O(V + E)
  - Her düğüm ve kenar bir kez ziyaret edilir.

- **Alan Karmaşıklığı:** O(V)
  - Özyinelemeli çağrı yığını.

---

### 3.3 Dijkstra Algoritması - En Kısa Yol


Dijkstra algoritması, ağırlıklı graflarda bir başlangıç düğümünden diğer tüm düğümlere olan en kısa yolları bulur. Algoritma, açgözlü (greedy) yaklaşım kullanarak her adımda en düşük maliyetli düğümü seçer. Negatif ağırlıklı kenarlar içermeyen graflarda optimal sonuç verir.

Mekanlar arasındaki aktiflik, sosyal etkileşim ve bağlantı yoğunluğuna göre belirlenen Euclidean tabanlı ağırlık fonksiyonu kullanılarak en düşük maliyetli rotaların belirlenmesini sağlar.

```mermaid

graph TD
    classDef startEnd fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px,color:#1b5e20;
    classDef process fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#01579b;
    classDef decision fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#f57f17;
    classDef error fill:#ffcdd2,stroke:#c62828,stroke-width:2px,color:#b71c1c;

    A([Başlat]):::startEnd --> B{Başlangıç ID<br/>Graf içinde mi?}:::decision
    
    B -- Hayır --> C([Boş Yol ve 0 döndür]):::error
    
    B -- Evet --> D[Mesafe Tablosunu -dist- Sonsuz Yap<br/>Önceki Düğüm Tablosunu -prev- Hazırla<br/>Başlangıç Mesafesini 0 Ayarla]:::process
    
    D --> E[Öncelik Kuyruğuna -pq-<br/>Başlangıç Düğümünü Ekle]:::process
    
    E --> F{Kuyruk -pq-<br/>Boş mu?}:::decision
    
    F -- Hayır --> G[Kuyruktan En Küçük<br/>Mesafeli Düğümü -curr- Çıkar]:::process
    
    G --> H{curr_dist ><br/>dist -curr-?}:::decision
    
    H -- Evet --> F
    
    H -- Hayır --> I{curr == target_id?}:::decision
    
    I -- Evet --> J[Döngüden Çık]:::process
    
    I -- Hayır --> K[Düğümün Komşularını Tara]:::process
    
    K --> L{Yeni Mesafe <<br/>dist -komşu-?}:::decision
    
    L -- Evet --> M[Mesafe Tablosunu Güncelle<br/>Önceki Düğümü Kaydet<br/>Kuyruğa -pq- Yeni Mesafeyi Ekle]:::process
    
    M --> K
    
    L -- Hayır --> K
    
    K -- Tüm komşular bitti --> F
    
    F -- Evet --> N{Hedef Mesafesi<br/>Sonsuz mu?}:::decision
    
    J --> N
    
    N -- Evet --> C
    
    N -- Hayır --> O[prev Tablosunu Takip Ederek<br/>En Kısa Rotayı Listele]:::process
    
    O --> P([ROTAYI VE TOPLAM<br/>MESAFEYİ DÖNDÜR]):::startEnd

    linkStyle default stroke:#666,stroke-width:1px;


```


#### Karmaşıklık Analizi

- **Zaman Karmaşıklığı:** 
  -  O((V + E) log V)

- **Alan Karmaşıklığı:** O(V)
  - Mesafe dizisi ve öncelik kuyruğu


---

### 3.4 A* (A-Star) Algoritması - Heuristik En Kısa Yol


A* algoritması, Dijkstra algoritmasının geliştirilmiş versiyonudur. Dijkstra algoritmasına sezgisel (heuristic) bir maliyet fonksiyonu ekleyerek arama uzayını hedefe doğru daraltan bir optimizasyon algoritmasıdır. Hedef düğüme olan tahmini mesafeyi (heuristic) kullanarak arama sürecini hızlandırır. Algoritma, f(n) = g(n) + h(n) formülünü kullanır.

- g(n): Başlangıçtan n düğümüne gerçek maliyet
- h(n): n düğümünden hedefe tahmini maliyet (heuristik)
- f(n): Toplam tahmini maliyet

İstanbul haritası üzerinde coğrafi koordinatlar arası kuş uçuşu mesafeyi sezgisel veri olarak kullanarak, hedef odaklı ve yüksek performanslı rota planlaması yapar.


```mermaid
graph TD
    classDef startEnd fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px,color:#1b5e20;
    classDef process fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#01579b;
    classDef decision fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#f57f17;
    classDef error fill:#ffcdd2,stroke:#c62828,stroke-width:2px,color:#b71c1c;

    A([Başlat]):::startEnd --> B{Mekanlar Kayıtlı mı?}:::decision
    B -- Hayır --> C([İşlemi Durdur]):::error
    B -- Evet --> D[Mesafe Tablolarını Hazırla<br/>Heuristic Fonksiyonu Tanımla]:::process
    D --> E[Başlangıcı Ekle ve<br/>Tahmini Uzaklığı Hesapla]:::process
    E --> F{İşlenecek Mekan<br/>Kaldı mı?}:::decision
    F -- Hayır --> G([Yol Bulunamadı]):::error
    F -- Evet --> H[Hedefe En Yakın<br/>Mekanı Seç]:::process
    H --> I{Seçilen Mekan<br/>Hedef mi?}:::decision
    I -- Evet --> J[Yolu Geriye Doğru Çıkar]:::process
    J --> K([Sonucu Döndür]):::startEnd
    I -- Hayır --> L[Bağlı Mekanları İncele]:::process
    L --> M[Yeni G Skorunu Hesapla]:::process
    M --> N{Yeni Yol<br/>Daha mı Kısa?}:::decision
    N -- Evet --> O[Bilgileri Güncelle ve<br/>Kuyruğa Ekle]:::process
    O --> F
    N -- Hayır --> F
```

#### Karmaşıklık Analizi

- **Zaman Karmaşıklığı:** O(b^d)
  - b: Dallanma faktörü (branching factor)
  - d: Hedefin derinliği
  - En Kötü Durum: O(E)

- **Alan Karmaşıklığı:** O(b^d)
  - En Kötü Durum: O(V)


---

### 3.5 Floyd-Warshall Algoritması - Tüm Çiftler En Kısa Yol


Floyd-Warshall algoritması, tüm düğüm çiftleri arasındaki en kısa yolları bulur. Dinamik programlama yaklaşımı kullanarak her adımda ara düğümler üzerinden geçen yolları değerlendirir.  Negatif ağırlıklı kenarları destekler ancak negatif döngü içermemelidir. Ağların genel geçiş kapasitesini ölçmede ve küçük-orta ölçekli çizgelerde tüm çiftler arası analizler için kullanılmaktadır.

```mermaid
graph TD

    classDef startEnd fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px,color:#1b5e20;
    classDef process fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#01579b;
    classDef decision fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#f57f17;

    A([BAŞLAT]):::startEnd --> B[Tüm Mekanlar Arası Mesafe<br/>Tablosunu Hazırla<br/>Bilinen Yolları ve<br/>Mesafeleri Tabloya İşle]:::process
    B --> C[Henüz Bilinmeyen Tüm<br/>Yolları<br/>'Sonsuz Uzaklık' Olarak<br/>İşaretle]:::process
    C --> D[Sırayla Her Bir Mekanı<br/>'ARA DURAK' Olarak Seç]:::process
    
    D -- Tüm Mekanlar Ara Durak<br/>Oldu --> E{Belirli Bir Rota<br/>İsteniyor mu?}:::decision
    E -- Hayır --> F([İşlemi Sonlandır]):::startEnd
    E -- Evet --> G[Tablodaki Güncel Verileri<br/>Kullanarak<br/>Adım Adım En Kısa Rotayı<br/>Çıkar]:::process
    G --> H([EN KISA ROTAYI VE<br/>TOPLAM MESAFEYİ DÖNDÜR]):::startEnd

    D -- " " --> I[Sırayla Bir 'BAŞLANGIÇ'<br/>Mekanı Seç]:::process
    I -- Tüm Başlangıçlar Bitti --> D
    I -- " " --> J[Sırayla Bir 'HEDEF' Mekanı<br/>Seç]:::process
    J -- Tüm Hedefler Bitti --> I

    J -- " " --> K{Başlangıçtan Hedefe<br/>Giderken<br/>Seçilen 'ARA DURAK'tan<br/>Geçmek<br/>Yolu Kısaltıyor mu?}:::decision
    K -- Hayır --> J
    K -- Evet --> L[Tablodaki Eski Mesafeyi Sil<br/>Yeni ve Kısa Olan Mesafeyi<br/>Yaz]:::process
    L -- " " --> J

    linkStyle default stroke:#666,stroke-width:1px;

```

#### Karmaşıklık Analizi

- **Zaman Karmaşıklığı:** O(V³)
 
- **Alan Karmaşıklığı:** O(V²)
  - Mesafe matrisi V×V boyutundadır.


---

### 3.6 Degree Centrality - Derece Merkeziliği


Degree Centrality, bir düğümün ağdaki önemini komşu sayısına göre belirler. Basit ama etkili bir merkezilik ölçütüdür ve düğümün doğrudan etkileşim gücünü gösterir. ğdaki her bir düğümün doğrudan bağlantı sayısını hesaplayarak İstanbul turistik ağındaki "en popüler" ve "merkezi" lokasyonları tespit eder.

```mermaid

graph TD

    classDef baslangic fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef islem fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef karar fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;

    Start([BAŞLAT]):::baslangic --> Hazirlik[Analiz İçin Boş Bir Liste Oluştur]:::islem
    Hazirlik --> Dongu{İncelenmemiş<br/>Mekan Kaldı mı?}:::karar
    
    Dongu -- Evet --> Secim[Sıradaki Mekanı Seç]:::islem
    Secim --> Hesapla[Mekanın Kaç Tane Komşusu<br/>Olduğunu Say]:::islem
    
    Hesapla --> Kaydet[Mekan Adını ve Bağlantı Sayısını<br/>Listeye Not Et]:::islem
    Kaydet --> Dongu
    
    Dongu -- Hayır --> Sirala[Listeyi Bağlantı Sayısına Göre<br/>Büyükten Küçüğe Sırala]:::islem
    
    Sirala --> Sec[En Yüksek Puanlı<br/>İlk 5 Mekanı Ayır]:::islem
    Sec --> Bitis([EN POPÜLER 5 MEKANI DÖNDÜR]):::baslangic

```

#### Karmaşıklık Analizi

- **Zaman Karmaşıklığı:** O(V + E)
  
- **Alan Karmaşıklığı:** O(V)

---

# 4. MİMARİ VE İŞLEYİŞ ANALİZİ


Aşağıda, sistemin modüler yapısı ve çalışma zamanı davranışları, proje dokümantasyonundaki görsel diyagramların (Sınıf ve Akış Şemaları) renk kodlarına atıfta bulunularak detaylandırılmıştır.

---

## 1. Yazılım Mimarisi ve Sınıf Yapısı

Sistem dört ana modülden oluşmaktadır:

### A. Kullanıcı Arayüzü Katmanı (UI Layer)

Kullanıcının sistemle etkileşime girdiği ön yüz katmanıdır.
<img width="1920" height="1040" alt="image" src="https://github.com/user-attachments/assets/ede00e15-b6cc-4c8d-bcce-6883f2e0cebb" />


* **Sınıf:** `TuristRehberiUygulamasi`
* **Görevi:**
    * Uygulamanın grafiksel arayüzünü (`Tkinter`) yönetir.
    * Kullanıcıdan başlangıç (`Start Node`) ve hedef (`Target Node`) verilerini alır.
    * Harita çizimi (`Canvas`) ve sonuç listeleme (`Treeview`) işlemlerini yürütür.
* **İlişkisi:** Veri katmanı (`Graph`) ile doğrudan iletişim halindedir ve analiz butonuna basıldığında ilgili algoritmayı tetikler.

### B. Veri Yönetim Katmanı (Data & Manager Layer)

Projenin veri omurgasını oluşturur. Verinin bellekte tutulması, dosyadan okunması ve yönetilmesinden sorumludur.

* **Temel Sınıflar:**
    * `Node` (Düğüm): Haritadaki mekanı, koordinatları (`x,y`) ve sosyal skorları (`active_score`) temsil eder.
    * `Edge` (Kenar): İki mekan arasındaki bağlantıyı ve maliyeti (`weight`) temsil eder.
* **Yönetici Sınıf:** `Graph`
    * Tüm düğüm ve kenarları bir arada tutan ana kapsayıcıdır.
    * CSV dosyasından veri yükleme (`load_from_csv`).
    * JSON formatında kaydetme/yükleme.
    * Dinamik ağırlık hesaplama (`_calculate_weight`).

### C. Algoritma Katmanı (Logic Layer)

Projenin hesaplama mantığının bulunduğu merkezdir. **Strateji Tasarım Deseni (Strategy Pattern)** kullanılarak tasarlanmıştır.

* **Soyutlama (Mavi Alan):**
    * `Algorithm`: Tüm algoritmaların türediği soyut (abstract) sınıftır. Her algoritmanın `execute(graph, start, target)` metoduna sahip olmasını zorunlu kılar.
* **Somut Algoritmalar (Yeşil Alan):**
    * **Yol Bulma:** `BFS`, `DFS` (Gezinme), `Dijkstra`, `A*` (En Kısa Yol), `FloydWarshall`.
    * **Analiz:** `DegreeCentrality` (Popülerlik), `Coloring` (Graf Renklendirme), `ConnectedComponents` (Kopuk Parçalar).

```mermaid
classDiagram
    %% --- Sınıflar ---
    class Node:::graphextends {
        +int id
        +str name
        +int x
        +int y
        +float active_score
        +int social_score
        +int connection_count
    }

    class Edge:::graphextends {
        +Node source
        +Node target
        +float weight
    }
    class Graph:::graphbase {
        +dict nodes
        +dict adjacency_list
        +str data_dir
        +add_node(Node node)
        +add_edge(id1, id2)
        +load_from_csv(filename)
        +save_to_json_path(filepath)
        +get_neighbors(node_id)
        -_calculate_weight(n1, n2)
        +export_adjacency_matrix()
    }
    class Algorithm:::algbase {
        <<Abstract>>
        +execute(graph, start, target)
    }

    class BFS:::extends { +execute() }
    class DFS:::extends { +execute() }
    class Dijkstra:::extends { +execute() }
    class AStar:::extends { +execute() }
    class FloydWarshall:::extends { +execute() }
    class DegreeCentrality:::extends { +execute() }
    class Coloring:::extends { +execute() }
    class ConnectedComponents:::extends { +execute() }
    
    class TuristRehberiUygulamasi {
        +Tk root
        +Graph graph
        +create_ui_controls()
        +create_result_table()
        +load_scenario()
        +run_algorithm()
        +draw_map()
    }

    %% --- İlişkiler ---
    Graph "1" *-- "many" Node : Yönetir
    Graph "1" *-- "many" Edge : Yönetir
    Edge --> Node : Bağlar
    
    Algorithm <|-- BFS
    Algorithm <|-- DFS
    Algorithm <|-- Dijkstra
    Algorithm <|-- AStar
    Algorithm <|-- FloydWarshall
    Algorithm <|-- DegreeCentrality
    Algorithm <|-- Coloring
    Algorithm <|-- ConnectedComponents

    TuristRehberiUygulamasi --> Graph : Kullanır
    TuristRehberiUygulamasi ..> Algorithm : Çalıştırır

    classDef algbase fill:#add8e6,stroke:#1a237e,stroke-width:2px,color:#000;
    classDef extends fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px,color:#000;
    classDef graphbase fill:#ffd59a,stroke:#bf360c,stroke-width:2px,color:#000;    
    classDef graphextends fill:#ffeebb,stroke:#ab6600,stroke-width:2px,color:#000;
```

---

## 2. Sistem İşleyişi ve Algoritma Akış Analizi

Sistemenin çalışma zamanındaki davranışı üç ana fazdan oluşur.

### Faz 1: Başlatma
Program `main.py` üzerinden tetiklendiğinde sırasıyla şu işlemler gerçekleşir:
1.  **Arayüz Yüklemesi:** `TuristRehberiUygulamasi` sınıfı başlatılır.
2.  **Veri Entegrasyonu:** Sistem varsayılan olarak `mekanlar.csv` dosyasını okur. `Graph` sınıfı bu ham veriyi işleyerek bellekte nesnelere dönüştürür.
3.  **Görselleştirme:** Oluşturulan graf yapısı arayüze çizilir ve sistem "Kullanıcı Bekleniyor" durumuna geçer.

### Faz 2: Kullanıcı Etkileşimi
Kullanıcı arayüz üzerinden aşağıdaki işlemleri gerçekleştirebilir:

* **Algoritma Çalıştırma:**
    * Kullanıcı algoritmayı seçer ve noktaları belirler.
    * Sistem ilgili algoritma sınıfını dinamik olarak çağırır.
* **Veri Düzenleme (CRUD):**
    * Düğüm Ekleme/Silme ve Bağlantı kurma işlemleri `Graph` yöneticisi üzerinden yapılır ve harita anlık (`refresh`) güncellenir.
* **Dosya İşlemleri (I/O):**
    * Mevcut senaryo JSON olarak dışa aktarılabilir veya yeni bir dosya içeri aktarılabilir.

### Faz 3: Sonuçlandırma
Algoritma çalıştıktan sonra sonuçlar değerlendirilir:

* **Başarılı Sonuç:** Yol bulunduysa haritada **kırmızı çizgi** ile rota çizilir, adım adım detaylar tabloya yazılır.
* **Hata Durumu:** Hedefe ulaşılamıyorsa (graf kopuksa) veya geçersiz girdi varsa kullanıcıya görsel hata mesajı gösterilir.

```mermaid
graph TD
      
    %% UI- Arayüz ve Kullanıcı Etkileşimi
    classDef uiStyle fill:#FFF2CC,stroke:#D6B656,stroke-width:2px,color:#000;
    
    %% DATA  - Veri ve Graph Yönetimi
    classDef dataStyle fill:#F4B084,stroke:#B95000,stroke-width:2px,color:#000;
    
    %% LOGIC - Karar Mekanizmaları ve Girdiler
    classDef logicStyle fill:#DAE8FC,stroke:#6C8EBF,stroke-width:2px,color:#000;
    
    %% ALGO  - Algoritma İşleme
    classDef algoStyle fill:#D5E8D4,stroke:#82B366,stroke-width:2px,color:#000;

    %% ERROR
    classDef errorStyle fill:#F8CECC,stroke:#B85450,stroke-width:2px,color:#000;

    %% ---------------------------------------------------

    start([Başlat: main.py]):::uiStyle --> init_gui[Arayüzü Başlat: TuristRehberi]:::uiStyle
    
    init_gui --> load_csv[Varsayılan CSV'yi Yükle]:::dataStyle
    load_csv --> create_graph[Graph Yapısını Oluştur]:::dataStyle
    create_graph --> draw_ui[Haritayı ve Tabloyu Çiz]:::uiStyle
    
    draw_ui --> user_wait{Kullanıcı Bekleniyor}:::uiStyle
    
    %% --- DAL 1: ALGORİTMA İŞLEMLERİ (Yeşil & Mavi) ---
    user_wait -- Algoritma Seç --> get_inputs[Başlangıç/Bitiş ID Gir]:::logicStyle
    get_inputs --> run_algo[Algoritmayı Çalıştır]:::algoStyle
    run_algo --> check_result{Sonuç Var mı?}:::logicStyle
    
    check_result -- Evet --> draw_path[Haritada Yolu Göster]:::uiStyle
    draw_path --> update_table[Sonuç Tablosunu Doldur]:::uiStyle
    
    check_result -- Hayır --> show_error[Hata: Yol Bulunamadı]:::errorStyle
    
    %% --- DAL 2: VERİ YÖNETİMİ (Turuncu) ---
    user_wait -- Node Ekle / Sil / Bağla --> crud_ops[Graph Manager Güncelle]:::dataStyle
    crud_ops --> refresh_map[Haritayı Yeniden Çiz]:::uiStyle
    
    %% --- DAL 3: DOSYA İŞLEMLERİ (Turuncu) ---
    user_wait -- JSON Kaydet / Yükle --> file_io[Dosya İşlemleri]:::dataStyle
    file_io --> refresh_map

    %% Döngüler
    update_table --> user_wait
    show_error --> user_wait
    refresh_map --> user_wait
```
---



