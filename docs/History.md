# Proje Hafızası — CyberLearn AI
# Bu dosya danışman Claude'un hafızasıdır. Şablon yok, sadece bilgi var.

---

## PROJE KİMLİĞİ

- Ad: CyberLearn AI — Duolingo tarzı siber güvenlik öğrenme platformu
- Repo: https://github.com/ahmetilterinci/Gazi_BLG106_Final (public)
- Ders: Gazi Üniversitesi TUSAŞ Kazan MYO, BLG106 İnternet Programcılığı
- Bölüm: Bilişim Güvenliği
- Teslim: 01/06/2026 saat 13:00 — GitHub repo + GUZEM zip
- Geliştirme ortamı: Antigravity (zorunlu, -20 ceza var)
- AI modeli: Claude Sonnet 4.6 (Antigravity içinde)
- Danışman: Claude Sonnet 4.6 (bu sohbet)
- Proje yolu: C:\Users\LENOVO\Desktop\Gazi_BLG106_Final

---

## TEKNİK YAPI

### Stack
- Flask 3.x, SQLAlchemy 2.x (Mapped/mapped_column stili)
- Flask-Login, Flask-WTF (CSRF), Flask-Migrate (Alembic)
- SQLite (dev), geçiş planı: PostgreSQL (deploy)
- Bootstrap 5 değil — tamamen custom CSS (design system var)

### Design System
- Font: Syne (display/başlıklar) + Inter (body)
- Primary: --p: #6e5bff (mor)
- Accent: --a: #00f5c4 (yeşil)
- Diğer token'lar: --bg, --edge, --txt, --mono, --display
- Dark/light tema toggle base.html'de var
- Dil butonu base.html'de var (Flask-Babel Oturum 5'te aktif edilecek)
- Parçacık ağı canvas, cursor glow, noise texture, navbar scroll efekti
- cl-reveal / cl-reveal-left / cl-reveal-right (IntersectionObserver)

### Modeller (app/models.py)
- User: id, username, email, password_hash, created_at + UserMixin
- Topic: id, title, description, icon, order, user_id(FK→user.id, nullable)
- Lesson: id, title, content, difficulty(beginner/intermediate/advanced), order, topic_id(FK)
- UserProgress: id, user_id(FK), lesson_id(FK), is_completed, score, completed_at
  + UniqueConstraint(user_id, lesson_id)

### Migration Geçmişi
- f1abdb670357: initial schema (4 tablo)
- 294ba7f0547e: topic user_id eklendi (FK constraint adı: fk_topic_user_id)

