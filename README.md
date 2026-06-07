# L Braket Yapay Zekâ Tahmin Aracı

## Nihai veri kontrolü

Bu paket, kullanıcının yüklediği ham SolidWorks CSV dosyaları baştan
okunarak hazırlanmıştır.

- Ham kayıt sayısı: 454
- Benzersiz geometri sayısı: 339
- Tekrarlanan kayıt sayısı: 115
- Stress modeli: Kernel Ridge Regression
- Displacement modeli: KNN Regression
- Displacement birimi CSV içinde doğrudan mm'dir.

Aynı geometriye ait çakışmalarda hedefli yeniden analiz dosyaları
(`l_braket_4.csv` ve `l_braket_5.csv`) öncelikli kullanılmıştır.

Kontrol örneği:

- L1 = 80 mm
- L2 = 60 mm
- t = 8 mm
- d = 18 mm
- Stress = 5.9488 MPa
- Displacement = 0.01222 mm
- Kaynak = l_braket_4.csv

`l_braket_5.csv` dosyasında delik çapı satırı yer almadığı için bu
dosyadaki senaryolarda d = 15 mm kabul edilmiştir.

Bağımsız doğrulama için gönderilen ekran görüntülerindeki tasarımlar,
modelin test edilmesi amacıyla eğitim veri setine eklenmemiştir.
