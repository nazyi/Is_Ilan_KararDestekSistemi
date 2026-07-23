<div align="center">
# 💼 İş İlanı Karar Destek Sistemi
 
**CV'leri iş ilanlarıyla anlamsal olarak eşleştiren, AHP tabanlı ağırlıklandırma ile uyumluluk skoru üreten NLP destekli karar destek sistemi**

</div>
---

## Proje Hakkında
 
**İş İlanı Karar Destek Sistemi**, aday CV'lerini iş ilanlarıyla anlamsal açıdan analiz ederek en uygun adayların belirlenmesini sağlayan, yapay zekâ destekli bir karar destek sistemidir. Doğal Dil İşleme (NLP) teknikleri sayesinde yalnızca anahtar kelime eşleşmelerine değil, metinlerin anlam bütünlüğüne de odaklanarak işe alım süreçlerini daha verimli hale getirmeyi amaçlar.
 
Sistem; şirketlerin ilan açabildiği, adayların CV yükleyip başvuru yapabildiği bir Django web uygulaması ile bu uygulamanın arkasında çalışan bir **NLP + çok kriterli karar verme (AHP)** boru hattından oluşur.

## Projenin Amacı

İşe alım süreçlerinde yüzlerce CV'nin manuel olarak incelenmesi zaman alıcı ve hataya açık olabilir. Bu proje, CV içeriklerini iş ilanlarının gereksinimleriyle anlamsal olarak karşılaştırarak adaylara uyumluluk puanı verir ve insan kaynakları uzmanlarının en uygun adayları daha hızlı belirlemesine yardımcı olur.

## Özellikler
 
- 🏢 İşverenlerin şirket sayfası üzerinden iş ilanı oluşturması, düzenlemesi
- 🧑‍💼 Adayların üye olup CV bilgilerini ve başvurularını sisteme girmesi
- 🧠 CV ve ilan metinlerinin spaCy + NLTK ile Türkçe doğal dil işlemeden geçirilmesi (anlamlı kelime çıkarımı, stopword temizliği)
- 🔗 İlan–CV alanlarının (yetenek, dil, konum, eğitim, deneyim) karşılıklı eşleştirilmesi
- ⚖️ **AHP (Analitik Hiyerarşi Süreci)** ile kriter ağırlıklarının belirlenmesi
- 📊 Her aday için ağırlıklı uyumluluk skoru hesaplanması ve sıralanması
- 👥 Şirketler için önerilen adaylar, adaylar için önerilen ilanlar

## Kullanılan Teknolojiler
 
| Katman | Teknoloji |
|---|---|
| Backend | Python, Django |
| Doğal Dil İşleme | spaCy (`tr_core_news_sm`), NLTK (Türkçe stopwords), scikit-learn |
| Veri İşleme | Pandas, NumPy |
| Çok Kriterli Karar Verme | AHP (Analytic Hierarchy Process) |
| Veri Depolama | CSV tabanlı veri dosyaları |
| Arayüz | HTML, CSS |

> ⚠️ Depodaki `.csv` dosyalarında (`basvurular.csv`, `cv_bilgileri.csv`, `company_name.csv`, `personel-bilgi.csv` vb.) yer alan aday, şirket ve ilan bilgileri **gerçek değildir**. Bu veriler yalnızca sistemin geliştirilmesi ve test edilmesi amacıyla oluşturulmuş örnek/deneme verileridir.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=flat-square&logo=spacy&logoColor=white)](https://spacy.io/)
[![NLTK](https://img.shields.io/badge/NLTK-green?style=flat-square)](https://www.nltk.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
