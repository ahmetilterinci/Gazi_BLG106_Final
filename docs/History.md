# Proje Geliştirme Geçmişi

## Oturum 1 — 23 Mayıs 2026 ✅ TAMAMLANDI

**Prompt 1 — Proje iskeleti (Antigravity)**
- Application factory pattern + blueprint yapısı kuruldu
- app/auth/ ve app/main/ blueprint'leri oluşturuldu
- config.py: DevelopmentConfig / ProductionConfig
- requirements.txt, .env.example, .gitignore, run.py

**Prompt 2 — README.md (Antigravity)**
- Türkçe README, kurulum adımları, teknoloji listesi

**Prompt 3 — Modeller (Antigravity)**
- User, Topic, Lesson, UserProgress — SQLAlchemy 2.x stili (Mapped/mapped_column)
- UniqueConstraint(user_id, lesson_id), datetime.now(timezone.utc)

**Prompt 4 — Migration (manuel terminal)**
- flask db init → stamp head → migrate → upgrade
- ⚠️ Ajan migration dosyasını silmeyi önerdi, reddedildi

**Prompt 5 — Auth akışı (Antigravity)**
- RegisterForm + LoginForm, /register /login /logout rotaları
- 404/500 hata handler'ları, base.html + auth şablonları

### Commit Geçmişi
| # | Mesaj |
|---|-------|
| 1 | Proje iskeleti kuruldu - Prompt 1-2 |
| 2 | Modeller ve migration eklendi - Prompt 3-4 |
| 3 | Auth akışı eklendi - Prompt 5 |

---

## Oturum 2 — 24.05.2026 ✅ TAMAMLANDI

**UI Yenileme — base.html + index.html + auth sayfaları (Danışman Claude)**
- Syne + Inter + JetBrains Mono font sistemi
- Design tokens: --p:#6e5bff, --a:#00f5c4, --r:#ff3d6b
- index.html: Hero → Özellikler → Nasıl Çalışır → Topics Preview → Stats → CTA
- login.html + register.html sıfırdan yazıldı
- 404.html + 500.html design system ile uyumlu

**Prompt 6 — CRUD Rotaları + Şablonlar + Pagination (Antigravity)**
- topics, topic_detail, topic_new, topic_edit, topic_delete rotaları
- lesson_detail, lesson_new, lesson_complete rotaları
- TopicForm + LessonForm (Flask-WTF)
- Pagination (sayfa başı 10)
- Topic modeline user_id FK eklendi + migration

**Seed Sistemi — commands.py**
- flask seed-db: 3 konu, 9 ders (Ağ Güvenliği, Şifreleme, Web Güvenliği)
- İdempotent, gerçek siber güvenlik içerikleri

### Commit Geçmişi
| # | Mesaj |
|---|-------|
| 4 | UI yenileme - base ve index şablonları |
| 5 | login ve register şablonları yenilendi |
| 6 | 404 ve 500 hata sayfaları yenilendi |
| 7 | CRUD rotaları ve şablonlar eklendi - Prompt 6 |
| 8 | Seed sistemi eklendi - commands.py |

---

## Oturum 3 — 27.05.2026 ✅ TAMAMLANDI

Bu oturumda projenin tüm ders/öğrenme sistemi sıfırdan yeniden tasarlandı.

**Prompt A — Gemini AI Quiz Backend**
- google-generativeai requirements.txt'e eklendi
- POST /lessons/<id>/quiz rotası eklendi (csrf.exempt + login_required)
- Gemini gemini-2.5-flash ile JSON formatında soru üretiyor
- lesson_complete rotası ai_score parametresini kabul ediyor

**Prompt B — İzometrik Öğrenme Yolu (Danışman Claude)**
- index.html authenticated bölümü tamamen yeniden yazıldı
- Her Topic = "Dünya" bloğu: başlık bandı + progress bar + izometrik ders yolu
- Zigzag düğümler: tamamlandı (mor+check), aktif (parlayan), kilitli (gri)
- SVG dönüş konnektörleri
- routes.py index(): topic/lesson/progress verilerini çekiyor, kilit mantığı hesaplıyor
- routes.py lesson_detail(): kilitli derse URL ile erişim engellendi
- Kilit kuralı: Topic N açık olmak için Topic N-1 tamamen bitmeli

