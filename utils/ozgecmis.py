import pandas as pd # type: ignore
import spacy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS # type: ignore
from nltk.corpus import stopwords # type: ignore
import nltk # type: ignore
def ozgecmis_eslesme():
    # Türkçe stopwords kullanımı
    nltk.download("stopwords")
    turkish_stopwords = set(stopwords.words("turkish"))

    # NLP modelini yükle
    try:
        nlp = spacy.load("tr_core_news_sm")  # Türkçe modeli kullanın
    except:
        nlp = spacy.load("xx_ent_wiki_sm")  # Varsayılan model

    # Özgeçmiş dosyasını oku
    input_path = "C:\\Users\\ASUS\\OneDrive\\Masaüstü\\djangoesra\\djangoesra\\django6\\django\\proje_adi\\cv_bilgileri.csv"
    df = pd.read_csv(input_path)

    # Anlamlı kelimeleri çıkartan fonksiyon
    def extract_meaningful_words(text, stop_words):
        if pd.isna(text):  # Eğer hücre boşsa
            return ""
        doc = nlp(str(text))
        meaningful_words = [
            token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in stop_words
        ]
        return ", ".join(meaningful_words)

    # İşlenecek sütunlar
    columns_to_process = ["Yetenekler", "Dil", "EgitimSeviyesi", "Konum"]

    for column in columns_to_process:
        if column in df.columns:
            # Yeni sütun adı
            processed_column_name = f"{column}_Anlamli_Kelimeler"
            # Anlamlı kelimeleri çıkar
            df[processed_column_name] = df[column].apply(lambda x: extract_meaningful_words(x, turkish_stopwords))
        else:
            print(f"'{column}' sütunu bulunamadı.")

    # Yeni CSV dosyasını kaydet
    output_path = "C:\\Users\\ASUS\\OneDrive\\Masaüstü\\djangoesra\\djangoesra\\django6\\django\\proje_adi\\OzgecmisCvAnlamli.csv"
    df.to_csv(output_path, index=False)

    print(f"Anlamlı kelimeler çıkarıldı ve dosya '{output_path}' olarak kaydedildi.")
    pass