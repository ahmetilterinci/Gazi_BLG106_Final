# Proje Geliştirme Geçmişi

## Oturum 1 — 23 Mayıs 2026 ✅ TAMAMLANDI

### Tamamlanan Adımlar

**Prompt 1 — Proje iskeleti (Antigravity)**
- Application factory pattern + blueprint yapısı kuruldu
- app/auth/ ve app/main/ blueprint'leri oluşturuldu
- config.py içinde DevelopmentConfig / ProductionConfig tanımlandı
- requirements.txt: flask, flask-sqlalchemy, flask-migrate, flask-login, flask-wtf, python-dotenv
- .env.example, .gitignore (.env korumalı), run.py oluşturuldu
- docs/ai-gunlugu.md boş şablonla oluşturuldu

**Prompt 2 — README.md (Antigravity)**
- Projeye özel Türkçe README yazıldı
- Kurulum adımları, geliştirme komutları, teknoloji listesi eklendi

**Ortam kurulumu (manuel)**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -c "from app import create_app; app = create_app(); print('✅ OK')"
```

**GitHub bağlantısı (manuel)**
- Repo: https://github.com/ahmetilterinci/Gazi_BLG106_Final (public)
- İlk commit: "Proje iskeleti kuruldu - Prompt 1-2"
- README merge conflict çözüldü

**Prompt 3 — Modeller (Antigravity)**
- app/models.py içine 4 model yazıldı: User, Topic, Lesson, UserProgress
- SQLAlchemy 2.x stili kullanıldı (Mapped, mapped_column)
- User modeli UserMixin'i kalıtıyor, set_password/check_password metodları var
- UniqueConstraint(user_id, lesson_id) UserProgress'e eklendi
- created_at için datetime.now(timezone.utc) kullanıldı (deprecation önlendi)
- back_populates ile tüm ilişkiler çift taraflı tanımlandı
- Import testi başarılı: "Import OK" çıktısı alındı

**Prompt 4 — Migration (Antigravity + manuel terminal)**
- flask db init: migrations/ klasörü kuruldu
- flask db stamp head: "Target database is not up to date" hatasını aşmak için
- flask db migrate: 4 tablo algılandı (topic, user, lesson, user_progress)
- ⚠️ Ajan migration dosyasını silmeyi önerdi — dosya incelendi, sağlıklıydı, öneri reddedildi
- flask db upgrade: tablolar SQLite'a yazıldı

**Prompt 5 — Auth akışı (Antigravity)**
- email-validator paketi requirements.txt'e eklendi
- app/__init__.py: login_view, login_message, user_loader eklendi
- app/auth/forms.py: RegisterForm + LoginForm (Flask-WTF, CSRF korumalı)
- app/auth/routes.py: /register, /login, /logout rotaları (Türkçe flash mesajları)
- app/main/routes.py: index rotası + 404/500 hata handler'ları (@main.app_errorhandler)
- templates/base.html: Bootstrap 5 navbar, koşullu login/logout linkleri
- templates/auth/register.html + login.html
- templates/main/index.html
- templates/errors/404.html + 500.html
- ⚠️ Flash mesajı kapatma butonu çalışmıyor — HTML/CSS yenilenince düzelecek
- Test sonuçları: index ✅, 404 sayfası ✅, kayıt ✅, giriş ✅, yönlendirmeler ✅

### Commit Geçmişi
| # | Hash | Mesaj |
|---|------|-------|
| 1 | 5e62f8d | Proje iskeleti kuruldu - Prompt 1-2 |
| 2 | 61f183a | Modeller ve migration eklendi - Prompt 3-4 |
| 3 | — | Auth akışı eklendi - Prompt 5 |

---

## Oturum 2 — 24.05.2026 ✅ TAMAMLANDI

### Tamamlanan Adımlar

**UI Yenileme V2 — base.html + index.html (Danışman Claude)**
- CSS bug düzeltildi: `{% block extra_css %}` Jinja2 tag'leri `</style>` içindeydi, dışına alındı
- Font sistemi güncellendi: Space Grotesk → **Syne** (display) + **Inter** (body)
- Design token'lar yenilendi: `#786fff` → `#6e5bff`, accent `#00e5b8` → `#00f5c4`
- Hero başlık, gradient, orb boyutları büyütüldü
- 6 section: Hero → Özellikler → Nasıl Çalışır → Dersler Preview → Stats → CTA