**Prompt B ek — Duolingo Quiz v1→v5 (Danışman Claude)**
- 4 soru tipi: mcq, truefalse, fillblank, matching
- Her soruya hint (3-4 cümle öğretici açıklama)
- Yanlış yapılan sorular sona ekleniyor, doğru yapana kadar tekrar geliyor
- Puan formülü: doğruluk×0.7 + hız_bonusu×0.3
- Sonuç ekranı: Süre + Başarı Oranı barı (renkli, dinamik) + XP
- UserProgress modeline wrong_count + attempts eklendi + migration

### Commit Geçmişi
| #  | Mesaj |
|----|-------|
| 9  | İzometrik öğrenme yolu eklendi - Prompt B |
| 10 | Duolingo quiz v1 eklendi - lesson_detail yenilendi |
| 11 | Quiz çoklu soru + hint sistemi - Prompt B ek2 |
| 12 | 4 tip soru + öğrenme uyumu altyapısı - Prompt B ek3 |

---

## Oturum 4 — 29.05.2026 ✅ TAMAMLANDI

**Prompt C — Render Deploy (Antigravity + Danışman Claude)**
- requirements.txt'e gunicorn eklendi
- run.py: FLASK_CONFIG env'den okunuyor (FLASK_ENV deprecated, Flask 3.x)
- render.yaml: yeni dosya — buildCommand, startCommand, envVars
- .gitignore: *.db eklendi
- db.create_all() run.py'e eklendi (flask db upgrade yerine)
- render.yaml buildCommand'dan flask db upgrade kaldırıldı
- startCommand: `sh -c 'flask seed-db; gunicorn run:app'`
- commands.py: seed çalışması için admin kullanıcı otomatik oluşturma

**Canlı URL:** https://gazi-blg106-final.onrender.com
**Admin giriş:** admin@cyberlearn.io / Admin1234!

⚠️ SQLite ephemeral — her deploy'da veriler sıfırlanır.
Sonraki oturumda PostgreSQL eklenecek.

### Commit Geçmişi
| #  | Mesaj |
|----|-------|
| 13 | Render deploy yapılandırması - Prompt C |
| 14 | db.create_all ile Render SQLite uyumu |
| 15 | render.yaml buildCommand düzeltildi |
| 16 | seed-db startCommand sh ile düzeltildi |
| 17 | seed-db admin kullanıcısı otomatik oluşturma |

---

## Oturum 5 — 30.05.2026 ✅ TAMAMLANDI

**PostgreSQL Geçişi**
- requirements.txt'e psycopg2-binary eklendi
- config.py ProductionConfig: postgres:// → postgresql+psycopg2:// otomatik dönüşüm
- run.py: db.create_all() + stamp() ile tablo oluşturma
- render.yaml: buildCommand'dan flask db upgrade kaldırıldı
- Render dashboard'da DATABASE_URL manuel eklendi
- Start Command: sh -c 'flask db upgrade && flask seed-db; gunicorn run:app'
- ⚠️ render.yaml fromDatabase otomatik inject etmedi — manuel çözüldü

**API Endpoint /api/v1/ (+5 puan)**
- GET /api/v1/topics
- GET /api/v1/topics/<id>
- GET /api/v1/lessons/<id>
- routes.py sonuna eklendi, public erişim

### Commit Geçmişi
| #  | Mesaj |
|----|-------|
| 18 | PostgreSQL desteği eklendi - Oturum 5 |
| 19 | PostgreSQL db.create_all fix - Oturum 5 |
| 20 | API endpoint /api/v1/ eklendi - bonus +5 |

---

## Oturum 6 — 31.05.2026 ✅ TAMAMLANDI

**Statik Sayfalar + Navbar/Footer Güncellemesi (Danışman Claude)**
- Hakkında, S.S.S., İletişim sayfaları oluşturuldu
- Navbar'a Hakkında + İletişim linkleri eklendi
- Footer'daki Hakkında, S.S.S., İletişim linkleri bağlandı
- routes.py'e /about, /faq, /contact rotaları eklendi

