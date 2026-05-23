"""
CyberLearn AI — Main Route'ları

/           — Ana sayfa (index)
404 handler — Sayfa bulunamadı
500 handler — Sunucu hatası
"""

from flask import render_template

from app import db
from app.main import main


@main.route("/")
def index():
    """Ana sayfa rotası."""
    return render_template("main/index.html", title="Ana Sayfa")


# ---------------------------------------------------------------------------
# Hata Handler'ları (app genelinde geçerli — @blueprint.app_errorhandler)
# ---------------------------------------------------------------------------


@main.app_errorhandler(404)
def page_not_found(error):
    """404 — Sayfa Bulunamadı."""
    return render_template("errors/404.html", title="Sayfa Bulunamadı"), 404


@main.app_errorhandler(500)
def internal_server_error(error):
    """500 — Sunucu Hatası. Session rollback yapılır."""
    db.session.rollback()
    return render_template("errors/500.html", title="Sunucu Hatası"), 500
