"""
CyberLearn AI — Main Route'ları (Prompt 6)

GET  /                            → index
GET  /topics                      → konu listesi (paginate 9)
GET  /topics/<id>                 → konu detayı + dersler
GET  /lessons/<id>                → ders içeriği
POST /lessons/<id>/complete       → ders tamamla (login_required)
GET,POST /topics/new              → yeni konu (login_required)
GET,POST /topics/<id>/edit        → konu düzenle (login_required + yetki)
GET  /topics/<id>/delete-confirm  → silme onay sayfası (login_required + yetki)
POST /topics/<id>/delete          → konuyu sil (login_required + yetki)
GET,POST /topics/<id>/lessons/new → konuya ders ekle (login_required)
"""

import json
import os
from datetime import datetime, timezone

from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db, csrf
from app.main import main
from app.main.forms import LessonForm, TopicForm
from app.models import Lesson, Topic, UserProgress


# ---------------------------------------------------------------------------
# Ana Sayfa
# ---------------------------------------------------------------------------

@main.route("/")
def index():
    """Ana sayfa rotası."""
    return render_template("main/index.html", title="Ana Sayfa")


# ---------------------------------------------------------------------------
# Konu Listesi — Paginate
# ---------------------------------------------------------------------------

@main.route("/topics")
def topics():
    """Paginate edilmiş konu listesi (sayfa başı 9)."""
    page = request.args.get("page", 1, type=int)
    pagination = (
        Topic.query
        .order_by(Topic.order, Topic.id)
        .paginate(page=page, per_page=9, error_out=False)
    )
    return render_template(
        "main/topics.html",
        title="Konular",
        pagination=pagination,
        topics=pagination.items,
    )


# ---------------------------------------------------------------------------
# Konu Detayı
# ---------------------------------------------------------------------------

@main.route("/topics/<int:id>")
def topic_detail(id: int):
    """Konu detayı + o konuya ait ders listesi."""
    topic = db.get_or_404(Topic, id)
    lessons = (
        Lesson.query
        .filter_by(topic_id=topic.id)
        .order_by(Lesson.order, Lesson.id)
        .all()
    )

    # Giriş yapılmışsa her ders için tamamlanma durumunu çek
    progress_map: dict[int, UserProgress] = {}
    if current_user.is_authenticated:
        lesson_ids = [l.id for l in lessons]
        if lesson_ids:
            rows = UserProgress.query.filter(
                UserProgress.user_id == current_user.id,
                UserProgress.lesson_id.in_(lesson_ids),
            ).all()
            progress_map = {row.lesson_id: row for row in rows}

    return render_template(
        "main/topic_detail.html",
        title=topic.title,
        topic=topic,
        lessons=lessons,
        progress_map=progress_map,
    )


# ---------------------------------------------------------------------------
# Ders Detayı
# ---------------------------------------------------------------------------

@main.route("/lessons/<int:id>")
def lesson_detail(id: int):
    """Ders içeriği + giriş yapılmışsa ilerleme durumu."""
    lesson = db.get_or_404(Lesson, id)
    progress = None
    if current_user.is_authenticated:
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            lesson_id=lesson.id,
        ).first()

    return render_template(
        "main/lesson_detail.html",
        title=lesson.title,
        lesson=lesson,
        progress=progress,
    )


# ---------------------------------------------------------------------------
# Ders Quiz (Gemini AI)
# ---------------------------------------------------------------------------

@main.route("/lessons/<int:id>/quiz", methods=["POST"])
@csrf.exempt
@login_required
def lesson_quiz(id: int):
    """Gemini ile ders içeriğine dayalı çoktan seçmeli soru üret."""
    import google.generativeai as genai  # noqa: PLC0415

    lesson = db.get_or_404(Lesson, id)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY ortam değişkeni tanımlı değil"}), 500

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=(
                "Sen bir siber güvenlik eğitim asistanısın. Verilen ders "
                "içeriğine dayalı 1 adet çoktan seçmeli soru üret. "
                'YALNIZCA şu JSON formatında yanıt ver, başka hiçbir şey yazma: '
                '{"question": "...", "options": ["A) ...", "B) ...", '
                '"C) ...", "D) ..."], "correct_index": 0, '
                '"explanation": "..."}'
            ),
        )
        prompt = f"Ders Başlığı: {lesson.title}\n\nDers İçeriği:\n{lesson.content}"
        response = model.generate_content(prompt)
        # Gemini bazen yanıtı ```json ... ``` bloğu içinde döndürebilir;
        # json.loads'tan önce bu işaretleri temizle
        raw = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        quiz_data = json.loads(raw)
        return jsonify(quiz_data), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# ---------------------------------------------------------------------------
# Ders Tamamlama
# ---------------------------------------------------------------------------

