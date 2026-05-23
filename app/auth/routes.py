"""
CyberLearn AI — Auth Route'ları

/auth/register  — Yeni kullanıcı kaydı
/auth/login     — Kullanıcı girişi
/auth/logout    — Kullanıcı çıkışı
"""

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user  # noqa: F401 (login_required ileride kullanılacak)

from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm
from app.models import User


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Yeni kullanıcı kayıt rotası."""
    # Zaten giriş yapılmışsa ana sayfaya yönlendir
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.lower().strip(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form, title="Kayıt Ol")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Kullanıcı giriş rotası."""
    # Zaten giriş yapılmışsa ana sayfaya yönlendir
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.email == form.email.data.lower().strip())
        )

        if user is None or not user.check_password(form.password.data):
            flash("E-posta adresi veya şifre hatalı. Lütfen tekrar deneyin.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember.data)
        flash(f"Hoş geldiniz, {user.username}!", "success")

        # Güvenli yönlendirme: next parametresi varsa kullan, yoksa ana sayfa
        next_page = request.args.get("next")
        if next_page and next_page.startswith("/"):
            return redirect(next_page)
        return redirect(url_for("main.index"))

    return render_template("auth/login.html", form=form, title="Giriş Yap")


@auth.route("/logout")
def logout():
    """Kullanıcı çıkış rotası."""
    logout_user()
    flash("Başarıyla çıkış yaptınız. Görüşmek üzere!", "info")
    return redirect(url_for("main.index"))
