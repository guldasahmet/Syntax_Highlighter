# tokens.py

# Dilin jeton tiplerini ve bunlara karşılık gelen düzenli ifadeleri veya anahtar kelimeleri tanımlar.
TOKEN_TYPES = {
    "KEYWORD": ["if", "else", "while", "return", "int", "float"], # C benzeri anahtar kelimeler
    "IDENTIFIER": r"[a-zA-Z_][a-zA-Z0-9_]*", # Tanımlayıcılar için düzenli ifade
    "NUMBER": r"\d+(\.\d+)?", # Sayılar (tam sayılar ve ondalıklı sayılar) için düzenli ifade
    "STRING": r'"[^"\n]*"', # Dizeler için düzenli ifade (tek satırlık, kaçış karakteri desteklenmiyor)
    "OPERATOR": r"(==|!=|<=|>=|[+\-*/=<>])", # Operatörler için düzenli ifade (uzun operatörler önce gelmeli)
    "COMMENT": r"//.*", # Tek satırlık yorumlar için düzenli ifade
    "WHITESPACE": r"\s+", # Boşluk karakterleri için düzenli ifade
    "DELIMITER": r"[;,\(\)\{\}]", # Ayraçlar için düzenli ifade (":" C benzeri dilde genellikle blok başlangıcı için kullanılır, özel bir ayraç olarak tutmaya gerek yok)
    "NEWLINE": r"\n", # Yeni satır karakteri
    # "INDENT": "INDENT", # Girinti artık dilbilgisel bir jeton değil
    # "DEDENT": "DEDENT", # Girinti kaldırma artık dilbilgisel bir jeton değil
}