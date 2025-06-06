# Proje Final Raporu

## 1. Giriş

Bu proje, basit bir C benzeri dil için gerçek zamanlı sözdizimi vurgulayıcıya sahip bir Masaüstü Uygulaması (GUI) geliştirmeyi amaçlamaktadır. Uygulama, sözcük analizi ve sözdizimi analizi süreçlerini kullanarak kodun dilbilgisel doğruluğunu kontrol eder ve jetonları görsel olarak vurgular. Bu yaklaşım, geliştiricilerin kod yazarken anında geri bildirim almasını sağlayarak hataları erken aşamada tespit etmelerine yardımcı olur.

---

## 2. Programlama Dili ve Geliştirme Ortamı

Proje, hızlı prototipleme ve kolay GUI geliştirme imkanları sunan **Python** dili ve **Tkinter** kütüphanesi kullanılarak geliştirilmiştir. Python'ın esnek yapısı ve geniş kütüphane ekosistemi, projenin temel derleyici bileşenlerinin (`Lexer` ve `Parser`) sıfırdan ve harici bir kütüphane bağımlılığı olmadan oluşturulmasına olanak tanımıştır.

---

## 3. Sözdizimi Analizi Süreci

Sözdizimi analizi, kullanıcının girdiği ham kodu önce **Sözcük Çözümleyici (Lexer)** ile jetonlara ayırır. Lexer, dilin anlamlı en küçük birimlerini (anahtar kelimeler, tanımlayıcılar, operatörler vb.) tanır. 

Ardından bu jeton akışı, **Sözdizimi Çözümleyici (Parser)** tarafından tanımlı C benzeri dilbilgisine göre ayrıştırılır. Herhangi bir dilbilgisel hata durumunda `SyntaxError` fırlatılır ve kullanıcıya bildirilir. Başarılı ayrıştırma veya kısmi vurgulama gerektiğinde, jetonlar GUI üzerinde önceden belirlenmiş renklerle renklendirilerek gösterilir.

---

## 4. Sözcük Analizi Detayları (Lexical Analysis)

Lexer, **Durum Diyagramı** ve **Program Uygulaması** yaklaşımıyla, Python'ın yerleşik `re` (düzenli ifadeler) modülü kullanılarak geliştirilmiştir. Bu yapı sayesinde jetonlama süreci üzerinde tam kontrol sağlanmış ve dilin özel gereksinimleri (tam kelime eşleşmesi gibi) verimli biçimde yönetilmiştir.

`tokens.py` dosyasında tanımlanan düzenli ifadelerle aşağıdaki jeton türleri tanınır:

- **Anahtar Kelimeler**
- **Tanımlayıcılar**
- **Sayılar**
- **Operatörler**
- **Yorumlar**
- **Ayraçlar**
- **Boşluklar**
- **Yeni Satırlar**

> C benzeri dilin girintiye dayalı olmaması nedeniyle `INDENT` ve `DEDENT` jetonları üretilmez. Bu, lexer'ın C dilinin yapısına daha uygun hale gelmesini sağlar.

---

## 5. Ayrıştırma Metodolojisi (Parsing Methodology)

Parser, **Yukarıdan Aşağıya (Top-Down)** / **Özyinelemeli İniş (Recursive Descent)** yaklaşımıyla uygulanmıştır. Her dilbilgisi kuralı ayrı bir Python fonksiyonu ile temsil edilerek, kodun okunabilirliği ve sürdürülebilirliği artırılmıştır.

### Desteklenen Dilbilgisi Özellikleri:

- `if-else` yapıları (örneğin: `if (x > 0) { return 1; } else { return 0; }`)
- `while` döngüleri
- `return` ifadeleri
- `int`, `float` gibi değişken tanımları
- Aritmetik ve karşılaştırma işlemleri
- Noktalı virgül (`;`) ile sonlanan ifadeler

### Hata Yakalama:

Dilbilgisi kurallarına uyulmadığında `SyntaxError` fırlatılarak kullanıcıya anında geri bildirim sağlanır. Parser yalnızca anlamlı jetonlara odaklanır, boşluk ve yeni satır jetonlarını atlar.

---

