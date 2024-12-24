import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import heapq


# Çocuk sınıfı
class Cocuk:
    def __init__(self, ad, soyad, dogum_tarihi):
        self.ad = ad
        self.soyad = soyad
        self.dogum_tarihi = dogum_tarihi
        self.asilar = []

    def asi_ekle(self, asi_adi, tarih):
        self.asilar.append((asi_adi, tarih, "Bekleniyor"))

    def asi_listesi(self):
        return self.asilar

    def asi_tamamla(self, asi_adi):
        for i, (adi, tarih, durum) in enumerate(self.asilar):
            if adi == asi_adi and durum == "Bekleniyor":
                self.asilar[i] = (adi, tarih, "Tamamlandı")
                return True
        return False


# Çocuk Hash Tablosu sınıfı
class CocukHashTablosu:
    def __init__(self):
        self.tablo = {}

    def ekle(self, id, cocuk):
        self.tablo[id] = cocuk

    def cocuk_bul(self, id):
        return self.tablo.get(id)


# Aşı Hatırlatma sınıfı
class AsiHatirlatma:
    def __init__(self):
        self.oncelik_kuyrugu = []

    def hatirlatma_ekle(self, tarih, asi_adi):
        heapq.heappush(self.oncelik_kuyrugu, (tarih, asi_adi))


# Aşı Takvimi Oluşturma
def asi_takvimi_olustur(dogum_tarihi, asilar):
    takvim = []
    dogum_tarihi_dt = datetime.strptime(dogum_tarihi, '%Y-%m-%d')
    for asi, gun_sayisi in asilar:
        asi_tarihi = dogum_tarihi_dt + timedelta(days=gun_sayisi)
        takvim.append((asi, asi_tarihi))
    return takvim


