"""
CyberLearn AI — Auth Formları

RegisterForm : Kullanıcı kayıt formu (username, email, password, confirm)
LoginForm    : Kullanıcı giriş formu (email, password, remember)
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
)


class RegisterForm(FlaskForm):
    """Yeni kullanıcı kayıt formu."""

    username = StringField(
        "Kullanıcı Adı",
        validators=[
            DataRequired(message="Kullanıcı adı zorunludur."),
            Length(min=3, max=64, message="Kullanıcı adı 3-64 karakter arasında olmalıdır."),
        ],
    )
    email = EmailField(
        "E-posta",
        validators=[
            DataRequired(message="E-posta adresi zorunludur."),
            Email(message="Geçerli bir e-posta adresi giriniz."),
            Length(max=120, message="E-posta adresi en fazla 120 karakter olabilir."),
        ],
    )
    password = PasswordField(
        "Şifre",
        validators=[
            DataRequired(message="Şifre zorunludur."),
            Length(min=8, message="Şifre en az 8 karakter olmalıdır."),
        ],
    )
    confirm = PasswordField(
        "Şifre Tekrar",
        validators=[
            DataRequired(message="Şifre tekrarı zorunludur."),
            EqualTo("password", message="Şifreler eşleşmiyor."),
        ],
    )
    submit = SubmitField("Kayıt Ol")

    def validate_email(self, field: EmailField) -> None:
        """E-posta adresinin veritabanında kayıtlı olup olmadığını kontrol eder."""
        from app.models import User
        from app import db

        existing_user = db.session.scalar(
            db.select(User).where(User.email == field.data.lower().strip())
        )
        if existing_user:
            raise ValidationError(
                "Bu e-posta adresi zaten kayıtlı. Lütfen giriş yapın veya farklı bir e-posta kullanın."
            )

    def validate_username(self, field: StringField) -> None:
        """Kullanıcı adının veritabanında kayıtlı olup olmadığını kontrol eder."""
        from app.models import User
        from app import db

        existing_user = db.session.scalar(
            db.select(User).where(User.username == field.data.strip())
        )
        if existing_user:
            raise ValidationError(
                "Bu kullanıcı adı zaten alınmış. Lütfen farklı bir kullanıcı adı seçin."
            )


class LoginForm(FlaskForm):
    """Kullanıcı giriş formu."""

    email = EmailField(
        "E-posta",
        validators=[
            DataRequired(message="E-posta adresi zorunludur."),
            Email(message="Geçerli bir e-posta adresi giriniz."),
        ],
    )
    password = PasswordField(
        "Şifre",
        validators=[
            DataRequired(message="Şifre zorunludur."),
        ],
    )
    remember = BooleanField("Beni Hatırla")
    submit = SubmitField("Giriş Yap")
