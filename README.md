# L Braket AI Tasarım Aracı

Bu paket, SolidWorks sonlu elemanlar analizi verileriyle eğitilen
Random Forest tabanlı stress ve displacement tahmin uygulamasını içerir.

## Veri seti özeti

- Önceki benzersiz tasarım sayısı: 179
- Yeni SolidWorks senaryo sayısı: 256
- Tekrarlanan geometri sayısı: 96
- Nihai benzersiz tasarım sayısı: 339

Aynı geometriye ait tekrar eden kayıtlarda yeni SolidWorks sonuçları esas alınmıştır.

## Kullanım

1. Bu klasördeki dosyaları GitHub deposuna yükleyin.
2. Streamlit uygulamasında Reboot app yapın.
3. Uygulama açıldığında Random Forest modeli güncel veri setiyle otomatik eğitilir.
