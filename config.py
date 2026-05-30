"""
CyberLearn AI — Konfigürasyon Sınıfları

Kullanım (create_app içinde):
    app.config.from_object(config["development"])
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Tüm ortamlar için ortak temel ayarlar."""

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "degistir-beni-lutfen")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    WTF_CSRF_ENABLED: bool = True


class DevelopmentConfig(Config):
    """Geliştirme ortamı ayarları."""

    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", "sqlite:///cyberlearn_dev.db"
    )


class ProductionConfig(Config):
    """Üretim ortamı ayarları."""

    DEBUG: bool = False
    _db_url: str = os.environ.get("DATABASE_URL", "sqlite:///cyberlearn_prod.db")
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql+psycopg2://", 1)
    SQLALCHEMY_DATABASE_URI: str = _db_url


# create_app(config_name) çağrısında kullanılacak sözlük
config: dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
