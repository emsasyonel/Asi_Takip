import heapq
from datetime import datetime, timedelta

# Çocuk sınıfı
class Cocuk:
    def __init__(self, ad, soyad, dogum_tarihi):
        # Çocuk bilgilerini saklar: ad, soyad ve doğum tarihi
        self.ad = ad
        self.soyad = soyad
        self.dogum_tarihi = datetime.strptime(dogum_tarihi, '%Y-%m-%d')
        self.asilar = []  # Çocuğun aşı bilgilerini tutar [(Aşı Adı, Tarih, Durum)]

    def asi_ekle(self, asi_adi, tarih, durum="Bekliyor"):
        # Aşıyı listeye ekler
        self.asilar.append((asi_adi, tarih, durum))

    def asi_listesi(self):
        # Tüm aşıları döndürür
        return self.asilar

    def asi_tamamla(self, asi_adi):
        # Belirtilen aşıyı "Tamamlandı" olarak işaretler
        for i, asi in enumerate(self.asilar):
            if asi[0] == asi_adi and asi[2] == "Bekliyor":
                self.asilar[i] = (asi[0], asi[1], "Tamamlandı")
                return True
        return False

# Aşı takvimi oluşturma (özyineleme)
def asi_takvimi_olustur(dogum_tarihi, asilar, index=0):
    # Verilen aşı ve süre bilgisine göre bir takvim oluşturur
    if index >= len(asilar):
        return []
    return [(asilar[index][0], dogum_tarihi + timedelta(days=asilar[index][1]))] + asi_takvimi_olustur(
        dogum_tarihi, asilar, index + 1
    )

# Ağaç veri yapısı
class CocukAgaci:
    def __init__(self, veri):
        # Ağaç düğümünde bir çocuk nesnesi saklar
        self.veri = veri
        self.sol = None
        self.sag = None

    def ekle(self, yeni_cocuk):
        # Çocuk isimlerine göre ağaca ekleme yapar
        if yeni_cocuk.ad < self.veri.ad:
            if self.sol is None:
                self.sol = CocukAgaci(yeni_cocuk)
            else:
                self.sol.ekle(yeni_cocuk)
        else:
            if self.sag is None:
                self.sag = CocukAgaci(yeni_cocuk)
            else:
                self.sag.ekle(yeni_cocuk)

# Öncelikli kuyruk ve heap
class AsiHatirlatma:
    def __init__(self):
        # Hatırlatmalar için öncelikli kuyruk
        self.oncelik_kuyrugu = []

    def hatirlatma_ekle(self, tarih, asi_adi):
        # Yeni bir hatırlatma ekler
        heapq.heappush(self.oncelik_kuyrugu, (tarih, asi_adi))

    def siradaki_hatirlatma(self):
        # Tarihi geçen hatırlatmaları atlayarak sıradaki hatırlatmayı döndürür
        while self.oncelik_kuyrugu:
            tarih, asi_adi = heapq.heappop(self.oncelik_kuyrugu)
            if tarih >= datetime.now():
                return tarih, asi_adi
        return None

# Hash tablo (hızlı erişim için)
class CocukHashTablosu:
    def __init__(self):
        # Çocuk bilgilerini ID ile saklayan bir hash tablosu
        self.tablo = {}

    def ekle(self, id, cocuk):
        # Yeni bir çocuk ekler
        self.tablo[id] = cocuk

    def cocuk_bul(self, id):
        # ID'ye göre çocuk arar
        return self.tablo.get(id, None)

