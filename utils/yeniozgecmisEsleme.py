import pandas as pd
import os

# Dosya yolları
sayfa1_path = "C:\\Users\\ASUS\\OneDrive\\Masaüstü\\django5\\django\\proje_adi\\utils\\AnlamliSayfa1.csv"
ozgecmis_path = "C:\\Users\\ASUS\\OneDrive\\Masaüstü\\django5\\django\\proje_adi\\utils\\OzgecmisCvAnlamli.csv"
output_path = "C:\\Users\\ASUS\\OneDrive\\Masaüstü\\django5\\django\\proje_adi\\utils\\ilanCvEslesme.csv"

# Dosyaları yükle
sayfa1_df = pd.read_csv(sayfa1_path)
ozgecmis_df = pd.read_csv(ozgecmis_path)

# Kelime eşleşmelerini bulma fonksiyonu
def find_matching_words(list1, list2):
    if pd.isna(list1):
        list1 = ""
    if pd.isna(list2):
        list2 = ""
    list1 = str(list1)
    list2 = str(list2)
    return list(set(list1.split(", ")) & set(list2.split(", ")))

# Tecrübe eşleşmesi kontrol fonksiyonu
def match_experience(experience, tecrube):
    if pd.isna(experience):
        return 0
    experience = str(experience)
    if experience == "0":
        return 1
    elif "," in experience:
        try:
            start, end = map(int, experience.split(","))
            return 1 if start <= int(tecrube) <= end else 0
        except ValueError:
            return 0
    else:
        try:
            return 1 if int(tecrube) >= int(experience) else 0
        except ValueError:
            return 0

# CV dosyasının son satırını al
cv_row = ozgecmis_df.iloc[-1]  # En alt satır

# Eşleşme sonuçlarını tutacak liste
results = []

# Her bir iş ilanı için eşleşmeleri kontrol et
for _, ilan_row in sayfa1_df.iterrows():
    # Aciklama ile Yetenekler eşleşmesi
    aciklama_yetenek_matches = find_matching_words(
        ilan_row['Aciklama_Anlamli_Kelimeler'], cv_row['Yetenekler_Anlamli_Kelimeler']
    )
    # Aciklama ile Dil eşleşmesi
    aciklama_dil_matches = find_matching_words(
        ilan_row['Aciklama_Anlamli_Kelimeler'], cv_row['Dil_Anlamli_Kelimeler']
    )
    # Konum ile Konum eşleşmesi
    konum_matches = find_matching_words(
        ilan_row['Konum_Anlamli_Kelimeler'], cv_row['Konum_Anlamli_Kelimeler']
    )
    # Eğitim ile EğitimSeviyesi eşleşmesi
    egitim_matches = find_matching_words(
        ilan_row['Egitim_Anlamli_Kelimeler'], cv_row['EgitimSeviyesi_Anlamli_Kelimeler']
    )
    # Deneyim eşleşmesi
    deneyim_match = match_experience(
        ilan_row['Deneyim_Anlamli_Rakamlar'], cv_row['Tecrube']
    )

    # Sonuçları ekle
    results.append({
        "ilan_id": ilan_row['Ilan_id'],
        "id": cv_row['id'],
        "Aciklama_Yetenek_Eslesme_Sayisi": len(aciklama_yetenek_matches),
        "Aciklama_Yetenek_Eslesen_Kelimeler": ", ".join(aciklama_yetenek_matches),
        "Aciklama_Dil_Eslesme_Sayisi": len(aciklama_dil_matches),
        "Aciklama_Dil_Eslesen_Kelimeler": ", ".join(aciklama_dil_matches),
        "Konum_Eslesme_Sayisi": len(konum_matches),
        "Konum_Eslesen_Kelimeler": ", ".join(konum_matches),
        "Egitim_Eslesme_Sayisi": len(egitim_matches),
        "Egitim_Eslesen_Kelimeler": ", ".join(egitim_matches),
        "Deneyim_Eslesme": deneyim_match
    })

# Sonuçları DataFrame'e dönüştür
results_df = pd.DataFrame(results)

# Eğer sonuç dosyası varsa, ekleme yap
if os.path.exists(output_path):
    results_df.to_csv(output_path, mode='a', index=False, header=False)
else:
    results_df.to_csv(output_path, index=False)

print("Son satır eşleştirme sonuçları başarıyla kaydedildi.")
