import re
from tokens import TOKEN_TYPES

class Lexer:
    """
    C benzeri bir dil için sözcük çözümleyici.
    Giriş kodunu jetonlara ayırır. C benzeri dillerde girintileme dilbilgisel olarak anlamlı değildir,
    bu nedenle INDENT ve DEDENT jetonları üretilmez.
    """
    def __init__(self, code):
        self.code = code
        self.length = len(code)
        self.idx = 0
        self.tokens = []

    def _add_token(self, token_type, value):
        """Üretilen jetonu listeye ekler."""
        self.tokens.append((token_type, value))

    def tokenize(self):
        """
        Giriş kodunu jetonlara ayırır.
        """
        while self.idx < self.length:
            match_found = False

            # Önce yeni satır karakterini kontrol et
            if self.code.startswith('\n', self.idx):
                self._add_token("NEWLINE", "\n")
                self.idx += 1
                match_found = True
                continue
            
            # Satır içi boşlukları kontrol et
            whitespace_match = re.compile(TOKEN_TYPES["WHITESPACE"]).match(self.code, self.idx)
            if whitespace_match:
                value = whitespace_match.group()
                self._add_token("WHITESPACE", value)
                self.idx += len(value)
                match_found = True
                continue

            # Keyword'leri öncelikli olarak kontrol et
            for keyword in TOKEN_TYPES["KEYWORD"]:
                kw_len = len(keyword)
                # Tam bir kelime eşleşmesi olduğundan emin olun (tanımlayıcının bir parçası olmamalı)
                if self.code.startswith(keyword, self.idx) and \
                   (self.idx + kw_len == self.length or not re.match(r"[a-zA-Z0-9_]", self.code[self.idx + kw_len:self.idx + kw_len + 1])):
                    self._add_token("KEYWORD", keyword)
                    self.idx += kw_len
                    match_found = True
                    break
            if match_found:
                continue

            # Diğer jeton tiplerini sırayla dene (WHITESPACE, NEWLINE, KEYWORD özel olarak işlendi)
            # INDENT ve DEDENT artık token_types'ta tanımlı olsalar bile burada işlenmeyecekler.
            for token_type, pattern in TOKEN_TYPES.items():
                if token_type in ["KEYWORD", "WHITESPACE", "NEWLINE", "INDENT", "DEDENT"]:
                    continue
                
                regex = re.compile(pattern)
                match = regex.match(self.code, self.idx)
                if match:
                    value = match.group()
                    self._add_token(token_type, value)
                    self.idx += len(value)
                    match_found = True
                    break
            
            if not match_found:
                # Tanımlanamayan bir karakterle karşılaşılırsa hata fırlat
                raise SyntaxError(f"Tanımlanamayan karakter: '{self.code[self.idx]}' pozisyon: {self.idx}")

        # Dosya sonu jetonunu ekle
        self._add_token("EOF", None)
        return self.tokens

# Kullanım için kolaylaştırıcı fonksiyon
def tokenize(code):
    lexer = Lexer(code)
    return lexer.tokenize()