# Ana program
def main():
    # Çocuk ve hatırlatma yönetimi için yapıların oluşturulması
    cocuklar = CocukHashTablosu()
    hatirlatma = AsiHatirlatma()

    print("Aşı Takip Uygulamasına Hoşgeldiniz!")

    while True:
        # Kullanıcıya seçeneklerin sunulması
        print("\n1. Çocuk Ekle")
        print("2. Çocukların Aşı Takvimini Görüntüle")
        print("3. Aşı Hatırlatmalarını Gör")
        print("4. Bekleyen Aşıyı Tamamla")
        print("5. Çıkış")
        secim = input("Seçiminizi yapınız: ")

        if secim == "1":
            # Yeni çocuk ekleme işlemi
            ad = input("Çocuğun adı: ")
            soyad = input("Çocuğun soyadı: ")
            dogum_tarihi = input("Doğum tarihi (YYYY-MM-DD): ")
            cocuk = Cocuk(ad, soyad, dogum_tarihi)

            asilar = [("Hepatit B", 0), ("BCG", 60), ("DBT", 120), ("Kızamık", 180)]
            asi_takvimi = asi_takvimi_olustur(cocuk.dogum_tarihi, asilar)

            for asi_adi, tarih in asi_takvimi:
                cocuk.asi_ekle(asi_adi, tarih.strftime('%Y-%m-%d'))
                hatirlatma.hatirlatma_ekle(tarih, asi_adi)

            id = input("Çocuk için bir ID belirleyin: ")
            cocuklar.ekle(id, cocuk)
            print(f"{ad} {soyad} başarıyla eklendi!")

        elif secim == "2":
            # Belirli bir çocuğun aşı takvimini görüntüleme
            id = input("Çocuğun ID'sini giriniz: ")
            cocuk = cocuklar.cocuk_bul(id)
            if cocuk:
                print(f"\n{cocuk.ad} {cocuk.soyad} - Aşı Takvimi:")
                for asi in cocuk.asi_listesi():
                    print(f"- {asi[0]}: {asi[1]} ({asi[2]})")
            else:
                print("Bu ID'ye ait bir çocuk bulunamadı.")

        elif secim == "3":
            # Sıradaki hatırlatmayı görüntüleme
            hatirlatma_veri = hatirlatma.siradaki_hatirlatma()
            if hatirlatma_veri:
                print(f"\nYaklaşan aşı: {hatirlatma_veri[1]} - Tarih: {hatirlatma_veri[0].strftime('%Y-%m-%d')}")
            else:
                print("Hatırlatma bulunmuyor.")

        elif secim == "4":
            # Belirli bir çocuğun bekleyen aşılarını tamamlama
            id = input("Çocuğun ID'sini giriniz: ")
            cocuk = cocuklar.cocuk_bul(id)
            if cocuk:
                print(f"\n{cocuk.ad} {cocuk.soyad} - Bekleyen Aşılar:")
                bekleyen_asilar = [asi for asi in cocuk.asi_listesi() if asi[2] == "Bekliyor"]
                if not bekleyen_asilar:
                    print("Bekleyen aşı bulunmuyor.")
                else:
                    for i, asi in enumerate(bekleyen_asilar):
                        print(f"{i + 1}. {asi[0]} - Tarih: {asi[1]}")

                    secim = int(input("Tamamlamak istediğiniz aşının numarasını giriniz: "))
                    if 1 <= secim <= len(bekleyen_asilar):
                        asi_adi = bekleyen_asilar[secim - 1][0]
                        if cocuk.asi_tamamla(asi_adi):
                            print(f"{asi_adi} başarıyla tamamlandı!")
                            # Kuyrukta tamamlanan aşının çıkarılması
                            hatirlatma.oncelik_kuyrugu = [
                                (tarih, asi) for tarih, asi in hatirlatma.oncelik_kuyrugu if asi != asi_adi
                            ]
                            heapq.heapify(hatirlatma.oncelik_kuyrugu)
                        else:
                            print("Aşı tamamlanamadı.")
                    else:
                        print("Geçersiz seçim.")
            else:
                print("Bu ID'ye ait bir çocuk bulunamadı.")

        elif secim == "5":
            # Programdan çıkış
            print("Çıkış yapılıyor. Hoşçakalın!")
            break

        else:
            print("Geçersiz seçim. Tekrar deneyiniz.")


if __name__ == "__main__":
    main()
