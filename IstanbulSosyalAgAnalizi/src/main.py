import tkinter as tk
import sys
import os
import time

try:
    from gui_app import TuristRehberiUygulamasi
    from test_manager import AdvancedPerformanceTester
except ImportError as e:
    print(f"[HATA] Modül aktarılamadı: {e}")
    print("Lütfen gui_app.py, test_manager.py ve diğer bağımlılıkların aynı dizinde olduğunu kontrol edin.")
    sys.exit(1)

def run_performance_suite():
    """Performans testlerini başlatır ve raporu hazırlar."""
    print("\n" + "="*60)
    print("      İSTANBUL SOSYAL AĞ ANALİZİ - PERFORMANS TEST SİSTEMİ")
    print("="*60)
    
    try:
        tester = AdvancedPerformanceTester()
        tester.run_tests()
        print("\n[BAŞARILI] Performans testleri tamamlandı ve rapor kaydedildi.")
    except Exception as e:
        print(f"\n[HATA] Testler çalıştırılırken bir sorun oluştu: {e}")
    
    print("="*60 + "\n")

def start_gui():
    """Ana GUI uygulamasını başlatır."""
    print("[SİSTEM] Görsel Arayüz (GUI) Hazırlanıyor...")
    
    try:
        root = tk.Tk()
        
        # GUI Sınıfını örneklendirme
        app = TuristRehberiUygulamasi(root)
        
        # Pencere kapatıldığında uygulamayı sonlandır.
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        
        print("[SİSTEM] Uygulama Başlatıldı.")
        root.mainloop()
        
    except Exception as e:
        print(f"[KRİTİK HATA] Arayüz başlatılamadı: {e}")
        sys.exit(1)

def main():
    """Ana program akışı."""
    # 1. Aşama: Performans Testleri
    # algoritmaların hız ve doğruluk testleri
    run_performance_suite()
    
    # 2. Aşama: Uygulama Arayüzü
    # Testler bittikten sonra GUI aç
    start_gui()

if __name__ == "__main__":
    main()
