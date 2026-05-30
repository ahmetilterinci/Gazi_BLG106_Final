"""
CyberLearn AI — Veritabanı Modelleri

SQLAlchemy 2.x stili (Mapped / mapped_column) kullanılır.
db.Column KULLANILMAZ.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from flask_login import UserMixin
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class User(UserMixin, db.Model):
    """Kayıtlı kullanıcıyı temsil eder."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # İlişkiler
    progress_entries: Mapped[list[UserProgress]] = relationship(
        "UserProgress", back_populates="user"
    )
    topics_created: Mapped[list[Topic]] = relationship(
        "Topic", back_populates="creator"
    )

    # ------------------------------------------------------------------
    # Şifre yönetimi
    # ------------------------------------------------------------------

    def set_password(self, password: str) -> None:
        """Ham şifreyi hash'leyerek kaydeder."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verilen şifrenin hash ile eşleşip eşleşmediğini döner."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

class Topic(db.Model):
    """Siber güvenlik konularını (örn. 'Ağ Güvenliği') temsil eder."""

    __tablename__ = "topic"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Konuyu oluşturan kullanıcı (nullable — eski kayıtlar veya seed verisi için)
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=True
    )

    # İlişkiler
    lessons: Mapped[list[Lesson]] = relationship(
        "Lesson", back_populates="topic"
    )
    creator: Mapped[Optional[User]] = relationship(
        "User", back_populates="topics_created"
    )

    def __repr__(self) -> str:
        return f"<Topic {self.title} (owner={self.user_id})>"


# ---------------------------------------------------------------------------
# Lesson
# ---------------------------------------------------------------------------

class Lesson(db.Model):
    """Bir konuya ait tek bir dersi temsil eder."""

    __tablename__ = "lesson"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str] = mapped_column(
        String(20), nullable=False, default="beginner"
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    topic_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("topic.id"), nullable=False
    )

    # İlişkiler
    topic: Mapped[Topic] = relationship("Topic", back_populates="lessons")
    progress_entries: Mapped[list[UserProgress]] = relationship(
        "UserProgress", back_populates="lesson"
    )

    def __repr__(self) -> str:
        return f"<Lesson {self.title} [{self.difficulty}]>"


# ---------------------------------------------------------------------------
# UserProgress
# ---------------------------------------------------------------------------

class UserProgress(db.Model):
    """Bir kullanıcının belirli bir dersteki ilerlemesini kaydeder."""
 
    __tablename__ = "user_progress"
 
    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson"),
    )
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False
    )
    lesson_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lesson.id"), nullable=False
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    # Öğrenme uyumu için yeni alanlar
    wrong_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    attempts: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
 
    # İlişkiler
    user: Mapped[User] = relationship("User", back_populates="progress_entries")
    lesson: Mapped[Lesson] = relationship(
        "Lesson", back_populates="progress_entries"
    )
 
    def __repr__(self) -> str:
        return (
            f"<UserProgress user={self.user_id} "
            f"lesson={self.lesson_id} "
            f"completed={self.is_completed} "
            f"attempts={self.attempts}>"
        )
