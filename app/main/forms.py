"""
CyberLearn AI — Main Blueprint Formları

TopicForm   : Konu oluşturma / düzenleme
LessonForm  : Ders oluşturma
ProfileForm : Kullanıcı profil düzenleme

Tüm hata mesajları Türkçe'dir.
CSRF koruması FlaskForm üzerinden sağlanır.
"""

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL


class TopicForm(FlaskForm):
    """Konu oluşturma ve düzenleme formu."""

    title = StringField(
        "Başlık",
        validators=[
            DataRequired(message="Başlık zorunludur."),
            Length(max=128, message="Başlık en fazla 128 karakter olabilir."),
        ],
        render_kw={"placeholder": "Örn: Ağ Güvenliği"},
    )
    description = TextAreaField(
        "Açıklama",
        validators=[Optional()],
        render_kw={"placeholder": "Konu hakkında kısa bir açıklama...", "rows": 4},
    )
    icon = StringField(
        "Simge (emoji)",
        validators=[Optional(), Length(max=64, message="Simge en fazla 64 karakter olabilir.")],
        render_kw={"placeholder": "🔒"},
    )
    order = IntegerField(
        "Sıra",
        validators=[
            Optional(),
            NumberRange(min=0, message="Sıra 0 veya daha büyük olmalıdır."),
        ],
        default=0,
    )


class LessonForm(FlaskForm):
    """Ders oluşturma formu."""

    title = StringField(
        "Başlık",
        validators=[
            DataRequired(message="Başlık zorunludur."),
            Length(max=128, message="Başlık en fazla 128 karakter olabilir."),
        ],
        render_kw={"placeholder": "Örn: Firewall Nedir?"},
    )
    content = TextAreaField(
        "İçerik",
        validators=[DataRequired(message="İçerik zorunludur.")],
        render_kw={"placeholder": "Ders içeriğini buraya yazın...", "rows": 10},
    )
    difficulty = SelectField(
        "Zorluk Seviyesi",
        choices=[
            ("beginner", "🟢 Kolay"),
            ("intermediate", "🟡 Orta"),
            ("advanced", "🔴 Zor"),
        ],
        default="beginner",
    )
    order = IntegerField(
        "Sıra",
        validators=[
            Optional(),
            NumberRange(min=0, message="Sıra 0 veya daha büyük olmalıdır."),
        ],
        default=0,
    )


class ProfileForm(FlaskForm):
    """Kullanıcı profil düzenleme formu."""

    bio = TextAreaField(
        "Hakkımda",
        validators=[
            Optional(),
            Length(max=256, message="Bio en fazla 256 karakter olabilir."),
        ],
        render_kw={
            "placeholder": "Kendinden kısaca bahset...",
            "rows": 3,
            "maxlength": "256",
        },
    )
    avatar_url = StringField(
        "Avatar URL",
        validators=[
            Optional(),
            Length(max=512, message="URL en fazla 512 karakter olabilir."),
            URL(message="Geçerli bir URL giriniz (https://... ile başlamalı)."),
        ],
        render_kw={
            "placeholder": "https://api.dicebear.com/7.x/bottts/svg?seed=...",
            "maxlength": "512",
        },
    )
    submit = SubmitField("Profili Kaydet")


