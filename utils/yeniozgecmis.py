import pandas as pd
import spacy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.corpus import stopwords
import nltk
import os

# Türkçe stopwords kullanımı
#nltk.download("stopwords")
turkish_stopwords = set(stopwords.words("turkish"))

# NLP modelini yükle
try:
    nlp = spacy.load("tr_core_news_sm")  # Türkçe modeli kullanın
except:
    nlp = spacy.load("xx_ent_wiki_sm")  # Varsayılan model

# Anlamlı kelimeleri çıkartan fonksiyon
def extract_meaningful_words(text, stop_words):
    if pd.isna(text):  # Eğer hücre boşsa
        return ""
    doc = nlp(str(text))
    meaningful_words = [
        token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in stop_words
    ]
    return ", ".join(meaningful_words)

# Giriş dosyası ve çıkış dosyası yolları
input_path = r"C:\\Users\\ASUS\\OneDrive\\Masaüstü\\django5\\django\\proje_adi\\cv_bilgileri.csv"
output_path = r"C:\\Users\\ASUS\\OneDrive\\Masaüstü\\django5\\django\\proje_adi\\utils\\OzgecmisCvAnlamli.csv"

# cv_bilgileri.csv'den son satırı oku
df_input = pd.read_csv(input_path)
if df_input.empty:
    print("Giriş dosyası boş.")
else:
    last_row = df_input.tail(1)  # Son satırı al

    # İşlenecek sütunlar
    columns_to_process = ["Yetenekler", "Dil", "EgitimSeviyesi", "Konum"]
    
    # Son satırda anlamlı kelimeleri işle
    for column in columns_to_process:
        if column in last_row.columns:
            # Yeni sütun adı
            processed_column_name = f"{column}_Anlamli_Kelimeler"
            # Anlamlı kelimeleri çıkar
            last_row[processed_column_name] = last_row[column].apply(lambda x: extract_meaningful_words(x, turkish_stopwords))
        else:
            print(f"'{column}' sütunu bulunamadı.")

    # Eğer çıkış dosyası zaten varsa, son satırı dosyaya ekle
    if os.path.exists(output_path):
        df_output = pd.read_csv(output_path)
        df_output = pd.concat([df_output, last_row], ignore_index=True)
    else:
        # Çıkış dosyası yoksa, son satırdan yeni bir dosya oluştur
        df_output = last_row

    # Güncellenmiş veriyi dosyaya yaz
    df_output.to_csv(output_path, index=False)
    print(f"Son satır işlendi ve  dosyasına eklendi.")
