class NoktaBulucu:
    def __init__(self):
        ### BEOTNARME 3. ÖRNEKTEKİ KESİT İÇİN ABAK FONKSİYONU.
        # birimler N, mm
        self.PasPayi = 40
        self.b = 300  # mm
        self.h = 500  # mm
        self.As1 = 763
        self.As2 = 402
        self.As3 = 763
        self.donati_adresi = {(self.As1, self.As3): self.PasPayi, self.As2: (self.h / 2),
                              self.As1: (self.h - self.PasPayi)}
        # donatı yukarıdan itibaren ne kadarlık mesafede.
        # aynı değere sahip ifadelerde python sadeleşirme yapıyor.
        # yani As1 değerine ulaşmaya çalışında As3 değerini veriyor.
        # bunun önüne üstteki kullanımla geçiyorsun. ??

        self.Beton = "C30"
        self.fyd = 365.22
        self.fcd = 20  # beton tipine bağımlı

        self.Es = 2 * (10 ** 5)
        self.k1 = 0.82  # (abaklardan okunur: beton tipine göre seçilir. if koyarsın c30 için 0,85miş)
        self.epsilonC = 0.003  # betonun yer değiştirme miktarı

        # eksenel basınç durumu 0,85 * fcd * Ac + As_toplam * fyd

        # eksenel çekme durumu -(As1 + As2 + As3) * fyd

        # dengeli durum εsy = fyd / Es

        # çeşitli c değerlerine göre hesaplar.
        """
            c değerleri belirlenir ( c nin h den büyük olma durumu )
            FORMÜLLER
            a = k1 * c ( beton basınç bölge yüksekliği )
            a değeri hesaplanır.
            ilgili donatıların akıp akmadıklarını kontrol et.
                εsy den büyükse akar, küçükse akmaz (hesaplanır)
                küçükse, üzerine gelen yük hesaplanır.
                εsy dengei durumda hesaplanır.
            sigmaS değeri hesaplanır.
            akma durumunda sigmaS 350 kabul edilmiş.
            sigmaS = ε * Es
            Fc hesaplanır (betonun basınç değeri)
                0,85 * fcd * Ac ( b * a )
            Nr hesaplanır
                Nr = Fs3 + Fs2 + Fs1 + Fc negatif ya da pozitif olabilir.
            Mr hesaplanır.
                Mr = Fc * ((h/2) - (a/2)) + Fs1 * ((h/2) - pas_payı) + Fs2 * ((h/2) - pas_payı) + Fs3 * ((h/2) - pas_payı)
                sanırım kesit ortasına göre moment alıyor.
            ilgili c değeri için Nr ve Mr değerleri hespalanmış olur.
        """

    def Eksenel_basinc_durumu(self):
        Ac = self.h * self.b  # beton basınç bölge alanı
        Nr = ((0.85 * self.fcd * Ac) + ((self.As1 + self.As2 + self.As3) * self.fyd)) / 1000
        return round(Nr, 2), round(0, 2)

    def Eksenel_cekme_durumu(self):
        Nr = (-(self.As1 + self.As2 + self.As3) * self.fyd) / 1000
        return round(Nr, 2), round(0, 2)

    def Nr_Mr_bulucu(self, c):
        a = self.k1 * c  # beton basınç bölge yüksekliği

        epsilonS3 = ((c - self.donati_adresi[self.As3, self.As1]) / c) * self.epsilonC
        epsilonS2 = ((c - self.donati_adresi[self.As2]) / c) * self.epsilonC
        epsilonS1 = ((c - self.donati_adresi[self.As1]) / c) * self.epsilonC

        # akıp akmama durumlarına göre hesap yapacak.

        epsilonSY = self.fyd / self.Es  # dengeli duruma göre hesaplanır
        sigmaSY = epsilonSY * self.Es  # akmış olan donatının taşıyabileceği yük

        # 3. DONATI SİGMA DEĞERİNİ HESAPLAR
        if (abs(epsilonS3) > epsilonSY):
            # donatı akmıştır
            sigmaS3 = sigmaSY if epsilonS3 > 0 else -sigmaSY
            # epsilınS3 pozitifse sigmaSY ata, eğer negatifse çekmeye çalışıyordur - ile çarp işaret değiş.
        else:
            sigmaS3 = (epsilonS3 * self.Es)
            # donatının üzerindeki yük

        # 2. DONATI SİGMA DEĞERİNİ HESAPLAR
        if (abs(epsilonS2) > epsilonSY):
            # donatı akmıştır
            sigmaS2 = sigmaSY if epsilonS2 > 0 else -sigmaSY
        else:
            sigmaS2 = (epsilonS2 * self.Es)
            # donatının üzerindeki yük

        # 1. DONATI SİGMA DEĞERİNİ HESAPLAR
        if (abs(epsilonS1) > epsilonSY):
            # donatı akmıştır
            sigmaS1 = sigmaSY if epsilonS1 > 0 else -sigmaSY
        else:
            sigmaS1 = (epsilonS1 * self.Es)
            # donatının üzerindeki yük

        # donatılar üzerindeki kuvveti bulalım
        Fs3 = (sigmaS3 * self.As3) / 1000  # kN
        Fs2 = (sigmaS2 * self.As2) / 1000  # kN
        Fs1 = (sigmaS1 * self.As1) / 1000  # kN

        # beton basınç bölgesi taşımasını hesapla
        Fc = 0.85 * self.fcd * self.b * a  # 0,85 * fcd * Ac ( b * a ) #N
        Fc = Fc / 1000  # kN

        Nr = Fs3 + Fs2 + Fs1 + Fc  # kolona gelen toplam basınç. kN

        # Mr = Fc * ((h/2) - (a/2)) + Fs1 * ((h/2) - pas_payı) + Fs2 * ((h/2) - pas_payı) + Fs3 * ((h/2) - pas_payı)
        # kesitin ortasına göre moment alırsın. Kn.m
        # bu yüzden ortadaki donatı sıfır etki eder.
        Mr = (Fc * (((self.h / 2) - (a / 2)) / 1000)) + (Fs2 * 0) + (
                (Fs3 - Fs1) * (((self.h - (2 * self.PasPayi)) / 2) / 1000))

        # print("normal kuvvet\t:", Nr, "\nmoment kuvvet\t:", Mr)
        return round(Nr, 2), round(Mr, 2)

if __name__ == "__main__":
    print("nokta bulucu içeriden çalıştırıldı.")
    ana_sinif = NoktaBulucu()
    print(ana_sinif.Nr_Mr_bulucu(650))
    # belli bir değerden sonra niçin momenti 0a çok yakın pozitif bir değer olarak vermiyor ??