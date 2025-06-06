# Gerçek Zamanlı Sözdizimi Vurgulayıcı: Kodunuzu Renklendirme Sanatı

## Giriş: Neden Koda Renk Katmalıyız?

Kod yazarken anında geri bildirim almak, geliştiricilerin hayatını kolaylaştıran en önemli özelliklerden biridir. Peki ya yazdığınız her satır, doğru sözdizimine sahipse anında renklense ve hatalar göze çarpsa? İşte bu makale, basit bir C benzeri dil için tam da bunu yapan, sıfırdan inşa edilmiş gerçek zamanlı bir sözdizimi vurgulayıcının perde arkasını aralıyor. Amacımız, harici kütüphanelere bağımlı kalmadan, kodun nasıl "anlaşıldığını" ve görselleştirildiğini göstermek.

## Projemizin Kalbi: Lexer ve Parser İkilisi

Uygulamamızın temeli, bir programlama dilinin sözdizimini analiz eden iki kritik bileşene dayanıyor: sözcük çözümleyici (lexer) ve sözdizimi çözümleyici (parser).

Özetle, süreç şöyle işler: Siz kodunuzu yazdıkça, lexer onu küçük, anlamlı parçalara (jetonlara) ayırır. Ardından parser, bu jetonları birleştirerek dilin kurallarına uygun bir yapı oluşturmaya çalışır. Herhangi bir kural dışılıkta, yani bir sözdizimi hatasında, uygulama size anında "Bu kısım doğru değil!" der. Her şey yolundaysa, kodunuz adeta bir tablo gibi renklendirilir!

## Kodu Çözmek: Lexer'ın Rolü

Lexer'ımızı, Durum Diyagramı ve Program Uygulaması yaklaşımını benimseyerek geliştirdik. Bu ne anlama geliyor? Her bir jeton tipini (anahtar kelimeler, değişken adları, sayılar, operatörler gibi) Python'ın güçlü `re` (düzenli ifadeler) modülüyle kendi kodumuzda eşleştirdik. Bu sayede, jetonlama süreci üzerinde tam kontrol sahibi olduk.

C benzeri dillerin Python gibi girintiye bağımlı olmadığını biliyoruz. Bu yüzden lexer'ımız, girintiler için özel jetonlar (`INDENT`, `DEDENT`) üretmez; boşluk ve yeni satırlar sadece görsel biçimlendirme amaçlıdır. Bu, uygulamanın C'nin doğal sözdizimine sadık kalmasını sağlar.

## Dilbilgisini Anlamak: Parser'ın Görevi

Lexer'dan gelen jetonlar, şimdi Yukarıdan Aşağıya (Top-Down) / Özyinelemeli İniş parser'ımızın eline geçer. Bu yöntem, dilbilgisi kurallarını (örneğin, bir `if` ifadesi, bir döngü) ayrı bir fonksiyonla temsil eder. Parser, jeton akışını adım adım tüketerek kodunuzun C benzeri dilbilgisine uygun olup olmadığını kontrol eder.

Şu anda desteklediğimiz dilbilgisi şunları içerir:

- **Koşullu İfadeler:** `if-else` yapıları (C stilinde `{}` blokları ile).
- **Döngüler:** `while` döngüleri.
- **Temel İfadeler:** `return` deyimleri, `int` ve `float` gibi değişken tanımlamaları, aritmetik ve karşılaştırma işlemleri.
- **İfade Sonlandırma:** Tüm ifadeler noktalı virgül (`;`) ile biter.

Eğer bir dilbilgisi hatası yakalanırsa, kullanıcıya anında bir `SyntaxError` mesajı iletilir. Parser, ayrıştırma sırasında boşluk ve yeni satır jetonlarını akıllıca atlar, çünkü bunlar C benzeri bir dilde dilbilgisel olarak anlamsızdır.

## Kodu Canlandırma: Sözdizimi Vurgulamanın Sihri

