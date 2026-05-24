# Proje Geliştirme Geçmişi & Kalan Plan

> Bu dosya danışman Claude'un hafızasıdır. Her oturum sonunda güncellenir.
> ai-gunlugu.md formatına bağlı değil — sadece "ne yapıldı, ne kaldı, dikkat edilecekler" odaklı.

---

## GENEL DURUM (24.05.2026 itibarıyla)

- Commit sayısı: 6 (hedef: 15+)
- Teslim tarihi: 01.06.2026 saat 13:00
- GitHub: https://github.com/ahmetilterinci/Gazi_BLG106_Final (public)
- Geliştirme ortamı: Antigravity (zorunlu)
- AI modeli: Claude Sonnet 4.6

---

## TAMAMLANAN ADIMLAR

### Oturum 1 — 23.05.2026 ✅

**Prompt 1 — Proje iskeleti**
- Application factory + blueprint yapısı (app/main, app/auth)
- config.py: DevelopmentConfig / ProductionConfig
- requirements.txt: flask, flask-sqlalchemy, flask-migrate, flask-login, flask-wtf, python-dotenv, email-validator
- .env.example, .gitignore, run.py, docs/ai-gunlugu.md

**Prompt 2 — README.md**
- Türkçe, projeye özel dokümantasyon

**Prompt 3 — Modeller**
- User, Topic, Lesson, UserProgress — SQLAlchemy 2.x stili (Mapped, mapped_column)
- datetime.now(timezone.utc) kullanıldı (deprecation önlendi)
- UniqueConstraint(user_id, lesson_id) eklendi
- back_populates ile çift taraflı ilişkiler

**Prompt 4 — Migration**
- flask db init → stamp head → migrate → upgrade
- ⚠️ Ajan migration dosyasını silmeyi önerdi, reddedildi — dosya sağlıklıydı

**Prompt 5 — Auth akışı**
- RegisterForm + LoginForm (Flask-WTF, CSRF korumalı)
- /register, /login, /logout rotaları
- Flask-Login: login_manager, user_loader, login_view
- 404/500 hata handler'ları (@main.app_errorhandler)
- templates: base.html, auth/register.html, auth/login.html, main/index.html, errors/404.html, errors/500.html

Commit geçmişi:
- Commit 1: Proje iskeleti kuruldu - Prompt 1-2
- Commit 2: Modeller ve migration eklendi - Prompt 3-4
- Commit 3: Auth akışı eklendi - Prompt 5

---

### Oturum 2 — 24.05.2026 (devam ediyor)

