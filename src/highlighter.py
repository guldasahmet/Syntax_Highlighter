# highlight.py

# Token tiplerine karşılık gelen renk kodları (Tkinter renkleri)
TOKEN_COLORS = {
    "KEYWORD": "blue",         # Anahtar kelimeler mavi
    "IDENTIFIER": "white",    # Tanımlayıcılar beyaz (koyu tema için)
    "NUMBER": "darkorange",    # Sayılar koyu turuncu
    "STRING": "lightgreen",    # Dizeler açık yeşil (koyu tema için)
    "OPERATOR": "red",         # Operatörler kırmızı
    "COMMENT": "gray",         # Yorumlar gri
    "DELIMITER": "purple"      # Ayraçlar mor
}

def get_token_color(token_type):
    """Verilen token tipine karşılık gelen rengi döner."""
    return TOKEN_COLORS.get(token_type, "white")  # Bilinmeyen tip beyaz (koyu tema için)
