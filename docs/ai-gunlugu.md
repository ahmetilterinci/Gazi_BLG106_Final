## Oturum 1 — 23.05.2026 — 18:30-21:30

### Hedef
Proje iskeletini kurmak, README yazmak, veritabanı modellerini tanımlamak,
migration'ı çalıştırmak ve tabloları SQLite'a yazmak.

### Kullandığım Mod ve Model
- Mod: Plan
- Model: Claude Sonnet 4.6
- Görünüm: Manager View

### Verdiğim Promptlar
1. Prompt 1 — Proje iskeleti: Application factory + blueprint yapısı,
   requirements.txt, .gitignore, .env.example, run.py oluşturulması
2. Prompt 2 — README.md: Projeye özel Türkçe dokümantasyon
3. Prompt 3 — Model tasarımı: User, Topic, Lesson, UserProgress
   modellerinin SQLAlchemy 2.x stiliyle yazılması
4. Prompt 4 — Migration: flask db init → migrate → upgrade adım adım,
   her komut öncesi onay istenerek

### Ajanın Önerdiği Plan (Prompt 3)
- 4 model için alan listeleri ve ilişkiler tablo halinde sunuldu
- UniqueConstraint önerisini ajan kendisi "Açık Sorular" bölümünde sordu
- lazy="dynamic" kullanılmayacağını belirtti (SQLAlchemy 2.x uyumu)
- Import listesini önceden paylaştı

### Ajanın Önerdiği Plan (Prompt 4)
- 4 adım, 3 onay noktası: flask db init → flask db migrate → dosya inceleme → flask db upgrade
- FLASK_APP=run.py kontrolü notu ekledi
- Antigravity terminali C:\ sürücüsüne erişemediği için komutları manuel girdirdim

### Plan'da Sorguladıklarım
- `datetime.utcnow` kullanımına itiraz ettim: Flask 3.x + SQLAlchemy 2.x'te
  deprecation uyarısı veriyor. `datetime.now(timezone.utc)` kullanılmasını
  talep ettim. Ajan planı revize etti, `lambda` ile doğru şekilde uyguladı.
- `User.progresses` yerine `User.progress_entries` adlandırmasını tercih ettim:
  daha açıklayıcı ve ilişkinin ne olduğunu isimden anlamak kolaylaşıyor.
- `UniqueConstraint(user_id, lesson_id)` eklenmesini onayladım: aynı kullanıcının
  aynı derse iki kez kayıt oluşturmasını engellemek veri bütünlüğü açısından
  zorunlu.
- `flask db migrate` "Target database is not up to date" hatası verdi.
  `flask db stamp head` ile çözdüm — ajan sonradan bunun yanlış sıra olduğunu
  belirtti. Doğru sıranın önce `flask db upgrade`, sonra `flask db migrate`
  olduğunu öğrendim.

### Üretilen Kodda Düzelttiklerim
- Ajan 3 değişikliği doğru uyguladı, ek müdahale gerekmedi.
- `__table_args__` içinde UniqueConstraint `name="uq_user_lesson"` ile
  tanımlandı — migration sırasında anlamlı constraint ismi olması için iyi.

### ⚠️ Ajanın Yanlış Önerisi — Yakaladım
Prompt 4 sırasında ajan migration tamamlandıktan sonra şu komutları önerdi:
```powershell
Remove-Item migrations\versions\f1abdb670357_initial_schema_user_topic_lesson_.py
flask db stamp base
flask db upgrade
```
Migration dosyasını silmemi istiyordu. Danışman Claude ile dosya içeriğini
inceledim — 4 tablo, tüm FK'lar, UniqueConstraint, email/username index'leri
eksiksiz ve doğruydu. Silme önerisini reddettim, direkt `flask db upgrade`
çalıştırdım. Tablolar başarıyla oluştu.

**Bu, planı sorgulamadan onaylamanın ne kadar tehlikeli olduğunun somut kanıtı.**

### Karşılaştığım Hatalar ve Çözümler
- Antigravity terminali PowerShell sandbox'ta `C:\` sürücüsüne erişemedi,
  otomatik doğrulama çalıştıramadı. Çözüm: komutları kendi terminalimde
  manuel çalıştırdım.
- Hata: `ERROR: Target database is not up to date`
  Çözüm: `flask db stamp head` ile mevcut durumu işaretledim, ardından
  migrate tekrar çalıştı. (Not: doğru sıra önce upgrade, sonra migrate)
- Import testi:
```powershell
.venv\Scripts\python.exe -c "
from app import create_app; app = create_app('development')
with app.app_context():
    from app.models import User, Topic, Lesson, UserProgress
    print('Import OK')
"
```
  Çıktı: `Import OK` — modeller hatasız yüklendi.

### Bu Oturumdan Öğrendiğim
`datetime.utcnow` gibi görünürde zararsız bir default, Flask 3.x ve
SQLAlchemy 2.x kombinasyonunda deprecation uyarısına yol açıyor. Ajan bunu
kendiliğinden düzeltmedi; planı okuyup sorgulamasaydım bu uyarı migration
aşamasına kadar fark edilmeyecekti.

`flask db stamp head` Alembic'e "veritabanı güncel" dedirtir ama tabloları
gerçekte oluşturmaz. Doğru sıra: önce `flask db upgrade` ile tabloları yaz,
sonra yeni değişiklik varsa `flask db migrate`.

Ajanın "Açık Sorular" bölümü değerliydi: UniqueConstraint gibi veri
bütünlüğü kararlarını kullanıcıya bırakması doğru bir yaklaşım.

### Sonraki Oturum İçin Notlar
- Prompt 5: auth akışı (kayıt, giriş, çıkış), Flask-Login kurulumu,
  Bootstrap 5 formları
- Gün 1 hedefi 3 commit — 2 commit atıldı, Prompt 5 sonrası 3. commit atılacak
- Commits: "Proje iskeleti kuruldu - Prompt 1-2" + "Modeller ve migration eklendi - Prompt 3-4"