# Tkinter GUI
class AsiTakipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aşı Takip Uygulaması")

        self.cocuklar = CocukHashTablosu()
        self.hatirlatma = AsiHatirlatma()

        # Ana sekmeler
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Sekmeler
        self.cocuk_ekle_tab = ttk.Frame(self.notebook)
        self.asi_takvimi_tab = ttk.Frame(self.notebook)
        self.hatirlatma_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.cocuk_ekle_tab, text="Çocuk Ekle")
        self.notebook.add(self.asi_takvimi_tab, text="Aşı Takvimi")
        self.notebook.add(self.hatirlatma_tab, text="Hatırlatmalar")

        # Çocuk ekleme sekmesi
        self.setup_cocuk_ekle_tab()
        # Aşı takvimi sekmesi
        self.setup_asi_takvimi_tab()
        # Hatırlatma sekmesi
        self.setup_hatirlatma_tab()

    def setup_cocuk_ekle_tab(self):
        # Giriş alanları
        ttk.Label(self.cocuk_ekle_tab, text="Ad:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ad_entry = ttk.Entry(self.cocuk_ekle_tab)
        self.ad_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.cocuk_ekle_tab, text="Soyad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.soyad_entry = ttk.Entry(self.cocuk_ekle_tab)
        self.soyad_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.cocuk_ekle_tab, text="Doğum Tarihi (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5,
                                                                               sticky="w")
        self.dogum_tarihi_entry = ttk.Entry(self.cocuk_ekle_tab)
        self.dogum_tarihi_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.cocuk_ekle_tab, text="ID:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.id_entry = ttk.Entry(self.cocuk_ekle_tab)
        self.id_entry.grid(row=3, column=1, padx=5, pady=5)

        # Ekleme butonu
        self.ekle_button = ttk.Button(self.cocuk_ekle_tab, text="Ekle", command=self.cocuk_ekle)
        self.ekle_button.grid(row=4, column=0, columnspan=2, pady=10)

    def setup_asi_takvimi_tab(self):
        # ID giriş alanı
        ttk.Label(self.asi_takvimi_tab, text="Çocuk ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.takvim_id_entry = ttk.Entry(self.asi_takvimi_tab)
        self.takvim_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Görüntüleme butonu
        self.takvim_goster_button = ttk.Button(self.asi_takvimi_tab, text="Göster", command=self.asi_takvimi_goster)
        self.takvim_goster_button.grid(row=0, column=2, padx=5, pady=5)

        # Sonuçlar için liste
        self.asi_takvimi_list = ttk.Treeview(self.asi_takvimi_tab, columns=("Aşı Adı", "Tarih", "Durum"),
                                             show="headings")
        self.asi_takvimi_list.heading("Aşı Adı", text="Aşı Adı")
        self.asi_takvimi_list.heading("Tarih", text="Tarih")
        self.asi_takvimi_list.heading("Durum", text="Durum")
        self.asi_takvimi_list.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

        # Aşıyı Tamamla butonu
        self.asi_tamamla_button = ttk.Button(self.asi_takvimi_tab, text="Aşıyı Tamamla", command=self.asi_tamamla)
        self.asi_tamamla_button.grid(row=2, column=0, columnspan=3, pady=10)

    def setup_hatirlatma_tab(self):
        # Hatırlatmaları listeleme
        self.hatirlatma_button = ttk.Button(self.hatirlatma_tab, text="Hatırlatmaları Göster",
                                            command=self.hatirlatmalari_goster)
        self.hatirlatma_button.pack(pady=10)

        self.hatirlatma_list = ttk.Treeview(self.hatirlatma_tab, columns=("Tarih", "Aşı Adı"), show="headings")
        self.hatirlatma_list.heading("Tarih", text="Tarih")
        self.hatirlatma_list.heading("Aşı Adı", text="Aşı Adı")
        self.hatirlatma_list.pack(fill="both", expand=True)

    def cocuk_ekle(self):
        ad = self.ad_entry.get()
        soyad = self.soyad_entry.get()
        dogum_tarihi = self.dogum_tarihi_entry.get()
        id = self.id_entry.get()

        try:
            # Doğum tarihi doğrulaması
            datetime.strptime(dogum_tarihi, '%Y-%m-%d')
            cocuk = Cocuk(ad, soyad, dogum_tarihi)
            asilar = [
                ("Hepatit B", 0),
                ("BCG", 60),
                ("DBT", 120),
                ("Kızamık", 180)
            ]
            asi_takvimi = asi_takvimi_olustur(cocuk.dogum_tarihi, asilar)

            for asi_adi, tarih in asi_takvimi:
                cocuk.asi_ekle(asi_adi, tarih.strftime('%Y-%m-%d'))
                self.hatirlatma.hatirlatma_ekle(tarih, asi_adi)

            self.cocuklar.ekle(id, cocuk)
            messagebox.showinfo("Başarılı", f"{ad} {soyad} başarıyla eklendi!")
        except ValueError:
            messagebox.showerror("Hata", "Doğum tarihi formatı geçersiz. Lütfen YYYY-MM-DD formatında giriniz.")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def asi_takvimi_goster(self):
        self.asi_takvimi_list.delete(*self.asi_takvimi_list.get_children())
        id = self.takvim_id_entry.get()
        cocuk = self.cocuklar.cocuk_bul(id)

        if cocuk:
            for asi in cocuk.asi_listesi():
                self.asi_takvimi_list.insert("", "end", values=(asi[0], asi[1], asi[2]))
        else:
            messagebox.showerror("Hata", "Bu ID'ye ait bir çocuk bulunamadı.")

    def asi_tamamla(self):
        selected_item = self.asi_takvimi_list.selection()
        if selected_item:
            values = self.asi_takvimi_list.item(selected_item, "values")
            id = self.takvim_id_entry.get()
            cocuk = self.cocuklar.cocuk_bul(id)

            if cocuk and cocuk.asi_tamamla(values[0]):
                messagebox.showinfo("Başarılı", f"{values[0]} aşısı tamamlandı.")
                self.asi_takvimi_goster()
            else:
                messagebox.showerror("Hata", "Aşı tamamlanamadı veya zaten tamamlandı.")
        else:
            messagebox.showerror("Hata", "Lütfen bir aşı seçin.")

    def hatirlatmalari_goster(self):
        self.hatirlatma_list.delete(*self.hatirlatma_list.get_children())

        # Kuyruğun geçici bir kopyası üzerinde işlem yap
        gecici_kuyruk = list(self.hatirlatma.oncelik_kuyrugu)
        heapq.heapify(gecici_kuyruk)

        while gecici_kuyruk:
            tarih, asi_adi = heapq.heappop(gecici_kuyruk)
            if tarih >= datetime.now():
                self.hatirlatma_list.insert("", "end", values=(tarih.strftime('%Y-%m-%d'), asi_adi))


# Ana program
if __name__ == "__main__":
    root = tk.Tk()
    app = AsiTakipGUI(root)
    root.mainloop()