Gerçek zamanlı vurgulama, Tkinter'ın `Text` bileşeninin `tag_config` özelliği sayesinde mümkün oluyor. Bu özellik, metnin belirli bölümlerine renk ve font gibi stil etiketleri atamamızı sağlar. Uygulamamızda en az beşten fazla farklı jeton tipini vurguluyoruz:

- **Anahtar Kelimeler:** Mavi (örneğin: `if`, `while`)
- **Değişkenler/Fonksiyonlar:** Beyaz (örneğin: `sayac`, `main`)
- **Sayılar:** Koyu Turuncu (örneğin: `10`, `3.14`)
- **Metin Dizeleri:** Açık Yeşil (örneğin: `"Merhaba!"`)
- **Operatörler:** Kırmızı (örneğin: `+`, `=`, `==`)
- **Yorumlar:** Gri (örneğin: `// bu bir yorumdur`)
- **Ayraçlar:** Mor (örneğin: `(`, `{`, `;`)

Siz her tuşa bastığınızda, kodunuz yeniden analiz edilir ve vurgulama anında güncellenir. Bu, kod yazarken hataları hemen görmenizi ve doğru yazım şeklini kolayca takip etmenizi sağlar.

## Kullanıcı Deneyimi: Akıllı Editör Özellikleri

Python'ın Tkinter kütüphanesiyle inşa ettiğimiz GUI, koyu tema tasarımıyla modern bir görünüm sunuyor. Kod girişinin yapıldığı `tk.Text` alanı, temel bir metin düzenleyicinin tüm özelliklerini (`geri alma`, `kelime sarma`) barındırıyor. Ancak, kullanıcı deneyimini daha da zenginleştirmek için, popüler IDE'lerden ilham alan bazı akıllı özellikler ekledik:

- **Otomatik Girintileme:** Enter tuşuna bastığınızda, özellikle `{` karakterinden sonra, kodunuz otomatik olarak doğru girintiye kavuşur.
- **Girinti Geri Alma:** Backspace ile yanlış girintileri kolayca düzeltebilirsiniz.
- **Akıllı Parantez Tamamlama:** `{` tuşuna bastığınızda, uygulama otomatik olarak alt satırda girintili bir boşluk bırakıp kapanış `}` parantezini yerleştirir ve imlecinizi tam da kod yazmanız gereken yere konumlandırır. Bu özellik, blok yazımını hızlandırır ve parantez hatalarını azaltır.
- **Tutarlı Tab Boşlukları:** Tab tuşuna basıldığında her zaman 4 boşluk eklenir, böylece kodunuz her zaman düzenli görünür.

Sözdizimi hataları, GUI'nin alt kısmında canlı olarak kırmızı bir mesajla görüntülenir ve pencere boyutu değiştiğinde arayüz de duyarlı bir şekilde kendini ayarlar.

## Sonuç: Geleceğe Yönelik Bakış

Bu proje, gerçek zamanlı bir sözdizimi vurgulayıcının temel mimarisini ve C benzeri bir dil için nasıl sıfırdan inşa edilebileceğini başarıyla göstermiştir. Kendi lexer ve parser'ımızı geliştirmek, dilin kuralları üzerinde tam kontrol sağlamanın ve etkili bir görsel geri bildirim mekanizması oluşturmanın anahtarıydı.

Gelecekte, bu projeyi daha karmaşık C dil özelliklerini (fonksiyon parametreleri, diziler, yapılar gibi) içerecek şekilde genişletebilir, değişkenlerin türlerini kontrol eden anlamsal analiz yetenekleri ekleyebilir ve daha sofistike hata kurtarma algoritmaları entegre edebiliriz. Amacımız, bu temel üzerine inşa ederek, geliştiricilerin her zaman yanlarında olabilecek daha akıllı ve daha yetenekli bir kodlama arkadaşı yaratmaktır.
