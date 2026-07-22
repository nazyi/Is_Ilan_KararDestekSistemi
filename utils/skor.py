import pandas as pd # type: ignore
def skor_hesapla():
    # 1. CSV dosyasını yükleyin
    df = pd.read_csv("C:\\Users\\ASUS\\OneDrive\\Masaüstü\\djangoesra\\djangoesra\\django6\\django\\proje_adi\\ilanCvEslesme.csv")

    # 2. Ağırlıkları tanımlayın
    weights = {
        'yetenek': 0.51,
        'tecrübe': 0.26,
        'konum': 0.14,
        'eğitim': 0.05,
        'dil': 0.04
    }

    # 3. Sabit toplam yetenek sayısı (eğer her ilan için farklı ise, bu değeri her satırda dinamik olarak hesaplayın)
    total_skills = 10

    # 4. Benzerlik skoru hesaplama fonksiyonu
    def calculate_similarity(row):
        # Yetenek skoru: eşleşen yetenek sayısı / toplam yetenek sayısı
        skill_score = row['Aciklama_Yetenek_Eslesme_Sayisi'] / total_skills

        # Diğer özellik skorları
        experience_score = row['Deneyim_Eslesme']  # 1 veya 0
        location_score = row['Konum_Eslesme_Sayisi']      # 1 veya 0
        education_score = row['Egitim_Eslesme_Sayisi']    # 1 veya 0
        language_score = row['Aciklama_Dil_Eslesme_Sayisi']        # Eşleşen dil sayısı

        # Toplam skor
        similarity_score = (
            weights['yetenek'] * skill_score +
            weights['tecrübe'] * experience_score +
            weights['konum'] * location_score +
            weights['eğitim'] * education_score +
            weights['dil'] * language_score
        )
        return similarity_score

    # 5. Her satır için benzerlik skoru hesapla
    df['Benzerlik_Skoru'] = df.apply(calculate_similarity, axis=1)

    # 6. Yeni Excel dosyasına kaydet
    df.to_csv('C:\\Users\\ASUS\\OneDrive\\Masaüstü\\djangoesra\\djangoesra\\django6\\django\\proje_adi\\Skor.csv', index=False)

    print("Benzerlik skorları başarıyla kaydedildi.")
    pass