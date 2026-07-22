# İş İlanı Karar Destek Sistemi

Yapay zeka destekli bir karar destek sistemi olarak geliştirilen bu proje, aday CV'lerini iş ilanlarıyla anlamsal açıdan analiz ederek en uygun adayların belirlenmesini sağlar. Doğal Dil İşleme (NLP) tekniklerinden yararlanarak yalnızca anahtar kelime eşleşmelerine değil, metinlerin anlam bütünlüğüne de odaklanır ve işe alım süreçlerini daha verimli hale getirir.

## Özellikler

- İşverenlerin iş ilanı oluşturabilmesi ve yönetebilmesi
- Adayların CV ve başvurularını sisteme yükleyebilmesi
- CV ve iş ilanlarının anlamsal benzerlik analizi
- Her aday için otomatik uyumluluk skoru hesaplanması
- En yüksek eşleşmeye sahip adayların sıralanması
- İşe alım sürecini hızlandıran karar destek mekanizması

## Kullanılan Teknolojiler

- **Backend:** Python, Django
- **Frontend:** HTML, CSS
- **Doğal Dil İşleme (NLP):** Anlamsal metin benzerliği analizi
- **Veri İşleme:** Python tabanlı metin ön işleme ve skorlama algoritmaları

## Projenin Amacı

İşe alım süreçlerinde yüzlerce CV'nin manuel olarak incelenmesi zaman alıcı ve hataya açık olabilir. Bu proje, CV içeriklerini iş ilanlarının gereksinimleriyle anlamsal olarak karşılaştırarak adaylara uyumluluk puanı verir ve insan kaynakları uzmanlarının en uygun adayları daha hızlı belirlemesine yardımcı olur.

## Kurulum

```bash
git clone https://github.com/nazyi/Is_Ilan_KararDestekSistemi.git
cd Is_Ilan_KararDestekSistemi
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```
