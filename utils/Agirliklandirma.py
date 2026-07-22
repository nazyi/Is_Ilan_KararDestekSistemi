import numpy as np

# Kriterler arası çift karşılaştırma matrisi
criteria_matrix = np.array([
    [1, 3, 5, 7, 9],  # Yetenek
    [1/3, 1, 3, 5, 7], # Tecrübe
    [1/5, 1/3, 1, 3, 5], # Konum
    [1/7, 1/5, 1/3, 1, 1], # Eğitim
    [1/9, 1/7, 1/5, 1, 1] # Dil
])

# Sütun toplamlarını hesaplayın
column_sums = criteria_matrix.sum(axis=0)

# Normalleştirilmiş matrisi oluşturun
normalized_matrix = criteria_matrix / column_sums

# Kriter ağırlıklarını hesaplayın (ortalama)
weights = normalized_matrix.mean(axis=1)

# Ağırlıkları normalize edin
weights /= weights.sum()

# Sonuçları yazdırın
print("Kriter Ağırlıkları:")
print(f"Yetenek: {weights[0]:.2f}, Tecrübe: {weights[1]:.2f}, Konum: {weights[2]:.2f}, Eğitim: {weights[3]:.2f}, Dil: {weights[4]:.2f}")
