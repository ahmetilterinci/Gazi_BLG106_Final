"""
CyberLearn AI — Seed CLI Komutu

Çalıştırma: flask seed-db
Tekrar çalıştırılırsa idempotent davranır (var olan veri atlanır).
"""

import click
from flask.cli import with_appcontext

from app import db
from app.models import Lesson, Topic, User


@click.command("seed-db")
@with_appcontext
def seed_db():
    """Veritabanına örnek konu ve ders verisi ekler (idempotent)."""

    if Topic.query.first():
        click.echo("⚠️  Veritabanı zaten dolu — seed atlandı.")
        return

    click.echo("🌱 Seed verisi ekleniyor...")

    admin = User.query.first()
    if not admin:
        click.echo("❌ Önce bir kullanıcı kaydı oluşturun (/register), sonra seed-db çalıştırın.")
        return

    # ------------------------------------------------------------------ #
    # Konu 1: Ağ Güvenliği
    # ------------------------------------------------------------------ #
    topic1 = Topic(
        title="Ağ Güvenliği",
        description=(
            "Ağ altyapısını koruma yöntemlerini, firewall teknolojilerini "
            "ve TCP/IP protokol güvenliğini öğrenin."
        ),
        icon="🌐",
        order=1,
        user_id=admin.id,
    )
    db.session.add(topic1)
    db.session.flush()  # ID almak için

    db.session.add_all([
        Lesson(
            title="Temel Ağ Kavramları",
            content=(
                "# Temel Ağ Kavramları\n\n"
                "Bir ağ, birbirine bağlı cihazların oluşturduğu sistemdir. "
                "IP adresleri, MAC adresleri, alt ağlar (subnet) ve yönlendirme "
                "(routing) bu ağın temel bileşenleridir.\n\n"
                "## OSI Modeli\n"
                "OSI modeli, ağ iletişimini 7 katmana ayırır:\n"
                "1. Fiziksel Katman\n2. Veri Bağlantı Katmanı\n"
                "3. Ağ Katmanı\n4. Taşıma Katmanı\n"
                "5. Oturum Katmanı\n6. Sunum Katmanı\n7. Uygulama Katmanı\n\n"
                "Her katman belirli görevleri üstlenerek üst katmana hizmet verir."
            ),
            difficulty="beginner",
            order=1,
            topic_id=topic1.id,
        ),
        Lesson(
            title="Firewall Nedir?",
            content=(
                "# Firewall (Güvenlik Duvarı)\n\n"
                "Firewall, ağ trafiğini belirli kurallara göre filtreleyen "
                "donanım veya yazılım tabanlı bir güvenlik sistemidir.\n\n"
                "## Firewall Türleri\n"
                "- **Paket Filtreli Firewall**: IP/port bazlı filtreleme\n"
                "- **Durum Bilgili Firewall**: Bağlantı durumunu takip eder\n"
                "- **Uygulama Katmanı Firewall (WAF)**: HTTP trafiğini inceler\n\n"
                "## Kural Yazımı\n"
                "İzin ver/reddet kuralları kaynak IP, hedef IP ve port numarasına "
                "göre oluşturulur. Kurallar sırayla değerlendirilir."
            ),
            difficulty="intermediate",
            order=2,
            topic_id=topic1.id,
        ),
        Lesson(
            title="TCP/IP Güvenliği",
            content=(
                "# TCP/IP Protokol Güvenliği\n\n"
                "TCP/IP, internetin temel protokol ailesidir. "
                "Bu protokollerdeki zafiyetler ciddi güvenlik açıklarına yol açabilir.\n\n"
                "## Yaygın Saldırılar\n"
                "- **SYN Flood**: TCP üçlü el sıkışmasını suistimal eder\n"
                "- **IP Spoofing**: Sahte kaynak IP adresi kullanımı\n"
                "- **Man-in-the-Middle**: İki taraf arasına girme\n\n"
                "## Önlemler\n"
                "SYN çerezleri, kaynak rota doğrulama ve TLS şifreleme "
                "bu saldırılara karşı temel savunma mekanizmalarıdır."
            ),
            difficulty="advanced",
            order=3,
            topic_id=topic1.id,
        ),
    ])

    # ------------------------------------------------------------------ #
    # Konu 2: Şifreleme Temelleri
    # ------------------------------------------------------------------ #
    topic2 = Topic(
        title="Şifreleme Temelleri",
        description=(
            "Simetrik ve asimetrik şifreleme algoritmalarını, "
            "hash fonksiyonlarını ve açık anahtar altyapısını (PKI) keşfedin."
        ),
        icon="🔐",
        order=2,
        user_id=admin.id,
    )
    db.session.add(topic2)
    db.session.flush()

    db.session.add_all([
        Lesson(
            title="Simetrik Şifreleme",
            content=(
                "# Simetrik Şifreleme\n\n"
                "Simetrik şifrelemede şifreleme ve şifre çözme işlemleri "
                "aynı anahtar ile gerçekleştirilir.\n\n"
                "## Yaygın Algoritmalar\n"
                "- **AES (Advanced Encryption Standard)**: 128/192/256-bit anahtar\n"
                "- **DES**: Artık güvensiz kabul edilmektedir\n"
                "- **3DES**: DES'in üçlü uygulaması\n\n"
                "## Avantaj ve Dezavantajlar\n"
                "✅ Hızlı işlem\n"
                "❌ Anahtar dağıtımı sorunu — iki tarafın güvenli kanaldan "
                "aynı anahtarı paylaşması gerekir."
            ),
            difficulty="beginner",
            order=1,
            topic_id=topic2.id,
        ),
        Lesson(
            title="Hash Fonksiyonları",
            content=(
                "# Hash Fonksiyonları\n\n"
                "Hash fonksiyonu, herhangi uzunluktaki girdiyi sabit uzunluklu "
                "bir çıktıya (özet) dönüştürür. Tek yönlüdür; geri dönüşü yoktur.\n\n"
                "## Özellikler\n"
                "- **Determinizm**: Aynı girdi her zaman aynı çıktıyı verir\n"
                "- **Çığır Etkisi**: Küçük değişiklik büyük fark yaratır\n"
                "- **Çarpışma Direnci**: İki farklı girdi aynı hash'i vermemeli\n\n"
                "## Algoritmalar\n"
                "- MD5: 128-bit (güvensiz)\n"
                "- SHA-1: 160-bit (zayıflamış)\n"
                "- SHA-256/SHA-3: Güncel standartlar"
            ),
            difficulty="intermediate",
            order=2,
            topic_id=topic2.id,
        ),
        Lesson(
            title="PKI (Açık Anahtar Altyapısı)",
            content=(
                "# Açık Anahtar Altyapısı (PKI)\n\n"
                "PKI, dijital sertifikalar aracılığıyla güven zinciri "
                "oluşturan bir sistemdir.\n\n"
                "## Bileşenler\n"
                "- **CA (Sertifika Otoritesi)**: Dijital sertifika imzalar\n"
                "- **RA (Kayıt Otoritesi)**: Kimlik doğrulama yapar\n"
                "- **CRL**: İptal edilen sertifikaların listesi\n\n"
                "## TLS Nasıl Çalışır?\n"
                "1. İstemci bağlantı başlatır\n"
                "2. Sunucu sertifikasını gönderir\n"
                "3. İstemci CA üzerinden doğrular\n"
                "4. Oturum anahtarı asimetrik şifrelemeyle paylaşılır\n"
                "5. Veri simetrik şifrelemeyle aktarılır"
            ),
            difficulty="advanced",
            order=3,
            topic_id=topic2.id,
        ),
    ])

    # ------------------------------------------------------------------ #
    # Konu 3: Web Güvenliği
    # ------------------------------------------------------------------ #
    topic3 = Topic(
        title="Web Güvenliği",
        description=(
            "OWASP Top 10 zafiyetlerini, SQL Injection ve "
            "Cross-Site Scripting (XSS) saldırılarını ve savunma yöntemlerini öğrenin."
        ),
        icon="🕷️",
        order=3,
        user_id=admin.id,
    )
    db.session.add(topic3)
    db.session.flush()

    db.session.add_all([
        Lesson(
            title="OWASP Top 10",
            content=(
                "# OWASP Top 10\n\n"
                "OWASP (Open Web Application Security Project), "
                "en kritik web uygulama güvenlik risklerini listeler.\n\n"
                "## 2021 Listesi\n"
                "1. Kırık Erişim Kontrolü\n"
                "2. Kriptografik Hatalar\n"
                "3. Injection\n"
                "4. Güvensiz Tasarım\n"
                "5. Güvenlik Yanlış Yapılandırması\n"
                "6. Savunmasız ve Güncel Olmayan Bileşenler\n"
                "7. Kimlik ve Kimlik Doğrulama Hataları\n"
                "8. Yazılım ve Veri Bütünlüğü Hataları\n"
                "9. Güvenlik Günlüğü ve İzleme Hataları\n"
                "10. Sunucu Taraflı İstek Sahteciliği (SSRF)"
            ),
            difficulty="beginner",
            order=1,
            topic_id=topic3.id,
        ),
        Lesson(
            title="SQL Injection",
            content=(
                "# SQL Injection Saldırısı\n\n"
                "SQL Injection, saldırganın uygulama girdisi aracılığıyla "
                "veritabanı sorgusunu manipüle etmesidir.\n\n"
                "## Örnek Saldırı\n"
                "```sql\n"
                "-- Güvensiz sorgu:\n"
                "SELECT * FROM users WHERE username = '[input]' AND password = '...'\n"
                "\n"
                "-- Saldırı: input = admin' --\n"
                "-- Sonuç: parola kontrolü atlanır!\n"
                "```\n\n"
                "## Önlemler\n"
                "- **Parametreli sorgular** (Prepared Statements)\n"
                "- **ORM kullanımı** (SQLAlchemy gibi)\n"
                "- Girdi doğrulama ve sanitizasyon\n"
                "- En az ayrıcalık prensibi (DB kullanıcısı)"
            ),
            difficulty="intermediate",
            order=2,
            topic_id=topic3.id,
        ),
        Lesson(
            title="XSS Nedir?",
            content=(
                "# Cross-Site Scripting (XSS)\n\n"
                "XSS, saldırganın kurban kullanıcının tarayıcısında "
                "kötü amaçlı JavaScript çalıştırmasına olanak tanır.\n\n"
                "## XSS Türleri\n"
                "- **Yansımalı XSS**: Zararlı kod URL üzerinden iletilir\n"
                "- **Depolanmış XSS**: Zararlı kod veritabanına kaydedilir\n"
                "- **DOM Tabanlı XSS**: Tarayıcı tarafında DOM manipülasyonu\n\n"
                "## Örnek Payload\n"
                "```html\n"
                "<script>document.cookie</script>\n"
                "<img src=x onerror=alert(1)>\n"
                "```\n\n"
                "## Önlemler\n"
                "- **HTML encoding** (çıktı kaçırma)\n"
                "- **Content Security Policy (CSP)** başlığı\n"
                "- HttpOnly ve Secure çerez bayrakları\n"
                "- Jinja2 auto-escape (Flask varsayılan)"
            ),
            difficulty="advanced",
            order=3,
            topic_id=topic3.id,
        ),
    ])

    db.session.commit()
    click.echo("✅ Seed tamamlandı: 3 konu, 9 ders eklendi.")
