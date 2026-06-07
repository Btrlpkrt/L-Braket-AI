# L Braket AI Tasarım Aracı

Bu proje, 100 N sabit yük altında L braket geometrik parametrelerinden stress ve displacement tahmini yapan Streamlit uygulamasıdır.

## GitHub ve Streamlit Cloud

Bu klasördeki tüm dosyaları GitHub reposuna yükleyin. Streamlit Community Cloud üzerinde ana dosya olarak `app.py` seçin.


## Birimler
- Stress: MPa (N/mm²)
- Displacement: mm


Not: Displacement verileri SolidWorks doğrulamasına göre 1/100 ölçeğine dönüştürülmektedir.


## Güncel veri seti
Eski 81 senaryo ile yeni 81 senaryo birleştirilmiştir. Bir ortak geometri yeni SolidWorks sonucu ile güncellendiği için toplam 161 benzersiz tasarım bulunmaktadır.


Model, ara değerlerde daha sürekli tahmin için 3. derece Polinom Regresyon olarak güncellenmiştir.


## Kullanılan model
Stress ve displacement tahmini için 800 ağaçlı Random Forest regresyon modeli kullanılmaktadır.
