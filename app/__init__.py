"""
CyberLearn AI — Uygulama Paketi
Application Factory Pattern ile Flask uygulaması oluşturulur.
"""

from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_babel import Babel

from config import config

# ---------------------------------------------------------------------------
# Extension nesneleri (henüz app'e bağlanmadı — factory içinde init edilir)
# ---------------------------------------------------------------------------
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
babel = Babel()


def get_locale():
    """Kullanıcının dil tercihini döndürür. Session > tarayıcı tercihi."""
    return session.get("lang", request.accept_languages.best_match(["tr", "en"]) or "tr")


def create_app(config_name: str = "development") -> Flask:
    """
    Application Factory.

    Kullanım:
        from app import create_app
        app = create_app("development")
    """
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # Konfigürasyon yükle
    app.config.from_object(config[config_name])

    # Babel yapılandırması
    app.config["BABEL_DEFAULT_LOCALE"] = "tr"
    app.config["BABEL_SUPPORTED_LOCALES"] = ["tr", "en"]

    # Extension'ları uygulamaya bağla
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    # ---------------------------------------------------------------------------
    # Flask-Login yapılandırması
    # ---------------------------------------------------------------------------
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Bu sayfayı görüntülemek için giriş yapmalısınız."
    login_manager.login_message_category = "warning"

    from app.models import User  # noqa: F401 — user_loader için gerekli

    @login_manager.user_loader
    def load_user(user_id: str):
        """Flask-Login'in oturum yönetimi için kullanıcıyı ID'ye göre yükler."""
        return db.session.get(User, int(user_id))

    # ---------------------------------------------------------------------------
    # Model kayıtları — Alembic autogenerate için metadata'nın dolu olması gerekir
    # ---------------------------------------------------------------------------
    from app import models  # noqa: F401

    # ---------------------------------------------------------------------------
    # Blueprint kayıtları
    # ---------------------------------------------------------------------------
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # ---------------------------------------------------------------------------
    # Dil değiştirme rotası
    # ---------------------------------------------------------------------------
    @app.route("/set-lang/<lang>")
    def set_lang(lang: str):
        from flask import redirect, url_for
        if lang in ["tr", "en"]:
            session["lang"] = lang
        return redirect(request.referrer or url_for("main.index"))

    # ---------------------------------------------------------------------------
    # CLI komutları
    # ---------------------------------------------------------------------------
    from app import commands as _commands  # noqa: F401
    app.cli.add_command(_commands.seed_db)

    return app