**Kullanıcı Profili + Avatar (+4 puan) (Danışman Claude)**
- User modeline avatar_url + bio alanları eklendi + migration
- ProfileForm (Flask-WTF) oluşturuldu
- /profile + /profile/avatar rotaları eklendi
- profile.html: avatar hero, istatistik kartları, DiceBear entegrasyonu

**Flask-Babel TR/EN (+3 puan) (Danışman Claude)**
- flask-babel requirements.txt'e eklendi
- app/__init__.py: Babel entegrasyonu, get_locale(), context_processor, /set-lang/<lang>
- babel.cfg oluşturuldu
- Tüm şablonlar `{{ _('...') }}` ile güncellendi:
  base.html, index.html, about.html, faq.html, contact.html, profile.html,
  login.html, register.html, lesson_detail.html, lesson_form.html,
  confirm_delete.html, 404.html, 500.html
- pybabel extract → init (tr + en) → compile
- app/translations/en/LC_MESSAGES/messages.po tüm çevirilerle dolduruldu
- render.yaml buildCommand güncellendi: `pip install -r requirements.txt && pybabel compile -d app/translations`
- Animasyonlu TR/EN pill switcher tasarımı base.html'e eklendi

**Çözülen Kritik Sorunlar**
- babel.cfg'den jinja2.ext.autoescape + jinja2.ext.with_ kaldırıldı (yeni Jinja2'de yok)
- get_locale() context_processor ile Jinja2'ye inject edildi
- EN messages.po'daki tüm boş msgstr alanları çeviriyle dolduruldu

### Commit Geçmişi
| #  | Mesaj |
|----|-------|
| 21 | Navbar ve footer: Hakkinda, SSS, Iletisim linkleri eklendi |
| 22 | Flask-Babel TR/EN dil destegi eklendi |
| 23 | Flask-Babel EN ceviri dosyasi tamamlandi |

---

## Zorunlu Gereksinim Durumu
| # | Gereksinim | Durum |
|---|-----------|-------|
| 1 | Application factory + blueprint | ✅ |
| 2 | En az 4 sayfa, base template, template inheritance | ✅ |
| 3 | Flask-WTF, 2 form, CSRF koruması | ✅ |
| 4 | SQLAlchemy, 3 model, ilişkiler | ✅ |
| 5 | Flask-Migrate, migration dosyaları | ✅ |
| 6 | Flask-Login, kayıt/giriş/çıkış, şifre hash | ✅ |
| 7 | 404/500 hata sayfaları | ✅ |
| 8 | Pagination | ✅ |
| 9 | Bootstrap/Tailwind, mobil uyumlu | ✅ |
| 10 | Docker veya canlı deploy | ✅ Render |

## Bonus Durum
| Bonus | Puan | Durum |
|-------|------|-------|
| API endpoint /api/v1/ | +5 | ✅ Oturum 5 |
| Kullanıcı profili + avatar | +4 | ✅ Oturum 6 |
| Flask-Babel TR/EN | +3 | ✅ Oturum 6 |
| Tam metin arama | +3 | ❌ Yapılmadı |
| E-posta şifre sıfırlama | +5 | ❌ Yapılmadı |

## Mevcut Dosya Durumu
- `app/__init__.py`: Babel entegrasyonu, context_processor, /set-lang rotası
- `app/models.py`: User (avatar_url, bio), Topic, Lesson, UserProgress
- `app/main/routes.py`: tüm rotalar + about/faq/contact + profile/avatar
- `app/main/forms.py`: ProfileForm dahil tüm formlar
- `app/commands.py`: flask seed-db
- `app/translations/tr/LC_MESSAGES/messages.po` + messages.mo
- `app/translations/en/LC_MESSAGES/messages.po` + messages.mo
- `babel.cfg`: jinja2 şablon tarayıcı
- `render.yaml`: pybabel compile buildCommand'a eklendi
- `requirements.txt`: flask-babel eklendi
- `templates/base.html`: Babel + animasyonlu TR/EN switcher
- `templates/main/`: index, about, faq, contact, profile, lesson_detail, lesson_form, confirm_delete
- `templates/auth/`: login, register
- `templates/errors/`: 404, 500

## Canlı URL
https://gazi-blg106-final.onrender.com

