import tkinter as tk
import re # Düzenli ifadeler için eklendi
from lexer import tokenize
from highlighter import get_token_color
from parser import Parser # Ayrıştırıcı sınıfını içe aktarın
from tokens import TOKEN_TYPES # TOKEN_TYPES'ı içe aktarın (kısmi vurgulama için)

class SyntaxHighlighterGUI:
    """
    Gerçek zamanlı bir sözdizimi vurgulayıcı için Tkinter tabanlı bir GUI.
    Kodu sözcük olarak vurgular ve dilbilgisi hatalarını tespit etmek için ayrıştırmaya çalışır.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Gerçek Zamanlı Sözdizimi Vurgulayıcı")

        # Duyarlılık için sütun ve satırları yapılandırın
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Kod girişi için metin widget'ı
        # Arka planı koyu, ön planı açık renk yaparak koyu tema ayarları
        self.text = tk.Text(root, wrap="word", font=("Consolas", 12), undo=True,
                            bg="#2D2D2D", fg="#F8F8F8", insertbackground="white") # insertbackground imleç rengi
        self.text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) # Daha iyi düzen için ızgara kullanın

        # Metin widget'ı için kaydırma çubuğu
        scrollbar = tk.Scrollbar(root, command=self.text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=5) # Kaydırma çubuğunu metnin yanına yerleştirin
        self.text.config(yscrollcommand=scrollbar.set)

        # Hata mesajı etiketi
        # Hata mesajının arka planını koyu temaya uygun hale getir
        self.error_label = tk.Label(root, text="Hata yok.", fg="white", bg="#1E1E1E", anchor="w")
        self.error_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=2) # Metin widget'ının altında

        # Gerçek zamanlı vurgulama için tuş bırakma olayını bağlayın
        self.text.bind("<KeyRelease>", self.on_key_release)
        # Enter tuşu için yeni bağlama
        self.text.bind("<Return>", self.on_return_key)
        # Backspace tuşu için yeni bağlama
        self.text.bind("<BackSpace>", self.on_backspace_key)
        
        # Yeni bağlamalar: Otomatik parantez tamamlama ve Tab girintileme
        # KeyPress kullanıyoruz, çünkü karakter metin alanına eklenmeden önce olayı yakalamak istiyoruz.
        self.text.bind("<KeyPress-{>", self.on_open_brace_key) # '{' tuşuna basıldığında
        self.text.bind("<Tab>", self.on_tab_key) # Tab tuşuna basıldığında

        # Her jeton türü rengi için etiket yapılandırması
        # Bu, her jeton türünün nasıl görüntüleneceğini ayarlar
        for token_type in TOKEN_TYPES.keys(): # TOKEN_TYPES'taki tüm anahtarlar için etiketleri yapılandır
            color = get_token_color(token_type)
            self.text.tag_config(token_type, foreground=color)

        # Başlangıçta vurgulama (varsayılan metin için veya dosya yüklendiğinde)
        self.highlight(self.text.get("1.0", "end-1c"))

    def on_key_release(self, event=None):
        """
        Tuş bırakma için olay işleyici. Mevcut kodu alır ve vurgulamayı tetikler.
        """
        code = self.text.get("1.0", "end-1c") # Widget'tan tüm metni alın
        self.highlight(code)

    def on_return_key(self, event):
        """
        Enter tuşu için özel olay işleyici. C benzeri diller için otomatik girintileme sağlar.
        Özellikle '{' sonrası girinti artırımı yapar.
        """
        current_index = self.text.index(tk.INSERT)
        line_start_index = f"{current_index.split('.')[0]}.0"
        
        line_content_before_cursor = self.text.get(line_start_index, current_index)
        
        # Mevcut girintiyi bul
        current_indent = len(line_content_before_cursor) - len(line_content_before_cursor.lstrip())

        # Eğer önceki karakter '{' ise, yeni satır ve bir tab ekle
        if line_content_before_cursor.strip().endswith('{'):
            new_indent = current_indent + 4 # 4 boşluk (bir tab) kadar girinti artır
            self.text.insert(tk.INSERT, "\n" + " " * new_indent)
            self.on_key_release()
            return "break"
        else:
            # Sadece mevcut satırın girintisi kadar boşluk ekle
            self.text.insert(tk.INSERT, "\n" + " " * current_indent)
            self.on_key_release()
            return "break" # Tkinter'ın varsayılan Enter tuşu davranışını tamamen engelle

    def on_backspace_key(self, event):
        """
        Backspace tuşu için özel olay işleyici. Otomatik girintilemeyi geri alır.
        """
        current_index = self.text.index(tk.INSERT)
        line_number, col = map(int, current_index.split('.'))
        
        if col == 0:
            return # İmleç zaten satır başındaysa varsayılan backspace'i kullan

        line_start_index = f"{line_number}.0"
        line_content_before_cursor = self.text.get(line_start_index, current_index)
        
        current_indent = len(line_content_before_cursor) - len(line_content_before_cursor.lstrip())

        # Eğer imleç girintili bir konumdaysa ve girinti 4'ün katı ise
        if col > 0 and col % 4 == 0 and current_indent > 0:
            # Önceki 4 boşluğu sil
            self.text.delete(f"{current_index} - 4 chars", current_index)
            self.on_key_release()
            return "break" # Varsayılan backspace davranışını engelle
        
        return # Varsayılan backspace davranışını sürdür (tek karakter sil)

    def on_open_brace_key(self, event):
        """
        '{' tuşuna basıldığında otomatik olarak '}' ekler ve imleci araya yerleştirir.
        """
        current_index = self.text.index(tk.INSERT)
        
        # İmleçten hemen sonraki karakteri kontrol et
        # Eğer kullanıcı zaten '}' yazmışsa (yani {} yazmak için), otomatik ekleme yapma.
        # Sadece otomatik olarak '{' karakterini ekle ve varsayılan olayları kes.
        char_after_cursor = self.text.get(current_index, f"{current_index} + 1c")
        if char_after_cursor == '}':
            self.text.insert(tk.INSERT, '{')
            self.on_key_release()
            return "break"

        line_number, col = map(int, current_index.split('.'))
        line_start_index = f"{line_number}.0"
        line_content_before_cursor = self.text.get(line_start_index, current_index)
        current_indent = len(line_content_before_cursor) - len(line_content_before_cursor.lstrip())

        # '{' karakterini, yeni satırı, girintili boşluğu, tekrar yeni satırı ve '}' karakterini tek seferde ekle
        self.text.insert(tk.INSERT, "{\n" + " " * (current_indent + 4) + "\n" + " " * current_indent + "}")
        
        # İmleci kapanış parantezinin üstündeki boş satıra taşı
        self.text.mark_set(tk.INSERT, f"{line_number + 1}.{current_indent + 4}")
        self.on_key_release()
        return "break" # Varsayılan Tkinter olayını engelle

    def on_tab_key(self, event):
        """
        Tab tuşuna basıldığında 4 boşluk ekler.
        """
        self.text.insert(tk.INSERT, " " * 4)
        self.on_key_release() # Vurgulamayı tetikle
        return "break" # Varsayılan Tab davranışını engelle

    def highlight(self, code):
        """
        Sözcük analizi ve ayrıştırma yapar, ardından metin widget'ına sözdizimi vurgulamasını uygular.
        Tüm sözcük veya dilbilgisi hatalarını görüntüler.
        """
        # print("\n--- Vurgulama Döngüsü Başladı ---") # Hata ayıklama çıktısı
        # Sıfırdan tekrar vurgulamak için önceki tüm etiketleri temizleyin.
        # Bu, eski vurgulamanın silinen veya değiştirilen metin için kalmamasını sağlar.
        for token_type in TOKEN_TYPES.keys():
            self.text.tag_remove(token_type, "1.0", "end")

        # Önceki hata mesajlarını temizleyin
        self.error_label.config(text="Hata yok.", fg="white") # Koyu tema için hata mesajı rengini beyaz yap

        try:
            # Adım 1: Sözcük Analizi
            # Kodu bir jeton akışına dönüştürün.
            tokens = tokenize(code) 
            # print(f"Lexer'dan alınan jetonlar: {tokens}") # Hata ayıklama çıktısı

            # Adım 2: Sözdizimi Analizi (Ayrıştırma)
            # Dilbilgisel doğruluğu kontrol etmek için jeton akışını ayrıştırmaya çalışın.
            parser = Parser(tokens) 
            # print(f"Ayrıştırıcıya gönderilen jetonlar: {tokens}") # Hata ayıklama çıktısı
            parser.parse() # Dilbilgisi kuralları ihlal edilirse SyntaxError yükseltir.
            # print("Ayrıştırma başarılı.") # Hata ayıklama çıktısı

            # Ayrıştırma başarılı olursa, tüm jetonlarla (boşluk ve yorumlar dahil) sözcük vurgulamasını uygulayın.
            pos = "1.0" # Etiketleme için başlangıç konumu
            for token_type, token_value in tokens: # Tüm jetonları kullan
                if token_type == "EOF":
                    break # Dosya sonu jetonunda durun.
                
                # Token'ın uzunluğu None veya sıfır ise atlayın.
                length = len(token_value) if token_value is not None else 0
                if length == 0:
                    # print(f"Uyarı: Sıfır uzunlukta jeton bulundu: {token_type}, Değer: '{token_value}'") # Hata ayıklama çıktısı
                    continue
                
                start_index = pos
                # Bitiş indeksini ve bir sonraki başlangıç konumunu Tkinter'ın index metodunu kullanarak hesapla.
                end_index = self.text.index(f"{start_index} + {length} chars")
                
                # Belirlenen aralığa belirli jeton türü etiketini uygulayın.
                self.text.tag_add(token_type, start_index, end_index)
                # print(f"Etiket uygulandı: {token_type}, Değer: '{token_value}', Başlangıç: {start_index}, Bitiş: {end_index}") # Hata ayıklama çıktısı

                # Bir sonraki jeton için başlangıç konumunu güncelleyin.
                pos = end_index 

        except SyntaxError as e:
            # print(f"Sözdizimi Hatası yakalandı: {e}") # Hata ayıklama çıktısı
            # SyntaxError oluşursa (sözcük çözümleyiciden veya ayrıştırıcıdan), görüntüleyin.
            self.error_label.config(text=f"Sözdizimi Hatası: {e}", fg="red")
            
            # Hata noktasında bile vurgulamayı sürdürmek için lexer.py'deki tokenize fonksiyonunun bir benzerini burada tekrar çalıştırıyoruz.
            try:
                # Hatadan önceki geçerli jetonlar için kısmi vurgulama uygulayın.
                temp_tokens = tokenize(code) 
                # print(f"Kısmi vurgulama jetonları: {temp_tokens}") # Hata ayıklama çıktısı
                
                pos = "1.0"
                for token_type, token_value in temp_tokens:
                    if token_type == "EOF":
                        break
                    
                    # Token'ın uzunluğu None veya sıfır ise atlayın.
                    length = len(token_value) if token_value is not None else 0
                    if length == 0:
                        # print(f"Uyarı: Sıfır uzunlukta jeton bulundu (kısmi vurgulama): {token_type}, Değer: '{token_value}'") # Hata ayıklama çıktısı
                        continue

                    start_index = pos
                    # Bitiş indeksini ve bir sonraki başlangıç konumunu Tkinter'ın index metodunu kullanarak hesapla.
                    end_index = self.text.index(f"{start_index} + {length} chars")
                    
                    self.text.tag_add(token_type, start_index, end_index)
                    # print(f"Kısmi etiket uygulandı: {token_type}, Değer: '{token_value}', Başlangıç: {start_index}, Bitiş: {end_index}") # Hata ayıklama çıktısı
                    pos = end_index

            except Exception as inner_e:
                # GUI'nin çökmesini önlemek için kısmi vurgulama sırasında oluşan hataları yakalayın.
                print(f"Kısmi vurgulama sırasında beklenmedik hata: {inner_e}")


        except Exception as e:
            # print(f"Beklenmedik bir hata yakalandı: {e}") # Hata ayıklama çıktısı
            # Jetonlama veya ayrıştırma sırasında ortaya çıkan diğer beklenmedik hataları yakalayın.
            self.error_label.config(text=f"Beklenmedik bir hata oluştu: {e}", fg="red")

    def run(self):
        """
        GUI uygulaması için Tkinter olay döngüsünü başlatır.
        """
        self.root.mainloop()