**login.html + register.html (Danışman Claude)**
- Eski dosyalarda design token uyumsuzluğu ve Bootstrap bug riski tespit edildi
- Her iki dosya sıfırdan, base.html design system ile tam uyumlu yazıldı
- Register'a şifre güç göstergesi + submit loading state eklendi

**404.html + 500.html (Danışman Claude)**
- Her iki sayfa design system'e uygun sıfırdan yazıldı
- ⚠️ Bug: url_for('main.topics') BuildError → stub /topics route + placeholder topics.html eklendi

**Prompt 6 — CRUD Rotaları + Şablonlar + Pagination (Antigravity)**
- app/main/routes.py: topics, topic_detail, topic_new, topic_edit, topic_delete_confirm
- app/main/routes.py: lesson_detail, lesson_new, lesson_complete rotaları
- app/main/forms.py: TopicForm + LessonForm
- templates/main/: topics.html, topic_detail.html, topic_form.html
- templates/main/: lesson_detail.html, lesson_form.html, confirm_delete.html
- Pagination: topics listesinde sayfa başı 10
- Tüm şablonlar design system ile uyumlu

**Seed Sistemi — app/commands.py (Antigravity)**
- flask seed-db CLI komutu eklendi
- İdempotent davranır (veri varsa atlar)
- 3 konu, 9 ders: Ağ Güvenliği, Şifreleme Temelleri, Web Güvenliği
- Gerçek siber güvenlik içerikleri (OSI, Firewall, TCP/IP, AES, Hash, PKI, OWASP, SQLi, XSS)
- app/__init__.py'e komut kaydedildi

### Mevcut Durum (Oturum 2 sonu)
- Tüm CRUD sayfaları çalışıyor
- Seed verisi mevcut: 3 konu, 9 ders
- lesson_detail.html: "döküman oku + kendine puan ver" sistemi — HENÜZ DEĞİŞTİRİLMEDİ
- .env içeriği:
  ```
  FLASK_APP=run.py
  FLASK_ENV=development
  SECRET_KEY=...
  DATABASE_URL=sqlite:///cyberlearn.db
  GEMINI_API_KEY=...  ← bu oturumda eklendi
  ```

### Commit Geçmişi (Oturum 2)
| # | Mesaj |
|---|-------|
| 4 | UI yenileme - base ve index şablonları yeniden tasarlandı |
| 5 | login ve register şablonları yenilendi |
| 6 | 404 ve 500 hata sayfaları yenilendi |
| 7 | CRUD rotaları ve şablonlar eklendi - Prompt 6 |
| 8 | Seed sistemi eklendi - commands.py |

---

## Oturum 3 — 27.05.2026 ✅ KISMEN TAMAMLANDI

### Hedef
Projeyi "döküman okuma sitesi"nden Duolingo tarzı AI destekli öğrenme platformuna dönüştürmek.

### Tamamlanan Adımlar

**Prompt A — Gemini AI Quiz Backend (Antigravity + Danışman Claude)**

Yapılan değişiklikler:
- requirements.txt'e `google-generativeai` eklendi
- app/main/routes.py'e `POST /lessons/<int:id>/quiz` rotası eklendi:
  - `@csrf.exempt` + `@login_required`
  - Gemini `gemini-2.5-flash` modeli kullanılıyor
  - System prompt ile JSON formatında çoktan seçmeli soru üretiliyor
  - response.text'ten ```json bloğu temizlenerek parse ediliyor
- app/main/routes.py'deki `lesson_complete` rotası güncellendi:
  - `ai_score` parametresi öncelikli, yoksa manuel `score` kullanılıyor
- app/__init__.py'den `csrf` nesnesi import edildi

