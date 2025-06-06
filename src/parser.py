class Parser:
    """
    Basit bir C benzeri dil için Yukarıdan Aşağıya (Özyinelemeli İniş) Ayrıştırıcı.
    Sözcük çözümleyiciden gelen jeton listesini alır ve bunları
    tanımlanmış bir dilbilgisine göre ayrıştırmaya çalışır.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0 # Jeton akışındaki mevcut konum
        # print("Parser: Başlatıldı.") # Hata ayıklama çıktısı

    def current(self):
        """
        self.pos konumundaki mevcut jetonu döndürür.
        Jeton akışının sonuna gelindiyse ("EOF", None) döndürür.
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("EOF", None)

    def match(self, expected_type):
        """
        Mevcut jetonun türü expected_type ile eşleşirse jetonu tüketir.
        Uyumsuzluk durumunda SyntaxError yükseltir.
        """
        tok_type, tok_val = self.current()
        # print(f"Parser Match: Beklenen tip '{expected_type}', mevcut '{tok_type}' ('{tok_val}')") # Hata ayıklama çıktısı
        if tok_type == expected_type:
            self.pos += 1
            return tok_val
        else:
            # print(f"Parser Match Hata: Beklenen '{expected_type}', alındı '{tok_type}'") # Hata ayıklama çıktısı
            raise SyntaxError(f"Beklenen jeton türü '{expected_type}', alındı '{tok_type}' ('{tok_val}')")

    def expect(self, expected_type, expected_value=None):
        """
        Mevcut jetonun türü ve isteğe bağlı olarak değeri eşleşirse jetonu tüketir.
        Uyumsuzluk durumunda SyntaxError yükseltir.
        """
        tok_type, tok_val = self.current()
        # print(f"Parser Expect: Beklenen '{expected_type}' ('{expected_value or ''}'), mevcut '{tok_type}' ('{tok_val or ''}')") # Hata ayıklama çıktısı
        if tok_type == expected_type and (expected_value is None or tok_val == expected_value):
            self.pos += 1
            return tok_val
        else:
            # print(f"Parser Expect Hata: Beklenen '{expected_type}' ('{expected_value or ''}'), alındı '{tok_type}' ('{tok_val or ''}')") # Hata ayıklama çıktısı
            raise SyntaxError(f"Beklenen '{expected_type}' ('{expected_value or ''}'), alındı '{tok_type}' ('{tok_val or ''}')")

    def parse(self):
        """
        Ayrıştırma sürecini başlatır. Dosya sonuna (EOF) kadar ifadeleri ayrıştırır.
        """
        # print("Parser: Ayrıştırma başladı.") # Hata ayıklama çıktısı
        while self.current()[0] != "EOF":
            # Boşluk ve yeni satır jetonlarını atla (ayrıştırma için anlamsızdırlar)
            while self.current()[0] in ["WHITESPACE", "NEWLINE"]:
                self.pos += 1
            if self.current()[0] == "EOF": # Boşluklardan sonra EOF'a ulaştıysak döngüden çık
                break
            self.statement()
        # print("Parser: Ayrıştırma bitti.") # Hata ayıklama çıktısı

    def statement(self):
        """
        Mevcut jetonun değerine göre tek bir ifadeyi ayrıştırır.
        Farklı ifade türleri için belirli ayrıştırma metotlarına gönderir.
        """
        tok_type, tok_val = self.current()
        # print(f"Parser Statement: '{tok_val}' ifadesini ayrıştırılıyor.") # Hata ayıklama çıktısı
        if tok_val == "if":
            self.if_stmt()
        elif tok_val == "while":
            self.while_stmt()
        elif tok_val == "return":
            self.return_stmt()
        elif tok_val in ("int", "float"):
            self.declaration()
        else:
            self.expression_stmt()

    def if_stmt(self):
        """
        İsteğe bağlı 'else if' ve 'else' yan tümcelerini içeren bir 'if' ifadesini ayrıştırır.
        Dilbilgisi: "if" "(" <expression> ")" <block> [ "else" ( "if" "(" <expression> ")" <block> | <block> ) ]
        """
        # print("Parser: if_stmt başladı.") # Hata ayıklama çıktısı
        self.expect("KEYWORD", "if")
        self.expect("DELIMITER", "(") # 'if (condition)'
        self.expression()
        self.expect("DELIMITER", ")")
        
        # Bloğa girmeden önce tüm boşlukları ve yeni satırları atla
        while self.current()[0] in ["WHITESPACE", "NEWLINE"]:
            self.pos += 1
        
        self.block() # if bloğu

        # Bloğun ardından gelen boşluk ve yeni satırları atla
        while self.current()[0] in ["WHITESPACE", "NEWLINE"]:
            self.pos += 1

        if self.current() == ("KEYWORD", "else"):
            # print("Parser: else bloğu başladı.") # Hata ayıklama çıktısı
            self.expect("KEYWORD", "else")
            
            # Bloğa girmeden önce tüm boşlukları ve yeni satırları atla
            while self.current()[0] in ["WHITESPACE", "NEWLINE"]:
                self.pos += 1

            # C'de 'else if' aslında bir 'else' bloğunun içindeki bir 'if'tir.
            if self.current() == ("KEYWORD", "if"):
                self.if_stmt() # Özyinelemeli olarak if_stmt'yi çağır
            else:
                self.block() # else bloğu
            # print("Parser: else bloğu bitti.") # Hata ayıklama çıktısı
        # print("Parser: if_stmt bitti.") # Hata ayıklama çıktısı


    def while_stmt(self):
        """
        Bir 'while' ifadesini ayrıştırır.
        Dilbilgisi: "while" "(" <expression> ")" <block>
        """
        # print("Parser: while_stmt başladı.") # Hata ayıklama çıktısı
        self.expect("KEYWORD", "while")
        self.expect("DELIMITER", "(") # 'while (condition)'
        self.expression()
        self.expect("DELIMITER", ")")

        # Bloğa girmeden önce tüm boşlukları ve yeni satırları atla
        while self.current()[0] in ["WHITESPACE", "NEWLINE"]:
            self.pos += 1

        self.block() # while bloğu
        # print("Parser: while_stmt bitti.") # Hata ayıklama çıktısı


    def return_stmt(self):
        """
        Bir 'return' ifadesini ayrıştırır.
        Dilbilgisi: "return" <expression> ";"
        """
        # print("Parser: return_stmt başladı.") # Hata ayıklama çıktısı
        self.expect("KEYWORD", "return")
        self.expression()
        self.expect("DELIMITER", ";") # C benzeri dilde ifade sonu için noktalı virgül
        # print("Parser: return_stmt bitti.") # Hata ayıklama çıktısı


    def declaration(self):
        """
        Bir değişken bildirimini ayrıştırır.
        Dilbilgisi: ( "int" | "float" ) IDENTIFIER "=" <expression> ";"
        """
        # print("Parser: declaration başladı.") # Hata ayıklama çıktısı
        tok = self.current()
        if tok[1] in ("int", "float"):
            self.match("KEYWORD") # 'int' veya 'float' tüket
        else:
            raise SyntaxError(f"Beklenen tip anahtar kelimesi, alındı {tok}")

        self.expect("IDENTIFIER")
        self.expect("OPERATOR", "=")
        self.expression()
        self.expect("DELIMITER", ";") # C benzeri dilde ifade sonu için noktalı virgül
        # print("Parser: declaration bitti.") # Hata ayıklama çıktısı


    def expression_stmt(self):
        """
        Yalnızca bir ifadeden oluşan bir ifadeyi ayrıştırır.
        Dilbilgisi: <expression> ";"
        """
        # print("Parser: expression_stmt başladı.") # Hata ayıklama çıktısı
        self.expression()
        self.expect("DELIMITER", ";") # C benzeri dilde ifade sonu için noktalı virgül
        # print("Parser: expression_stmt bitti.") # Hata ayıklama çıktısı


    def block(self):
        """
        Bir ifade bloğunu ayrıştırır. C benzeri dilde, bir blok '{' ile başlar ve '}' ile biter.
        İçinde bir dizi ifade bulunur.
        Dilbilgisi: "{" { <statement> }* "}"
        """
        # print("Parser Block: Bloğa girildi.") # Hata ayıklama çıktısı
        self.expect("DELIMITER", "{") # '{' bekle ve tüket

        # '}' jetonu veya dosya sonuna gelene kadar ifadeleri ayrıştır
        while self.current()[0] != "EOF" and not (self.current()[0] == "DELIMITER" and self.current()[1] == "}"):
            # Her ifadeden önce ve sonra boşluk/yeni satır jetonlarını atla
            while self.current()[0] in ["WHITESPACE", "NEWLINE"]:
                self.pos += 1
            if self.current()[0] == "EOF" or (self.current()[0] == "DELIMITER" and self.current()[1] == "}"): # Boşluklardan sonra EOF veya '}' a ulaştıysak döngüden çık
                break
            self.statement()
        
        self.expect("DELIMITER", "}") # '}' bekle ve tüket
        # print("Parser Block: Bloktan çıkıldı.") # Hata ayıklama çıktısı


    def expression(self):
        """
        Toplama, çıkarma ve karşılaştırma operatörlerini işleyen bir ifadeyi ayrıştırır.
        Dilbilgisi: <term> { ( "+" | "-" | ">" | "<" | "==" | "!=" | ">=" | "<=" ) <term> }*
        """
        # print("Parser: expression başladı.") # Hata ayıklama çıktısı
        self.term() # İlk terimi ayrıştır
        while self.current()[1] in ("+", "-", ">", "<", "==", "!=", ">=", "<="):
            self.match("OPERATOR") # Operatörü tüket
            self.term() # Sonraki terimi ayrıştır
        # print("Parser: expression bitti.") # Hata ayıklama çıktısı


    def term(self):
        """
        Çarpma ve bölme operatörlerini işleyen bir terimi ayrıştırır.
        Dilbilgisi: <factor> { ( "*" | "/" ) <factor> }*
        """
        # print("Parser: term başladı.") # Hata ayıklama çıktısı
        self.factor() # İlk faktörü ayrıştır
        while self.current()[1] in ("*", "/"):
            self.match("OPERATOR") # Operatörü tüket
            self.factor() # Sonraki faktörü ayrıştır
        # print("Parser: term bitti.") # Hata ayıklama çıktısı


    def factor(self):
        """
        Bir faktörü (bir ifadenin en temel birimi) ayrıştırır.
        Dilbilgisi: NUMBER | IDENTIFIER | "(" <expression> ")"
        """
        # print(f"Parser: factor başladı. Mevcut jeton: {self.current()}") # Hata ayıklama çıktısı
        tok_type, tok_val = self.current()
        if tok_type == "NUMBER":
            self.match("NUMBER") # Sayıyı tüket
        elif tok_type == "IDENTIFIER":
            self.match("IDENTIFIER") # Tanımlayıcıyı tüket
        elif tok_val == "(":
            self.expect("DELIMITER", "(") # '(' tüket
            self.expression() # İç içe ifadeyi ayrıştır
            self.expect("DELIMITER", ")") # ')' bekle ve tüket
        else:
            raise SyntaxError(f"İfadedeki beklenmedik jeton: {self.current()}")
        # print("Parser: factor bitti.") # Hata ayıklama çıktısı

