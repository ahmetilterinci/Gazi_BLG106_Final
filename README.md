# CyberLearn AI

Yapay zeka desteğiyle, kullanıcının öğrenme şekline göre uyarlanmış kişisel bir siber güvenlik eğitim platformu. Sistem kullanıcının geçmiş yanıtlarını, ilerleme hızını ve tercih ettiği içerik türünü analiz ederek her kullanıcıya özgü bir öğrenme yolu oluşturur. Hedef kitle: siber güvenliğe yeni adım atan, farklı öğrenme temposuna sahip bireyler.

---

## Kurulum

### 1. Depoyu klonla ve sanal ortamı kur

```bash
git clone <repo-url>
cd Gazi_BLG106_Final

python -m venv .venv
# Windows:
.venv\Scripts\Activate.ps1
```

### 2. Bağımlılıkları yükle

```bash
pip install -r requirements.txt
```

### 3. Ortam değişkenlerini ayarla

```bash
copy .env.example .env
```

`.env` dosyasını aç ve `SECRET_KEY` değerini güçlü, rastgele bir string ile değiştir.

### 4. Veritabanını başlat

```bash
flask db init
flask db migrate -m "ilk migration"
flask db upgrade
```

---

## Geliştirme Komutları

| Komut | Açıklama |
|---|---|
| `python run.py` | Geliştirme sunucusunu başlatır |
| `flask run` | Flask CLI ile sunucu başlatır |
| `flask db migrate -m "açıklama"` | Model değişikliği sonrası migration üretir |
| `flask db upgrade` | Bekleyen migration'ları uygular |
| `pytest` | `tests/` altındaki tüm testleri çalıştırır |

---

## Teknolojiler

| Paket | Kullanım Amacı |
|---|---|
| **Flask 3.x** | Web çerçevesi — Application Factory + Blueprint mimarisi |
| **Flask-SQLAlchemy** | ORM — kullanıcı, ders ve ilerleme modelleri |
| **Flask-Migrate** | Veritabanı şema versiyonlama (Alembic tabanlı) |
| **Flask-Login** | Oturum yönetimi ve kimlik doğrulama |
| **Flask-WTF** | Form doğrulama ve CSRF koruması |
| **python-dotenv** | `.env` dosyasından ortam değişkeni yükleme |

---

## Proje Yapısı

```
app/
├── __init__.py     # create_app() factory
├── models.py       # Veritabanı modelleri
├── main/           # Ana sayfa blueprint'i
└── auth/           # Kimlik doğrulama blueprint'i (/auth)
templates/          # Jinja2 HTML şablonları
static/             # CSS, JS, görseller
tests/              # Pytest test dosyaları
config.py           # DevelopmentConfig / ProductionConfig
run.py              # Uygulama giriş noktası
```

---

> **Gazi Üniversitesi — BLG106 İnternet Programcılığı Final Projesi**