⚠️ Yakalanan Sorunlar ve Çözümler:
- Gemini bazen yanıtı ```json bloğuna sarıyor → `removeprefix/removesuffix` ile temizlendi
- CSRF token fetch'ten undefined geliyordu → `@csrf.exempt` ile çözüldü
- Test sırasında login olmadan istek → 400 değil redirect geliyordu, login yapılınca çözüldü

✅ Test Sonucu:
```javascript
fetch('/lessons/1/quiz', {method:'POST',...}).then(r=>r.json()).then(console.log)
// Dönen örnek:
{
  question: "OSI modelinin yedi katmanından biri DEĞİLDİR?",
  options: ["A) Donanım Katmanı", "B) Fiziksel Katman", ...],
  correct_index: 0,
  explanation: "Ders içeriğinde belirtildiği üzere..."
}
```
Backend çalışıyor ✅

### Sıradaki Adım — Prompt B (YENİ SOHBETTE YAPILACAK)

**Prompt B — lesson_detail.html Duolingo Tarzı Yenileme**

Mevcut sorun: lesson_detail.html'de kullanıcı içeriği okuyup kendine manuel puan veriyor.
Hedef: Tam Duolingo deneyimi.

Yeni akış:
1. Kullanıcı derse girer → ders içeriğini okur (üstte)
2. "Quiz'i Başlat" butonuna basar
3. JS → `POST /lessons/<id>/quiz` → Gemini'den soru gelir
4. 4 şıklı soru kartı animasyonlu gösterilir
5. Kullanıcı şıkka tıklar → doğru=yeşil/yanlış=kırmızı animasyon
6. Explanation gösterilir
7. "Tamamla" butonu → `POST /lessons/<id>/complete` → ai_score ile (doğru=100, yanlış=40)
8. UserProgress güncellenir

Antigravity'ye verilecek prompt:
```
Bağlam: Flask 3.x, templates/main/lesson_detail.html mevcut.
POST /lessons/<id>/quiz endpoint'i çalışıyor, JSON döndürüyor:
{question, options: [...], correct_index, explanation}
POST /lessons/<id>/complete endpoint'i ai_score parametresi kabul ediyor.

Hedef: lesson_detail.html'i Duolingo tarzı quiz deneyimine dönüştür.
Mevcut "Dersi Tamamla / kendine puan ver" formu tamamen kaldırılacak.

Yeni düzen:
1. Üst kısım: Ders içeriği (mevcut lesson-content bloğu korunacak)
2. Alt kısım: Quiz bölümü
   - "🤖 AI Quiz'i Başlat" butonu (id="btn-start-quiz")
   - Quiz kartı (başta gizli, id="quiz-card"):
     * Yükleniyor spinner
     * Soru metni
     * 4 adet seçenek butonu (A/B/C/D)
     * Seçim sonrası: doğru=yeşil animasyon, yanlış=kırmızı + doğrusu yeşil
     * Explanation kutusu (seçim sonrası görünür)
     * "Tamamla ve İlerle" butonu → /lessons/<id>/complete POST, ai_score=100 veya 40

JS gereksinimleri:
- fetch ile /lessons/<id>/quiz POST isteği
- Cevap seçilince tüm butonlar disabled
- Doğruysa ai_score=100, yanlışsa ai_score=40
- Tamamla butonu form submit ile lesson_complete'e gönderir
- CSRF token: sayfadaki hidden input'tan al

Kısıtlar:
- Mevcut design system CSS variable'ları kullan (--p, --a, --r, --surface vb.)
- base.html'i değiştirme
- Sadece lesson_detail.html değiştir
- Terminal komutu çalıştırma

Önce planı göster.
```

### Sıradaki Adım — Prompt C (Prompt B'den sonra)

**Prompt C — Testler + Commit**
- tests/test_models.py: User set_password/check_password testleri
- tests/test_auth.py: kayıt, giriş, çıkış akışları
- tests/conftest.py: test client + in-memory SQLite fixture
- 3 commit atılacak:
  1. "Gemini AI quiz backend eklendi - Prompt A"
  2. "lesson_detail Duolingo tarzına dönüştürüldü - Prompt B"
  3. "Testler eklendi - Prompt C"

### Zorunlu Gereksinim Durumu
| # | Gereksinim | Durum |
|---|-----------|-------|
| 1 | Application factory + blueprint | ✅ |
| 2 | En az 4 sayfa, base template | ✅ |
| 3 | Flask-WTF, 2 form, CSRF | ✅ |
| 4 | SQLAlchemy, 3 model, ilişkiler | ✅ |
| 5 | Flask-Migrate, migration | ✅ |
| 6 | Flask-Login, kayıt/giriş/çıkış | ✅ |
| 7 | 404/500 hata sayfaları | ✅ |
| 8 | Pagination | ✅ |
| 9 | Bootstrap/Tailwind, mobil uyumlu | ✅ |
| 10 | Docker veya deploy | ❌ bekliyor |

### Bonus Durum
| Bonus | Durum |
|-------|-------|
| E-posta şifre sıfırlama (+5) | ❌ bekliyor |
| API endpoint /api/v1/ (+5) | ❌ bekliyor |
| Tam metin arama (+3) | ❌ bekliyor |
| Flask-Babel TR/EN (+3) | ❌ bekliyor |
| Kullanıcı profili + avatar (+4) | ❌ bekliyor |