**UI Yenileme — base.html + index.html (Danışman Claude)**
- Google Stitch denendi, yetersiz bulundu, danışman Claude devraldı
- Font: Syne (display) + Inter (body)
- Design token'lar: --p: #6e5bff, --a: #00f5c4
- Hero: clamp(2.8rem, 6.5vw, 5rem), gradient, orbs (700px/80px blur)
- Parçacık ağı canvas, cursor glow, noise texture, navbar scroll efekti
- cl-reveal / cl-reveal-left / cl-reveal-right (IntersectionObserver)
- Tema toggle (dark/light), Dil butonu (Flask-Babel Gün 5'e hazır)
- 6 section: Hero → Özellikler → Nasıl Çalışır → Dersler Preview → Stats → CTA

**UI Yenileme — login.html + register.html (Danışman Claude)**
- Eski dosyalarda 5 sorun tespit edildi (token uyumsuzluğu, Bootstrap input-group bug riski vb.)
- Sıfırdan, design system ile tam uyumlu yazıldı
- Register: şifre güç göstergesi (JS), submit loading state, güvenlik rozeti

**UI Yenileme — 404.html + 500.html (Danışman Claude)**
- Glitch animasyonlu, orb arka planlı, design system uyumlu
- ⚠️ Bug: url_for('main.topics') BuildError → 500'e düşüyordu
  Çözüm: stub /topics route + placeholder topics.html eklendi (Antigravity)
- Öğrenilen: hata sayfaları içindeki url_for çağrıları da render anında çalışır,
  olmayan route'a bağlantı verme

Commit geçmişi:
- Commit 4: UI yenileme - base ve index şablonları yeniden tasarlandı
- Commit 5: login ve register şablonları yenilendi
- Commit 6: 404 ve 500 hata sayfaları yenilendi

---

## KALAN PLAN (7 oturum = 7 gün hedefi)

### Oturum 2 — Bugün (devam) — YAPILACAK

**Prompt 6 — CRUD rotaları + şablonlar + pagination + UserProgress**
- app/main/routes.py içine:
  - GET /topics — paginate edilmiş konu listesi (sayfa başı 10)
  - GET /topics/<id> — konu detayı + ders listesi
  - GET /lessons/<id> — ders içeriği
  - GET,POST /lessons/<id>/complete — ders tamamlama (UserProgress oluştur/güncelle)
  - GET,POST /topics/new — yeni konu (login_required, admin)
  - GET,POST /topics/<id>/edit — düzenleme (sadece sahibi)
  - POST /topics/<id>/delete — silme (sadece sahibi)
- Şablonlar: topics.html, topic_detail.html, lesson_detail.html
- UserProgress kaydı: is_completed=True, score, completed_at (insert or update)
- Antigravity'ye verirken şunu belirt: "stub /topics route zaten var, onu genişlet"
- Hedef commit: "CRUD rotaları, şablonlar, pagination ve ilerleme takibi eklendi - Prompt 6"

---

### Oturum 3 — 25.05.2026

**Prompt 7 — AI özelliği**
- /lessons/<id>/quiz rotası: Claude API ile o dersin konusuna özel soru üret
- Kullanıcı cevap gönderir, Claude değerlendirir (doğru/yanlış + açıklama)
- Sonuç UserProgress.score'a işlenir
- Yeni paket: anthropic veya requests (API çağrısı için)
- Yeni migration gerekebilir (quiz_score alanı eklenecekse)
- Hedef commit: "AI destekli quiz özelliği eklendi - Prompt 7"

**Prompt 8 — Testler**
- tests/ klasörüne pytest ile en az 5 test:
  - Auth rotaları (kayıt, giriş, çıkış)
  - Topic/Lesson CRUD
  - UserProgress kaydı
  - 404 sayfası
- Hedef commit: "Birim testleri eklendi - Prompt 8"

---

### Oturum 4 — 26.05.2026

**Prompt 9 — Docker + Deploy**
- Dockerfile + docker-compose.yml
- config.py: DATABASE_URL env desteği (SQLite dev / PostgreSQL prod)
- Procfile + runtime.txt (Render/Railway için)
- Render veya Railway'e deploy, canlı URL alınır
- README'ye deploy bölümü eklenir
- Hedef commit: "Docker ve deploy yapılandırması eklendi - Prompt 9"

---

### Oturum 5 — 27.05.2026 — Bonuslar Part 1

**Prompt 10 — API endpoint (+5 puan)**
- /api/v1/topics — JSON liste
- /api/v1/topics/<id> — JSON detay
- /api/v1/lessons/<id> — JSON ders
- Flask-Login token veya session koruması

**Prompt 11 — Kullanıcı profili + avatar (+4 puan)**
- /profile rotası
- Avatar upload (Werkzeug, static/avatars/)
- Profil düzenleme formu (username, bio)
- UserProgress özeti: tamamlanan ders sayısı, ortalama skor

**Prompt 12 — Tam metin arama (+3 puan)**
- /search?q=... rotası
- Topic.title + Lesson.title + Lesson.content üzerinde LIKE sorgusu
- Arama sonuçları sayfası (pagination)

Hedef commit: "API endpoint, profil ve arama özellikleri eklendi - Prompt 10-12"

---

### Oturum 6 — 28.05.2026 — Bonuslar Part 2 + UI Cilası

**Prompt 13 — E-posta şifre sıfırlama (+5 puan)**
- Flask-Mail + itsdangerous token
- /forgot-password → e-posta gönder
- /reset-password/<token> → yeni şifre
- .env'e MAIL_* değişkenleri

**Prompt 14 — Flask-Babel TR/EN (+3 puan)**
- flask-babel kurulumu
- translations/ klasörü, TR ve EN
- Dil toggle (base.html'deki buton zaten hazır)
- Kritik metinlerin _('...') ile sarılması

**UI cilası + güvenlik gözden geçirme**
- Tüm sayfalar mobil test
- CSRF, rate limit kontrol
- Açık kalmış TODO'lar temizlenir

Hedef commit: "E-posta şifre sıfırlama ve Flask-Babel TR/EN eklendi - Prompt 13-14"

---

### Oturum 7 — 29-31.05.2026 — Teslim Hazırlığı

**rapor.md yazılır** (800-1200 kelime, docs/ altına)
- Projenin amacı
- Mimari kararlar
- AI aracının katkısı ve sınırlılıkları
- Karşılaşılan zorluklar
- Öz değerlendirme

**ai-gunlugu.md son güncelleme**
- Tüm oturumlar eksiksiz
- En az 5 ekran görüntüsü (docs/img/)
- En az 2 prompt-yanıt alıntısı (ajan yanlış önerdi, düzeltildi örnekleri zaten var)

**Demo videosu** (3-5 dk, Drive/YouTube)
- Kayıt → Giriş → Topic listesi → Lesson → Quiz → Profil → Arama
- README'ye link eklenir

**Son kontroller**
- En az 15 anlamlı commit var mı?
- Tüm .env değerleri .gitignore'da mı?
- Canlı URL çalışıyor mu?
- Docker build sorunsuz mu?

Hedef commit: "Rapor, demo ve son düzenlemeler - teslim hazır"

---

## TEKNİK NOTLAR (Unutulmaması Gerekenler)

- Antigravity terminali C:\ sürücüsüne erişemiyor — terminal komutlarını manuel çalıştır
- stub /topics route var, Prompt 6'da "genişlet" de "sıfırdan oluştur" deme
- email-validator requirements.txt'te var, tekrar ekleme
- Flask-Babel dil butonu base.html'e zaten konuldu, Oturum 5'te aktif edilecek
- UserProgress UniqueConstraint var: aynı user+lesson için insert değil update yap
- datetime.now(timezone.utc) kullan — datetime.utcnow deprecated

## BONUS PUAN TABLOSU

| Bonus | Puan | Oturum |
|-------|------|--------|
| E-posta şifre sıfırlama | +5 | 6 |
| API endpoint /api/v1/ | +5 | 5 |
| Kullanıcı profili + avatar | +4 | 5 |
| Flask-Babel TR/EN | +3 | 6 |
| Tam metin arama | +3 | 5 |
| **TOPLAM** | **+20** | |

## ZORUNLU GEREKSİNİM TAKİBİ

| Gereksinim | Durum |
|-----------|-------|
| Application factory + blueprint | ✅ |
| En az 4 sayfa | ⏳ (Prompt 6'da tamamlanır) |
| base template + inheritance | ✅ |
| Flask-WTF, 2 form, CSRF | ✅ |
| SQLAlchemy, 3+ model, ilişkiler | ✅ |
| Flask-Migrate + migration dosyaları | ✅ |
| Flask-Login, kayıt/giriş/çıkış, hash | ✅ |
| 404/500 hata sayfaları | ✅ |
| Pagination | ⏳ (Prompt 6) |
| Bootstrap/Tailwind, mobil uyumlu | ✅ |
| Docker veya canlı deploy | ⏳ (Oturum 4) |