# CyberLearn.io — Proje Raporu
**Öğrenci:** Ahmet İlter İnci  
**Ders:** BLG106 İnternet Programcılığı  
**Kurum:** Gazi Üniversitesi — TUSAŞ Kazan Meslek Yüksek Okulu   
**Canlı URL:** https://gazi-blg106-final.onrender.com  
**GitHub:** https://github.com/ahmetilterinci/Gazi_BLG106_Final
**Tanıtım Videosu:** 

### NOT: AI-Günlük docs dosyasının içerisindedir.

---

## 1. Projenin Amacı ve Ne İşe Yaradığı

CyberLearn.io, siber güvenlik eğitimini oyunlaştırma yöntemiyle sunan, yapay zeka destekli bir web öğrenme platformudur. Duolingo'nun bağımlılık yapıcı öğrenme modelinden ilham alınarak tasarlanan bu platform, kullanıcıların ağ güvenliği, kriptografi, etik hacking ve web güvenliği gibi konuları adım adım, sıralı bir "dünya sistemi" üzerinden öğrenmesine olanak tanır. Her ders tamamlandığında Gemini AI tarafından o derse özel sorular üretilir; çoktan seçmeli, doğru/yanlış, boşluk doldurma ve eşleştirme olmak üzere dört farklı soru tipiyle kullanıcının konuyu gerçekten kavrayıp kavramadığı ölçülür. Yanlış yapılan sorular sona eklenerek tümü doğru yanıtlanana kadar tekrar edilir.

---

## 2. Kullanılan Teknolojiler

Projenin backend'i **Flask 3.x** üzerine, application factory ve blueprint mimarisiyle inşa edilmiştir. Veritabanı katmanında **SQLAlchemy 2.x** (`Mapped`/`mapped_column` stili) ve **Flask-Migrate** kullanılmıştır. Kullanıcı kimlik doğrulaması **Flask-Login** ve Werkzeug şifre hash'leme ile sağlanmış; formlar **Flask-WTF** ile CSRF korumalı olarak yazılmıştır. Çok dilli destek için **Flask-Babel** entegre edilmiş, Türkçe ve İngilizce çeviriler eklenmiştir.

Frontend'de **Bootstrap 5.3** ve **Bootstrap Icons** kullanılmış; özel bir tasarım sistemi oluşturulmuştur. Renk tokenları (`--p:#6e5bff`, `--a:#00f5c4`), CSS değişkenleri ve karanlık/aydınlık tema desteği eklenmiştir. Syne, Inter ve JetBrains Mono font ailesi kullanılmıştır.

Yapay zeka entegrasyonu **Google Gemini 2.5 Flash** API'siyle sağlanmıştır. Üretim ortamı olarak **Render.com** tercih edilmiş, **PostgreSQL** veritabanı ile kalıcı veri depolama gerçekleştirilmiştir. Geliştirme süreci boyunca **Antigravity** (plan modu) ve **Claude** (danışman) birlikte kullanılmıştır.

---

## 3. AI Ajanıyla Çalışma Süreci

Proje geliştirilirken iki farklı AI aracı paralel kullanıldı: Antigravity (ajan modu) kod üretimi için, Claude (danışman modu) ise mimari kararlar, kod incelemesi ve sorun giderme için.

Geliştirme süreci Antigravity'nin plan modundan yararlanılarak yürütüldü. Her büyük özellik önce planlandı, plan incelendi, sorgulandı ve ancak onaylandıktan sonra kod üretimine geçildi. Örneğin Prompt 3'te ajan SQLAlchemy 1.x stili (`db.Column`) önerdi; 2.x stili (`Mapped`) istenince plan revize edildi. Prompt 4'te migration dosyasını silmek önerildi, bu kabul edilmedi ve elle yönetildi. Oturum 5'te `server_default` eksik olan bir migration dosyası, `flask db upgrade` çalıştırılmadan önce fark edilerek düzeltildi.

Büyük UI bileşenleri (index.html izometrik öğrenme yolu, quiz sistemi, profil sayfası) için doğrudan Claude ile çalışıldı. Bu bileşenler tek seferde değil, birden fazla turda olgunlaştırıldı ve her adımda test edildi.

Geliştirme boyunca "küçük adımlarla ilerleme" disiplinine uyuldu. Her tamamlanan özellik test edildi, commit atıldı, ardından bir sonraki adıma geçildi. Toplam 23 anlamlı commit oluşturuldu; commit mesajları hangi özelliğin eklendiğini ve hangi prompt'a karşılık geldiğini açıkça belirtiyor.

---

## 4. Karşılaşılan Zorluklar

**Deploy — Render ve SQLite:** İlk deploy denemelerinde SQLite kullanıldı. Ancak Render'ın ephemeral dosya sistemi nedeniyle her deploy'da veriler sıfırlandığı anlaşıldı. Çözüm olarak Render'ın ücretsiz PostgreSQL servisi eklendi. `render.yaml`'daki `fromDatabase` bloğu `DATABASE_URL`'yi otomatik inject etmedi; değişken dashboard'dan manuel girildi.

