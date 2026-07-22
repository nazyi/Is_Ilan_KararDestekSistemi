import pandas as pd # type: ignore
import spacy
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS # type: ignore
def process_data():
    # NLP modelini yükleyelim
    nlp = spacy.load("xx_ent_wiki_sm")

    # sayfa1.csv dosyasını oku
    df = pd.read_csv("C:\\Users\\ASUS\\OneDrive\\Masaüstü\\djangoesra\\djangoesra\\django6\\django\\proje_adi\\sayfa1.csv")

    # Anlamlı kelimeleri çıkartmak için fonksiyon
    def extract_meaningful_words(text):
        doc = nlp(str(text))
        meaningful_words = [token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in ENGLISH_STOP_WORDS]
        return ", ".join(meaningful_words)

    # Deneyim sütunundaki rakamları ve özel ifadeleri çıkartmak için fonksiyon
    def extract_experience(text):
        if not isinstance(text, str):  # Eğer boş bir hücre varsa
            return ""
        text = text.lower()
        # "Tecrübeli" ve "Tecrübesiz" için özel kontrol
        if "tecrübeli" in text or "tecrübesiz" in text:
            return "0"
        # Sayıları ve aralıkları ayıklama
        numbers = re.findall(r'\d+', text)
        if len(numbers) == 1:  # Tek bir sayı belirtilmişse
            return numbers[0]
        elif len(numbers) > 1:  # Bir aralık varsa
            return ",".join(numbers)
        return ""  # Eğer hiçbir sayı bulunamazsa

    # Sadece gerekli sütunlarda anlamlı kelimeleri çıkartalım
    df['Aciklama_Anlamli_Kelimeler'] = df['Aciklama'].apply(extract_meaningful_words)
    df['Konum_Anlamli_Kelimeler'] = df['Konum'].apply(extract_meaningful_words)
    df['Egitim_Anlamli_Kelimeler'] = df['Egitim'].apply(extract_meaningful_words)

    # Deneyim sütunundaki anlamlı rakamları ve özel ifadeleri çıkaralım
    df['Deneyim_Anlamli_Rakamlar'] = df['Deneyim'].apply(extract_experience)

    # Yeni Excel dosyasını kaydedelim
    df.to_csv('C:\\Users\\ASUS\\OneDrive\\Masaüstü\\djangoesra\\djangoesra\\django6\\django\\proje_adi\\AnlamliSayfa1.csv', index=False)

    print("İşlem tamamlandı, dosya kaydedildi!")
    pass