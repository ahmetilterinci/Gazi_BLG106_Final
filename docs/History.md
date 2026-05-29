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

### Yapılan Değişiklikler

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
- routes.py lesson_detail(): kilitli derse URL ile erişim engellendi (flash + redirect)
- Kilit kuralı: Topic N açık olmak için Topic N-1 tamamen bitmeli

**Prompt B ek — Duolingo Quiz v1→v2→v3 (Danışman Claude)**
- "Döküman oku + kendine puan ver" sistemi tamamen kaldırıldı
- lesson_detail.html: Başlat → Yükleniyor → Soru → Feedback → Devam akışı
- lesson_quiz endpoint: içerik uzunluğuna göre 5-12 soru üretiyor
- Her soruya hint (3-4 cümle öğretici açıklama) eklendi
- Yanlış yapılan sorular sona ekleniyor, doğru yapana kadar tekrar geliyor
- Tekrar turu ekranı + kutlama ekranı

**Prompt B ek2 — 4 Tip Soru + Öğrenme Uyumu (Danışman Claude)**
- UserProgress modeline wrong_count + attempts alanları eklendi
- Migration: server_default='0' elle eklenerek flask db upgrade başarılı
- 4 soru tipi: mcq, truefalse, fillblank, matching
- Her tipten en az 1 soru zorunlu
- Performans bazlı dağılım: yeni kullanıcı→mcq ağırlıklı, çok yanlış→kolay tipler
- lesson_complete: wrong_count ve attempts güncelleniyor
- Her tip için özel UI: eşleştirme tıkla-bağla, boşluk doldurma ___ animasyonu

**Prompt B ek3 — Kalp Sistemi Kaldırıldı + Yeni Puan Sistemi (Danışman Claude)**
- Kalp (can) sistemi tamamen kaldırıldı
- Progress şeridine süre sayacı eklendi (0:00 formatı)
- Başarı oranı %100'den başlar, her yanlışta (100/toplam_soru) kadar düşer
- Puan formülü: doğruluk×0.7 + hız_bonusu×0.3 (hız: soru başına ortalama süre)
- Sonuç ekranı: sadece Süre + Başarı Oranı barı (renkli, dinamik) + XP
- Bar rengi: %80+ mor-yeşil, %50-79 sarı, <%50 kırmızı

### Mevcut Dosya Durumu
- `app/models.py`: UserProgress'e wrong_count + attempts eklendi
- `app/main/routes.py`: index(), lesson_detail(), lesson_quiz(), lesson_complete() güncellendi
- `templates/main/index.html`: izometrik öğrenme yolu
- `templates/main/lesson_detail.html`: tam Duolingo deneyimi (v5 — son hal)

### ⚠️ Test Edilmedi
- 2. denemede soru dağılımının gerçekten değişip değişmediği test edilmedi
- Teslim tarihi nedeniyle geçildi, AI günlüğüne not düşüldü

### Commit Geçmişi
| #  | Mesaj |
|----|-------|
| 9  | İzometrik öğrenme yolu eklendi - Prompt B |
| 10 | Duolingo quiz v1 eklendi - lesson_detail yenilendi |
| 11 | Quiz çoklu soru + hint sistemi - Prompt B ek2 |
| 12 | 4 tip soru + öğrenme uyumu altyapısı - Prompt B ek3 |

---

## YAPILACAKLAR — Sonraki Oturum

### ⚠️ Önemli Not
**Site tasarımı tekrardan değiştirilecek.** Mevcut tasarım korunmayacak, yeni bir UI gelecek.

### Zorunlu (önce bunlar)
1. **Render Deploy** — GitHub repo bağla, environment variables ayarla, canlı URL al (-20 puan riski)

### Bonus (sırasıyla)
2. **API endpoint /api/v1/** — +5 puan, ~1 saat
3. **Kullanıcı profili + avatar** — +4 puan, ~2-3 saat
4. **Tam metin arama** — +3 puan, ~2-3 saat
5. **Babel TR/EN** — +3 puan, riskli, en sona bırak
6. **E-posta şifre sıfırlama** — +5 puan, e-posta servisi gerekiyor, riskli

### Teslim: 01/06/2026 saat 13:00
- Demo video
- rapor.md
- AI günlüğü son güncelleme
- Son commit + push

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
| 10 | Docker veya canlı deploy | ❌ YAPILACAK |

## Bonus Durum
| Bonus | Puan | Durum |
|-------|------|-------|
| API endpoint /api/v1/ | +5 | ❌ YAPILACAK |
| Kullanıcı profili + avatar | +4 | ❌ YAPILACAK |
| Tam metin arama | +3 | ❌ YAPILACAK |
| E-posta şifre sıfırlama | +5 | ❌ riskli |
| Flask-Babel TR/EN | +3 | ❌ riskli |