@main.route("/lessons/<int:id>/complete", methods=["POST"])
@login_required
def lesson_complete(id: int):
    """Dersi tamamla: UserProgress oluştur veya güncelle."""
    lesson = db.get_or_404(Lesson, id)

    # ai_score (AI quiz'den gelen puan) varsa öncelikli kullan;
    # yoksa form'daki manual score'a bak; her ikisi de 0-100 aralığına kısıtlanır
    try:
        ai_score_raw = request.form.get("ai_score")
        if ai_score_raw is not None:
            score = max(0, min(100, int(ai_score_raw)))
        else:
            score = max(0, min(100, int(request.form.get("score", 0))))
    except (TypeError, ValueError):
        score = 0

    progress = UserProgress.query.filter_by(
        user_id=current_user.id,
        lesson_id=lesson.id,
    ).first()

    if progress:
        progress.is_completed = True
        progress.score = score
        progress.completed_at = datetime.now(timezone.utc)
    else:
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson.id,
            is_completed=True,
            score=score,
            completed_at=datetime.now(timezone.utc),
        )
        db.session.add(progress)

    db.session.commit()
    flash("🎉 Ders başarıyla tamamlandı!", "success")
    return redirect(url_for("main.lesson_detail", id=lesson.id))


# ---------------------------------------------------------------------------
# Yeni Konu
# ---------------------------------------------------------------------------

@main.route("/topics/new", methods=["GET", "POST"])
@login_required
def topic_new():
    """Yeni konu oluşturma formu."""
    form = TopicForm()
    if form.validate_on_submit():
        topic = Topic(
            title=form.title.data,
            description=form.description.data or None,
            icon=form.icon.data or None,
            order=form.order.data or 0,
            user_id=current_user.id,
        )
        db.session.add(topic)
        db.session.commit()
        flash(f'✅ "{topic.title}" konusu oluşturuldu.', "success")
        return redirect(url_for("main.topic_detail", id=topic.id))

    return render_template(
        "main/topic_form.html",
        title="Yeni Konu",
        form=form,
        action="new",
    )


# ---------------------------------------------------------------------------
# Konu Düzenleme
# ---------------------------------------------------------------------------

@main.route("/topics/<int:id>/edit", methods=["GET", "POST"])
@login_required
def topic_edit(id: int):
    """Konu düzenleme formu. Yetki: konu sahibi."""
    topic = db.get_or_404(Topic, id)
    if topic.user_id is not None and topic.user_id != current_user.id:
        abort(403)

    form = TopicForm(obj=topic)
    if form.validate_on_submit():
        topic.title = form.title.data
        topic.description = form.description.data or None
        topic.icon = form.icon.data or None
        topic.order = form.order.data or 0
        db.session.commit()
        flash(f'✏️ "{topic.title}" konusu güncellendi.', "success")
        return redirect(url_for("main.topic_detail", id=topic.id))

    return render_template(
        "main/topic_form.html",
        title=f"{topic.title} — Düzenle",
        form=form,
        action="edit",
        topic=topic,
    )


# ---------------------------------------------------------------------------
# Konu Silme Onay
# ---------------------------------------------------------------------------

@main.route("/topics/<int:id>/delete-confirm")
@login_required
def topic_delete_confirm(id: int):
    """Silme onay sayfası. Yetki: konu sahibi."""
    topic = db.get_or_404(Topic, id)
    if topic.user_id is not None and topic.user_id != current_user.id:
        abort(403)

    # CSRF token için boş bir FlaskForm instance'ı
    from flask_wtf import FlaskForm
    form = FlaskForm()
    return render_template(
        "main/confirm_delete.html",
        title=f'"{topic.title}" Silinsin mi?',
        topic=topic,
        form=form,
    )


# ---------------------------------------------------------------------------
# Konu Silme
# ---------------------------------------------------------------------------

@main.route("/topics/<int:id>/delete", methods=["POST"])
@login_required
def topic_delete(id: int):
    """Konuyu sil. Yetki: konu sahibi."""
    topic = db.get_or_404(Topic, id)
    if topic.user_id is not None and topic.user_id != current_user.id:
        abort(403)

    title = topic.title
    db.session.delete(topic)
    db.session.commit()
    flash(f'🗑️ "{title}" konusu silindi.', "success")
    return redirect(url_for("main.topics"))


# ---------------------------------------------------------------------------
# Konuya Ders Ekleme
# ---------------------------------------------------------------------------

@main.route("/topics/<int:id>/lessons/new", methods=["GET", "POST"])
@login_required
def lesson_new(id: int):
    """Konuya yeni ders ekle."""
    topic = db.get_or_404(Topic, id)
    form = LessonForm()
    if form.validate_on_submit():
        lesson = Lesson(
            title=form.title.data,
            content=form.content.data,
            difficulty=form.difficulty.data,
            order=form.order.data or 0,
            topic_id=topic.id,
        )
        db.session.add(lesson)
        db.session.commit()
        flash(f'📚 "{lesson.title}" dersi eklendi.', "success")
        return redirect(url_for("main.topic_detail", id=topic.id))

    return render_template(
        "main/lesson_form.html",
        title=f"{topic.title} — Yeni Ders",
        form=form,
        topic=topic,
    )


# ---------------------------------------------------------------------------
# Hata Handler'ları
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