## 6. Vurgulama Şeması (Highlighting Scheme)

Gerçek zamanlı vurgulama, **Tkinter**'ın `Text` widget'ı üzerinden `tag_config` özelliği ile sağlanır. Her jeton türü, belirli bir renkle vurgulanarak kullanıcıya görsel olarak sunulur:

| Jeton Türü   | Renk        | Örnekler                           |
|--------------|-------------|------------------------------------|
| `KEYWORD`    | Mavi        | `if`, `while`, `int`              |
| `IDENTIFIER` | Beyaz       | `myVariable`, `calculateSum`     |
| `NUMBER`     | Koyu Turuncu| `123`, `3.14`                     |
| `STRING`     | Açık Yeşil  | `"hello world"`                   |
| `OPERATOR`   | Kırmızı     | `+`, `=`, `==`                    |
| `COMMENT`    | Gri         | `// yorum satırı`                |
| `DELIMITER`  | Mor         | `(`, `)`, `{`, `}`, `;`           |

Her **tuş bırakma (KeyRelease)** olayında, kod tekrar analiz edilip renklendirme güncellenir. Bu sayede geliştiriciler, sözdizimi hatalarını anında görebilir.

---

### 7. GUI Uygulaması (GUI Implementation)

Kullanıcı arayüzü **Tkinter** ile geliştirilmiştir ve modern bir koyu tema kullanır.

- **`tk.Text` Widget:**  
  Kod girişi ve vurgulama için merkezi bileşendir. `undo` özelliği ve kelime sarma (`wrap="word"`) gibi standart metin düzenleyici fonksiyonlarını içerir.

- **Gerçek Zamanlı Güncelleme:**  
  Metin alanındaki her `KeyRelease` olayı, kodun yeniden lexer ve parser'dan geçirilmesini tetikleyerek anlık sözdizimi vurgulamasını sağlar.

- **Gelişmiş Düzenleme Özellikleri:**
  - **Enter tuşuna basıldığında otomatik girintileme:**  
    Özellikle `{` karakterinden sonra Enter'a basıldığında, kodun okunabilirliğini artıran doğru girintili yeni bir satır oluşturur.
  - **Backspace ile girintileri geri alma:**  
    Kullanıcının yanlış girintileri kolayca düzeltmesine imkân tanır.
  - **`{` tuşuna basıldığında otomatik parantez tamamlama:**  
    `{ \n\t\n }` yapısını otomatik olarak oluşturur ve imleci içerideki boşluğa konumlandırır. Bu, blok tanımlamayı hızlandırır ve yazım hatalarını azaltır.
  - **Tab tuşuna basıldığında 4 boşluk ekleme:**  
    Konsol tab'ı yerine tutarlı boşluk kullanımı sağlar.

- **Hata Mesajı:**  
  Sözdizimi hatalarını canlı olarak, kırmızı metinle GUI'nin altında göstererek kullanıcının sorunu hızlıca görmesini sağlar.

- **Duyarlı Tasarım:**  
  Pencere boyutlandırıldığında metin alanı da dinamik olarak boyutlanır. Bu, farklı ekran çözünürlüklerinde tutarlı bir kullanıcı deneyimi sunar.

---

### 8. Sonuç ve Gelecek Çalışmalar

Bu proje, gerçek zamanlı bir sözdizimi vurgulayıcının temel prensiplerini ve C benzeri bir dil için uygulamasını başarıyla göstermiştir. **Lexical analiz** ve **Top-Down parsing** yaklaşımları kullanılarak sağlam bir dilbilgisel kontrol, etkili görsel geri bildirim ve IDE benzeri yazım kolaylıkları sunulmuştur.

Gelecek çalışmalar kapsamında:

- Daha kapsamlı bir dilbilgisi desteği (örneğin: fonksiyon parametreleri, diziler),
- Anlamsal analiz (örneğin: değişken türü kontrolü),
- Gelişmiş hata kurtarma mekanizmaları,
- Kullanıcı arayüzüne yeni özellikler (örneğin: satır numaraları, arama/değiştirme)

eklenmesi planlanmaktadır.

Projenin modüler yapısı, gelecekteki geliştirmeler için güçlü bir temel sunmaktadır.