### Blueprint Yapısı
- app/main/ → index, topics, lessons, CRUD rotaları
- app/auth/ → register, login, logout
- app/commands.py → flask seed-db CLI komutu (app/__init__.py'de register)

### Önemli Teknik Notlar
- datetime.now(timezone.utc) kullan — datetime.utcnow DEPRECATED
- Antigravity sandbox terminali C:\ sürücüsüne erişemiyor → terminal komutlarını Manuel çalıştır
- SQLite + Alembic batch_alter_table: FK constraint'e mutlaka isim ver (None geçme)
- Hata şablonlarında url_for kullanırken dikkat — olmayan route BuildError → 500'e düşer
- email-validator requirements.txt'te var
- Flask-Babel dil butonu base.html'de hazır, Oturum 5'te aktif edilecek

---

## COMMIT GEÇMİŞİ

| # | Mesaj |
|---|-------|
| 1 | Proje iskeleti kuruldu - Prompt 1-2 |
| 2 | Modeller ve migration eklendi - Prompt 3-4 |
| 3 | Auth akışı eklendi - Prompt 5 |
| 4 | UI yenileme - base ve index şablonları yeniden tasarlandı |
| 5 | login ve register şablonları yenilendi |
| 6 | 404 ve 500 hata sayfaları yenilendi |
| 7 | CRUD rotaları, şablonlar, pagination, UserProgress ve seed eklendi - Prompt 6 |

Hedef: 15+ anlamlı commit. Şu an: 7.

---

## TAMAMLANAN OTURUMLAR

### Oturum 1 — 23.05.2026 ✅
Prompt 1-5 tamamlandı.
- İskelet, README, modeller, migration, auth akışı
- Yakalanan hata: Ajan migration dosyasını silmeyi önerdi → reddedildi, dosya sağlıklıydı
- Yakalanan hata: datetime.utcnow yerine datetime.now(timezone.utc) kullandırıldı
- flask db stamp head hatası: "Target not up to date" → stamp head ile çözüldü

### Oturum 2 — 24.05.2026 ✅
Prompt 6 + UI yenileme tamamlandı.

**UI Yenileme:**
- Tüm şablonlar (base, index, login, register, 404, 500) design system ile yeniden yazıldı
- Google Stitch denendi → yetersiz, danışman Claude devraldı
- Bootstrap input-group + is-invalid bug riski tespit edilerek sıfırdan yazıldı
- 404 sayfası 500'e düşüyordu → url_for('main.topics') henüz yoktu → stub route eklendi

**Prompt 6 — CRUD:**
- Topic modelinde user_id olmadığı tespit edildi
  Ajan "sadece login_required" önerdi → reddedildi → migration yazıldı
  Neden: yönerge rubriğinde yetki kontrolü ayrı puan ölçütü
- commands.py'de seed konularına user_id atanmıyordu → User.query.first() ile düzeltildi
- commands.py'de SQL Injection ders içeriğinde Python tırnak syntax hatası → elle düzeltildi
- Alembic FK constraint isimsiz bırakıldı → ValueError → 'fk_topic_user_id' ismi verildi
- Ders tamamlama arayüzü "kendine puan ver" geldi → kabul edildi (AI quiz Oturum 3'te değiştirecek)

**Önemli not — kullanıcı gözlemi:**
Site şu an döküman okuma sitesi gibi görünüyor. Duolingo hissi yok.
Oturum 3'te AI quiz gelince lesson_detail.html tamamen değişecek:
- Markdown metin okuma → kısa içerik + AI sorusu
- "Kendine puan ver" → "Cevabı Gönder" → AI değerlendirsin

**Önemli not — admin panel:**
Kullanıcı admin panel istedi. Oturum sonunda söyledi, not aldım.
Admin panelde: kullanıcı yönetimi, konu/ders CRUD, site istatistikleri.
Şu anki user_id yetki kontrollerine admin bypass kolayca eklenebilir şekilde bırakıldı.
Admin panel hangi oturumda yapılacak henüz planlanmadı — bonus olarak değerlendir.

---

## AKTİF PLAN — KALAN OTURUMLAR

### Oturum 3 — 25.05.2026 — YARIN
**Prompt 7 — AI Quiz Özelliği**
- /lessons/<id>/quiz rotası
- Claude API ile o dersin konusuna özel soru üret (çoktan seçmeli veya açık uçlu)
- Kullanıcı cevap gönderir → Claude değerlendirir (doğru/yanlış + açıklama)
- Sonuç UserProgress.score'a işlenir
- lesson_detail.html tamamen yeniden yazılır
- Yeni paket: anthropic (pip install anthropic)
- .env'e ANTHROPIC_API_KEY eklenmeli
- YENİ MIGRATION GEREKEBİLİR: quiz_result veya question alanı eklenecekse

**Prompt 8 — Testler**
- tests/conftest.py: test client + in-memory SQLite fixture
- tests/test_auth.py: kayıt, giriş, çıkış
- tests/test_models.py: set_password/check_password
- tests/test_main.py: topics listesi, lesson detayı, UserProgress
- En az 5 test, her biri bağımsız

### Oturum 4 — 26.05.2026
**Prompt 9 — Docker + Deploy**
- Dockerfile (python:3.12-slim, gunicorn)
- docker-compose.yml (web + postgres)
- .dockerignore
- config.py: DATABASE_URL env desteği (sqlite dev / postgres prod)
- Procfile + runtime.txt (Render/Railway)
- Render veya Railway'e deploy → canlı URL
- README'ye deploy bölümü

### Oturum 5 — 27.05.2026 — Bonuslar Part 1
**Prompt 10 — API endpoint (+5 puan)**
- /api/v1/topics, /api/v1/topics/<id>, /api/v1/lessons/<id>
- JSON response, Flask-Login koruması

**Prompt 11 — Kullanıcı profili + avatar (+4 puan)**
- /profile rotası
- Avatar upload (static/avatars/)
- Profil düzenleme formu
- UserProgress özeti (tamamlanan ders, ortalama skor)

**Prompt 12 — Tam metin arama (+3 puan)**
- /search?q=... rotası
- Topic.title + Lesson.title + Lesson.content LIKE sorgusu
- Pagination

### Oturum 6 — 28.05.2026 — Bonuslar Part 2
**Prompt 13 — E-posta şifre sıfırlama (+5 puan)**
- Flask-Mail + itsdangerous token
- /forgot-password → /reset-password/<token>
- .env'e MAIL_* değişkenleri

**Prompt 14 — Flask-Babel TR/EN (+3 puan)**
- flask-babel kurulumu
- translations/ klasörü, TR ve EN
- Dil toggle zaten base.html'de hazır — sadece aktif et
- Kritik metinler _('...') ile sarılacak

**UI cilası + güvenlik gözden geçirme (Prompt 10 yönerge)**
- Tüm sayfalar mobil test
- CSRF, rate limit kontrol
- SECRET_KEY env'den mi geliyor? .env gitignore'da mı?

**Admin panel (eğer vakit kalırsa)**
- /admin/ blueprint
- Kullanıcı listesi, konu/ders yönetimi
- User modeline is_admin alanı ekle + migration

### Oturum 7 — 29-31.05.2026 — Teslim
- docs/rapor.md (800-1200 kelime, 7 madde)
- ai-gunlugu.md son güncelleme (7+ oturum, 5+ ekran görüntüsü)
- Demo videosu (3-5 dk, Drive/YouTube, README'ye link)
- Son kontroller: 15+ commit?, .env gitignore'da?, canlı URL?, docker build?

---

## BONUS PUAN TAKİBİ

| Bonus | Puan | Oturum | Durum |
|-------|------|--------|-------|
| E-posta şifre sıfırlama | +5 | 6 | ⏳ |
| API endpoint /api/v1/ | +5 | 5 | ⏳ |
| Kullanıcı profili + avatar | +4 | 5 | ⏳ |
| Flask-Babel TR/EN | +3 | 6 | ⏳ |
| Tam metin arama | +3 | 5 | ⏳ |
| Admin panel | ? | 6 | 📝 istendi |
| **TOPLAM** | **+20** | | |

---

## ZORUNLU GEREKSİNİM TAKİBİ

| # | Gereksinim | Durum |
|---|-----------|-------|
| 1 | Application factory + blueprint | ✅ |
| 2 | 4+ sayfa, base template, inheritance | ✅ |
| 3 | Flask-WTF, 2+ form, CSRF | ✅ |
| 4 | SQLAlchemy, 3+ model, ilişkiler | ✅ |
| 5 | Flask-Migrate, migration dosyaları | ✅ |
| 6 | Flask-Login, kayıt/giriş/çıkış, hash | ✅ |
| 7 | 404/500 hata sayfaları | ✅ |
| 8 | Pagination | ✅ |
| 9 | Bootstrap/Tailwind, mobil uyumlu | ✅ (custom CSS) |
| 10 | Docker veya canlı deploy | ⏳ Oturum 4 |

---

## ÇALIŞMA KURALLARI (benim için notlar)

- Her oturum başında History.md oku — bu benim hafızam
- Antigravity planı gelince ONAYLAMADAN önce incele, sorun varsa söyle
- Terminal komutlarını Antigravity çalıştıramıyor → kullanıcı manuel çalıştırıyor
- Her oturum sonu: AI günlüğü yaz + History güncelle + yeni sohbet hatırlat
- Commit kuralı: git add . → git commit -m "..." → git push
- datetime.utcnow YASAK — datetime.now(timezone.utc) kullan
- SQLAlchemy 1.x stili YASAK — Mapped, mapped_column kullan
- Yeni migration yazılırken FK constraint'e mutlaka isim ver
- Stub route varsa "genişlet" de "sıfırdan oluştur" deme

---

## TESLIM KONTROLLERİ (01/06 öncesi)

- [ ] 15+ anlamlı commit (şu an 7)
- [ ] .env asla commit'lenmemiş
- [ ] Canlı URL çalışıyor veya docker-compose up çalışıyor
- [ ] /docs/ai-gunlugu.md 7+ oturum, 5+ ekran görüntüsü
- [ ] /docs/rapor.md 800-1200 kelime, 7 madde
- [ ] Demo videosu Drive/YouTube, README'de link
- [ ] GitHub repo public
- [ ] GUZEM'e zip yüklendi