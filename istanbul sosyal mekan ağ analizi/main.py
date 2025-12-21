import os
import tkinter as tk
from src.graph_manager import IstanbulGraf
from src.ui import IstanbulUI
from src.algorithms import AnalizMotoru

def main():
    # 1. Tkinter ana penceresini oluştur (Görselleştirme için şart)
    root = tk.Tk()
    
    # 2. Graf nesnesini oluştur
    istanbul = IstanbulGraf()
    
    # 3. Veriyi yükle
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "data", "mekanlar.csv")
    istanbul.csv_den_yukle(csv_path)

    # 4. Görselleştirme sınıfını (UI) başlat
    # Bu adım, canvas üzerine çizim işlemini tetikler 
    app = IstanbulUI(root, istanbul)
    
    # 5. Pencereyi açık tut (Mainloop olmadan pencere anında kapanır)
    root.mainloop()

if __name__ == "__main__":
    main()