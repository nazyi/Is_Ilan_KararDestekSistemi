import pandas as pd

# 1. CSV dosyasını yükleyin
df = pd.read_csv(r"C:\\Users\\ASUS\\OneDrive\\Masaüstü\\django5\\django\\proje_adi\\utils\\ilanCvEslesme.csv")

# 2. Ağırlıkları tanımlayın
weights = {
    'yetenek': 0.51,
    'tecrübe': 0.26,
    'konum': 0.14,
    'eğitim': 0.05,
    'dil': 0.04
}

# 3. Son satırdaki ilan_id'yi al
last_ilan_id = df.iloc[-1]['ilan_id']  # son satırdaki ilan_id'yi al

# 4. Bu ilan_id ile eşleşen tüm satırları filtrele
filtered_df = df[df['ilan_id'] == last_ilan_id].copy()  # Kopya alarak işlemi güvenli hale getiriyoruz

# 5. Benzerlik skoru hesaplama fonksiyonu
def calculate_similarity(row):
    total_skills = row['Toplam_Yetenek'] if 'Toplam_Yetenek' in row else 10  # Eğer 'Toplam_Yetenek' kolonunu kontrol et
    skill_score = row['Aciklama_Yetenek_Eslesme_Sayisi'] / total_skills if total_skills != 0 else 0
    
    # Diğer özellik skorları
    experience_score = row['Deneyim_Eslesme']  # 1 veya 0
    location_score = row['Konum_Eslesme_Sayisi']  # 1 veya 0
    education_score = row['Egitim_Eslesme_Sayisi']  # 1 veya 0
    language_score = row['Aciklama_Dil_Eslesme_Sayisi']  # Eşleşen dil sayısı
    
    # Toplam skor
    similarity_score = (
        weights['yetenek'] * skill_score +
        weights['tecrübe'] * experience_score +
        weights['konum'] * location_score +
        weights['eğitim'] * education_score +
        weights['dil'] * language_score
    )
    return similarity_score

# 6. Filtrelenmiş satırlar için benzerlik skoru hesapla
filtered_df['Benzerlik Skoru'] = filtered_df.apply(calculate_similarity, axis=1)

# 7. Güncellenmiş satırları orijinal dataframe'e geri ekle
df.loc[df['ilan_id'] == last_ilan_id, 'Benzerlik Skoru'] = filtered_df['Benzerlik Skoru']

# 8. Yeni Excel dosyasına kaydet
df.to_excel('C:\\Users\\ASUS\\OneDrive\\Masaüstü\\sskor.xlsx', index=False)

print("Benzerlik skorları başarıyla kaydedildi.")