**Flask-Babel ve Jinja2 uyumsuzluğu:** `pybabel extract` sırasında `jinja2.ext.autoescape` ve `jinja2.ext.with_` extension'larının yeni Jinja2 sürümlerinde kaldırıldığı görüldü. `babel.cfg`'deki `extensions=` satırı tamamen silindi. Ayrıca `get_locale()` fonksiyonu Babel'e kayıtlıydı ancak Jinja2 şablonlarına inject edilmemişti; `@app.context_processor` ile çözüldü.

**Migration `server_default` eksikliği:** Mevcut verisi olan tablolara `nullable=False` kolon eklenirken `server_default` yazılmamıştı. Ajan bu detayı atladı; `flask db upgrade` öncesinde migration dosyası elle düzeltildi.

**Quiz arayüzü UX sorunu:** İlk quiz versiyonunda "Devam Et" butonu yanlış cevap durumunda görünmüyordu; `classList.add('show')` `display:none`'ı ezmiyordu. CSS'te `display:flex` olarak düzeltildi.

**CSS cascade sorunu:** Light tema değişkenleri `:root`'tan önce tanımlandığı için dark değerler tarafından eziliyordu. `:root` bloğu `[data-theme="light"]` bloğundan önce taşınarak çözüldü.

---

## 5. Öğrenilenler

Bu proje sürecinde en kalıcı öğrenme, **ajanı sorgulamadan onaylamamak** gerektiğiydi. SQLAlchemy versiyon farkı, migration `server_default` eksikliği ve Render deploy sorunları — bunların tümü plan aşamasında ya da kod incelemesinde fark edildi. Eğer ajan çıktıları doğrudan kabul edilseydi, bu hatalar çok daha geç ortaya çıkacak ve düzeltmesi çok daha maliyetli olacaktı.

Flask'ta `application factory` + `blueprint` mimarisinin gerçek değeri de bu süreçte anlaşıldı. Auth ve main modüllerini birbirinden bağımsız tutmak, hem test yazımını hem de özellik eklemeyi kolaylaştırdı. Her blueprint kendi rotalarını, formlarını ve şablonlarını yönetiyor; bu sayede bir modüldeki değişiklik diğerini etkilemiyor.

Gemini API ile çalışmak, prompt mühendisliği konusunda pratik deneyim kazandırdı. Soru üretimi için verilen prompt ne kadar spesifik ve örnekli yazılırsa, dönen JSON o kadar güvenilir ve tutarlı oluyor. Genel "soru üret" yerine her soru tipi için ayrı format tanımı ve örnek JSON şeması vermek, başarısız yanıt oranını önemli ölçüde düşürdü.

Flask-Babel entegrasyonu beklenenden karmaşık çıktı. Sadece `_()` fonksiyonu eklemek yetmiyor; `pybabel extract`, `init`, `compile` döngüsü, `context_processor` enjeksiyonu ve `locale_selector` — bunların hepsinin doğru sırayla kurulması gerekiyor. Ajanın bu konuda eski dokümantasyona dayandığı görüldü; güncel Flask + Jinja2 uyumluluğu için müdahale gerekti.

---

## 6. Özeleştiri

**E-posta şifre sıfırlama** (+5 puan) ve **tam metin arama** (+3 puan) bonusları zaman kısıtı ve konudaki çakışmalar nedeniyle tamamlanamadı. Özellikle şifre sıfırlama, kullanıcı deneyimi açısından önemli bir eksikliktir.

SQLite'tan PostgreSQL'e geçiş başarılı oldu, ancak bu geçiş proje planının başında değil ortasında yapıldı. Üretim ortamında ilişkisel veritabanı seçimi baştan yapılmalıydı. Bu gecikme birkaç commit ve sorun giderme sürecine neden oldu.

Gemini API hata yönetimi yeterli değil. API yanıt vermediğinde veya beklenmedik formatta JSON döndüğünde kullanıcıya belirsiz bir hata mesajı gösteriliyor. Daha güçlü bir fallback mekanizması eklenebilir.

---

## 7. Gelecek Planları

Teknik açıdan öncelik sırası şöyle olurdu: önce kapsamlı pytest suite'i, ardından e-posta doğrulama ve şifre sıfırlama, sonrasında tam metin arama (PostgreSQL `tsvector` ile). Daha uzun vadede kullanıcı liderlik tablosu, rozet sistemi ve gerçek CTF görevleri (Docker sandbox ortamında) eklenebilir.

Ürün perspektifinden bakıldığında, öğretici içeriklerin yalnızca admin tarafından değil topluluk katkısıyla da eklenebileceği bir yapı ilgi çekici olurdu. Gemini'nin kişiselleştirilmiş öğrenme yolu önerisi — kullanıcının yanlış yaptığı soru tiplerine göre adaptif zorluk ayarı — de güçlü bir özellik olarak öne çıkıyor.