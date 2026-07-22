import pandas as pd
import spacy
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# NLP modelini yükle
nlp = spacy.load("xx_ent_wiki_sm")

# Sayfa1'den ve AnlamliSayfa1'den verileri yükle
sayfa1_path = r"C:\\Users\\ASUS\\OneDrive\\Masaüstü\\django5\\django\\proje_adi\\sayfa1.csv"
anlamli_path = r"C:\\Users\\ASUS\\OneDrive\\Masaüstü\\django5\\django\\proje_adi\\utils\\AnlamliSayfa1.csv"

sayfa1_df = pd.read_csv(sayfa1_path)
anlamli_df = pd.read_csv(anlamli_path)

# Son satırdaki veriyi al
son_satira = sayfa1_df.tail(1).copy()  # copy() ekledik

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
son_satira.loc[:, 'Aciklama_Anlamli_Kelimeler'] = son_satira['Aciklama'].apply(extract_meaningful_words)
son_satira.loc[:,'Konum_Anlamli_Kelimeler'] = son_satira['Konum'].apply(extract_meaningful_words)
son_satira.loc[:,'Egitim_Anlamli_Kelimeler'] = son_satira['Egitim'].apply(extract_meaningful_words)

# Deneyim sütunundaki anlamlı rakamları ve özel ifadeleri çıkaralım
son_satira.loc[:,'Deneyim_Anlamli_Rakamlar'] = son_satira['Deneyim'].apply(extract_experience)

# AnlamliSayfa1'e son satırı ekleyin
anlamli_df = pd.concat([anlamli_df, son_satira], ignore_index=True)

# Birleştirilmiş veriyi kaydet
anlamli_df.to_csv(anlamli_path, index=False)

print("Son satır başarıyla işlendi ve AnlamliSayfa1'e eklendi.")
