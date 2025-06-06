#  Gerçek Zamanlı Sözdizimi Vurgulayıcı

[![YouTube Demo Video](https://img.youtube.com/vi/9qZDD1aRdTo/0.jpg)](https://www.youtube.com/watch?v=9qZDD1aRdTo) 



**Yukarıdaki görsel, projenin YouTube demo videosuna bağlantı vermektedir. Videoyu izlemek için tıklayınız.**

## 🚀 Proje Genel Bakışı

Bu proje, basit bir C benzeri dil için sıfırdan geliştirilmiş, gerçek zamanlı bir sözdizimi vurgulayıcıya sahip interaktif bir masaüstü uygulamasıdır (GUI). Amacımız, harici bir sözdizimi vurgulama kütüphanesi kullanmadan, Bilgisayar Bilimleri ve Derleyiciler derslerindeki **Lexical Analiz** ve **Sözdizimi Analizi (Parsing)** prensiplerini kullanarak kodun nasıl anlaşıldığını ve görsel olarak vurgulandığını göstermektir. Geliştiriciler, kod yazarken anında görsel geri bildirim ve potansiyel sözdizimi hataları hakkında bilgi alabilirler.

**Temel Felsefe:** "Hiçbir harici sözdizimi vurgulama kütüphanesi kullanılmamıştır." Tüm Lexer, Parser ve Vurgulama mantığı sıfırdan Python ile implemente edilmiştir. Bu, projenin özgünlüğünü ve temel prensiplere uygunluğunu vurgular.

## ✨ Temel Özellikler

* **Gerçek Zamanlı Sözdizimi Vurgulama:** Kullanıcı metin alanına kod yazdıkça, uygulama her tuş vuruşunda kodu anında analiz eder ve belirlenen kurallara göre renklendirir.
* **Tamamen Özel Geliştirilmiş Çözüm:** Proje, Python'ın standart kütüphaneleri (özellikle `re` modülü ve `tkinter`) kullanılarak sıfırdan inşa edilmiştir. Harici bir sözdizimi vurgulama veya ayrıştırma kütüphanesine bağımlılık yoktur.
* **Basit C Benzeri Dil Desteği:** Uygulama, aşağıdaki yapıları içeren bir C benzeri dilbilgisini destekler:
    * **Anahtar Kelimeler:** `if`, `else`, `while`, `return`, `int`, `float`
    * **Değişken Tanımlamaları:** `int x;`, `float y = 10.5;`
    * **Kontrol Akış İfadeleri:** `if (koşul) { ... } else { ... }`, `while (koşul) { ... }`
    * **İfade İfadeleri:** `a = b + c;`, `return x;`
    * **Aritmetik ve Karşılaştırma Operatörleri:** `+`, `-`, `*`, `/`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`
    * **Ayraçlar:** `(`, `)`, `{`, `}`, `;`, `,`
    * **Yorumlar:** Tek satırlık yorumlar (`//`)
* **Özel Lexer (Sözcük Çözümleyici):**
    * **Yaklaşım:** Durum Diyagramı ve Program Uygulaması.
    * **Uygulama:** Python'ın `re` (regular expression) modülü kullanılarak jetonlar düzenli ifadelerle tanınır.
    * **Önemli Not:** C benzeri dillerde girintileme dilbilgisel olarak anlamlı (Python'daki gibi) olmadığı için `INDENT` ve `DEDENT` jetonları üretilmez.
* **Özel Parser (Sözdizimi Çözümleyici):**
    * **Yaklaşım:** Yukarıdan Aşağıya (Top-Down) / Özyinelemeli İniş (Recursive Descent) ayrıştırma yöntemi.
    * **İşlev:** Lexer'dan gelen jeton akışını tanımlı C benzeri dilbilgisine göre ayrıştırmaya çalışır. Eğer jeton akışı dilbilgisi kurallarına uymazsa `SyntaxError` fırlatır.
* **Zengin GUI Deneyimi (Tkinter):**
    * **Akıllı Otomatik Girintileme:** Yeni satırda otomatik olarak doğru girintiyi sağlar ve `Backspace` tuşuyla girintileri kolayca geri almanızı mümkün kılar.
    * **Akıllı Parantez Tamamlama:** `{` tuşuna basıldığında, uygulama otomatik olarak alt satırda girintili bir boşluk bırakıp kapanış `}` parantezini yerleştirir ve imleci tam da kod yazmanız gereken yere konumlandırır. Bu özellik, blok yazımını hızlandırır ve parantez hatalarını azaltır.
    * **Tutarlı Tab Boşlukları:** `Tab` tuşuna basıldığında her zaman 4 boşluk eklenir, böylece kodunuz her zaman düzenli ve tutarlı bir girintilemeye sahip olur.
    * **Canlı Hata Mesajı:** Sözdizimi hataları, GUI'nin altında kırmızı renkte bir metinle anında görüntülenir. Bu, kullanıcının sorunları hızlıca fark etmesini sağlar.
    * **Duyarlı Tasarım:** Pencere boyutlandırıldığında metin alanı da dinamik olarak boyutlanır, bu da farklı ekran çözünürlüklerinde tutarlı bir kullanıcı deneyimi sunar.
* **Çeşitli Token Desteği:** En az 7 farklı jeton tipi için belirgin renkli vurgulama uygulanmıştır:
    * **KEYWORD:** Mavi (`if`, `else`, `while`, `return`, `int`, `float`)
    * **IDENTIFIER:** Beyaz (değişken isimleri, fonksiyon isimleri)
    * **NUMBER:** Koyu Turuncu (sayılar: `123`, `4.5`)
    * **STRING:** Açık Yeşil (dizeler: `"Merhaba Dünya"`)
    * **OPERATOR:** Kırmızı (`+`, `-`, `=`, `==`, `>=`, `*`, `/`)
    * **COMMENT:** Gri (`// Tek satırlık yorum`)
    * **DELIMITER:** Mor (ayraçlar: `(`, `)`, `{`, `}`, `;`, `,`)


## 🛠️ Kullanılan Teknolojiler

* **Programlama Dili:** Python 3.x
* **GUI Kütüphanesi:** Tkinter (Python Standart Kütüphanesi)
* **Regex İşleme:** Python `re` modülü

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel ortamınızda çalıştırabilmek için Python 3.x'in kurulu olması yeterlidir. Tkinter genellikle Python ile birlikte gelir ve ek bir kurulum gerektirmez.

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [GITHUB_DEPO_LINKI]
    cd [PROJE_ADI]
    ```
2.  **Uygulamayı Çalıştırın:**
    ```bash
    python src/main.py
    ```
    Uygulama açıldıktan sonra, metin alanına C benzeri kod yazmaya başlayabilir ve gerçek zamanlı vurgulamayı, akıllı düzenleme özelliklerini ve hata kontrolünü deneyimleyebilirsiniz.

## 📊 Dokümantasyon ve Video Gösterimi

Proje ödev gereksinimleri doğrultusunda hazırlanan detaylı dokümantasyon ve uygulama gösterim videosu aşağıda sunulmuştur. Bu belgeler, projenin teknik derinliğini ve gelişim sürecini daha ayrıntılı bir şekilde incelemek isteyenler için hazırlanmıştır.

* **Proje Makalesi:** Projenin teknik yaklaşımlarını, tasarım kararlarını ve implementasyon detaylarını açıklayan makalemize [buradan](./docs/makale.md) ulaşabilirsiniz.
* **Final Raporu:** Projenin genel değerlendirmesini, süreç detaylarını ve sonuçlarını içeren final raporumuza [buradan](./docs/final_raporu.md) ulaşabilirsiniz.
* **Demo Videosu:** Uygulamanın gerçek zamanlı çalışmasını, özelliklerini ve etkileşimini gösteren video için:
    * [YOUTUBE_VIDEO_LINKI]

## 📝 Çalışma Takvimi (Ara Rapor Özeti)

Proje süreci aşağıdaki ana adımları izlemiştir:

* **Hafta 1-2:** Proje gereksinimlerinin analizi, dilbilgisi seçimi ve Lexer tasarımı araştırması (Durum Diyagramları).
* **Hafta 3-4:** Lexer implementasyonu ve testleri, token tiplerinin belirlenmesi.
* **Hafta 5-6:** Parser tasarımı araştırması (Top-Down Parsing), C benzeri dilbilgisinin detaylandırılması.
* **Hafta 7-8:** Parser implementasyonu ve ilk sözdizimi kontrol testleri.
* **Hafta 9-10:** Tkinter GUI arayüzünün geliştirilmesi, temel metin editörü fonksiyonelliği.
* **Hafta 11-12:** Real-time vurgulama mekanizmasının entegrasyonu, tokenlara renk atamaları.
* **Hafta 13-14:** Akıllı düzenleme özelliklerinin (auto-indent, parantez tamamlama) eklenmesi, hata mesajı gösterimi.
* **Hafta 15:** Kapsamlı testler, hata ayıklama, performans iyileştirmeleri ve dokümantasyonun hazırlanması (makale, rapor, README).

## 🔮 Gelecek Çalışmalar

Bu projenin ileriki sürümlerinde eklenebilecek potansiyel geliştirmeler şunlardır:

* Daha kapsamlı bir C dilbilgisi desteği (örneğin: fonksiyon parametreleri, diziler, yapılar, enum'lar).
* Anlamsal analiz yeteneklerinin eklenmesi (değişkenlerin tanımlanıp tanımlanmadığını, tür uyumluluğunu kontrol etme).
* Gelişmiş hata kurtarma mekanizmaları, böylece tek bir hatada ayrıştırma durmaz ve daha fazla hata tespit edilebilir.
* Daha fazla IDE benzeri özellik (kod tamamlama, refactoring, kod navigasyonu).
* Farklı temalar için renk paleti seçenekleri.

---

## ✒️ Yazar

* **[Ahmet Güldaş]**


---
