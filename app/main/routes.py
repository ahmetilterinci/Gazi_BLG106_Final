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
from app.main.forms import LessonForm, ProfileForm, TopicForm
from app.models import Lesson, Topic, UserProgress


# ---------------------------------------------------------------------------
# Ana Sayfa
# ---------------------------------------------------------------------------

@main.route("/")
def index():
    """Ana sayfa — giriş yapılmışsa öğrenme yolu verilerini hazırla."""
    topics_with_data = []
 
    if current_user.is_authenticated:
        # Tüm topic'leri sıraya göre çek
        all_topics = (
            Topic.query
            .order_by(Topic.order, Topic.id)
            .all()
        )
 
        # Tüm progress kayıtlarını tek sorguda çek
        all_lesson_ids = []
        topic_lessons_map = {}
        for topic in all_topics:
            lessons = (
                Lesson.query
                .filter_by(topic_id=topic.id)
                .order_by(Lesson.order, Lesson.id)
                .all()
            )
            topic_lessons_map[topic.id] = lessons
            all_lesson_ids.extend([l.id for l in lessons])
 
        progress_map: dict[int, "UserProgress"] = {}
        if all_lesson_ids:
            rows = UserProgress.query.filter(
                UserProgress.user_id == current_user.id,
                UserProgress.lesson_id.in_(all_lesson_ids),
            ).all()
            progress_map = {row.lesson_id: row for row in rows}
 
        # Kilit mantığı: topic N açık olmak için topic N-1 tamamen bitmeli
        prev_world_complete = True  # ilk dünya her zaman açık
        for topic in all_topics:
            lessons = topic_lessons_map[topic.id]
            total = len(lessons)
 
            completed_count = sum(
                1 for l in lessons
                if progress_map.get(l.id) and progress_map[l.id].is_completed
            )
 
            is_locked = not prev_world_complete
 
            # Sonraki topic için: bu topic tamamen bitti mi?
            prev_world_complete = (total > 0 and completed_count == total)
 
            topics_with_data.append({
                "topic": topic,
                "lessons": lessons,
                "is_locked": is_locked,
                "completed_count": completed_count,
                "total_count": total,
                "progress_map": progress_map,
            })
 
    return render_template(
        "main/index.html",
        title="Ana Sayfa",
        topics_with_data=topics_with_data,
    )


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
    """Ders içeriği. Giriş yapılmışsa kilitli derse erişimi engelle."""
    lesson = db.get_or_404(Lesson, id)
    progress = None
 
    if current_user.is_authenticated:
        # Kilitli dünya kontrolü: bu dersin topic'i kilitli mi?
        topic = lesson.topic
        all_topics = (
            Topic.query
            .order_by(Topic.order, Topic.id)
            .all()
        )
        topic_ids_ordered = [t.id for t in all_topics]
 
        try:
            topic_index = topic_ids_ordered.index(topic.id)
        except ValueError:
            topic_index = 0
 
        if topic_index > 0:
            # Önceki topic'in tüm dersleri tamamlanmış mı?
            prev_topic = all_topics[topic_index - 1]
            prev_lessons = (
                Lesson.query
                .filter_by(topic_id=prev_topic.id)
                .all()
            )
            prev_lesson_ids = [l.id for l in prev_lessons]
 
            if prev_lesson_ids:
                prev_completed = UserProgress.query.filter(
                    UserProgress.user_id == current_user.id,
                    UserProgress.lesson_id.in_(prev_lesson_ids),
                    UserProgress.is_completed == True,  # noqa: E712
                ).count()
 
                if prev_completed < len(prev_lesson_ids):
                    flash(
                        f'🔒 Bu derse erişmek için önce '
                        f'"{prev_topic.title}" dünyasını tamamlamalısın.',
                        "warning"
                    )
                    return redirect(url_for("main.index"))
 
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
    """Gemini ile 4 tipte soru üret. Kullanıcı performansına göre dağılım ayarla."""
    import google.generativeai as genai  # noqa: PLC0415
 
    lesson = db.get_or_404(Lesson, id)
 
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY tanımlı değil"}), 500
 
    # Kullanıcının bu dersteki geçmiş performansını çek
    progress = UserProgress.query.filter_by(
        user_id=current_user.id,
        lesson_id=lesson.id,
    ).first()
 
    prev_wrong   = progress.wrong_count if progress else 0
    prev_attempts = progress.attempts   if progress else 0
 
    # İçerik uzunluğuna göre toplam soru sayısı (min 8 — 4 tipten en az 2'şer)
    content_len = len(lesson.content or "")
    if content_len < 500:
        total_q = 8
    elif content_len < 1500:
        total_q = 10
    elif content_len < 3000:
        total_q = 12
    else:
        total_q = 14
 
    # Performansa göre tip dağılımı
    # Her tipten en az 1 tane ZORUNLU — kalan sorular dağılıma göre
    base = 1  # her tipten minimum
    extra = total_q - 4  # 4 tip * 1 = 4 zorunlu, kalan extra
 
    if prev_attempts == 0:
        # Yeni kullanıcı: mcq ağırlıklı, kolay tiplerle başla
        mcq_n       = base + round(extra * 0.5)
        tf_n        = base + round(extra * 0.2)
        fill_n      = base + round(extra * 0.2)
        match_n     = base + round(extra * 0.1)
    elif prev_wrong <= 2:
        # Az yanlış: dengeli dağılım
        mcq_n       = base + round(extra * 0.3)
        tf_n        = base + round(extra * 0.2)
        fill_n      = base + round(extra * 0.3)
        match_n     = base + round(extra * 0.2)
    else:
        # Çok yanlış: daha kolay tipler ağırlıklı (truefalse + fillblank)
        mcq_n       = base + round(extra * 0.2)
        tf_n        = base + round(extra * 0.35)
        fill_n      = base + round(extra * 0.35)
        match_n     = base + round(extra * 0.1)
 
    # Toplam tutarlılığı sağla
    calculated = mcq_n + tf_n + fill_n + match_n
    if calculated < total_q:
        mcq_n += total_q - calculated
 
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=(
                "Sen bir siber güvenlik eğitim asistanısın. "
                "Duolingo tarzı etkileşimli öğrenme için çeşitli tipte sorular hazırlıyorsun. "
                "Her soru önce kavramı öğretmeli, sonra test etmeli. "
                "YALNIZCA geçerli JSON döndür, başka hiçbir şey yazma, markdown bloğu kullanma. "
                "\n\nSoru tipleri ve JSON formatları:"
                "\n\n1) mcq (çoktan seçmeli):"
                '\n{"type":"mcq","hint":"3-4 cümle öğretici açıklama","question":"soru metni",'
                '"options":["A) ...","B) ...","C) ...","D) ..."],"correct_index":0,'
                '"explanation":"neden bu doğru"}'
                "\n\n2) truefalse (doğru/yanlış):"
                '\n{"type":"truefalse","hint":"3-4 cümle öğretici açıklama","statement":"iddia cümlesi",'
                '"correct":true,"explanation":"neden doğru/yanlış"}'
                "\n\n3) fillblank (boşluk doldurma):"
                '\n{"type":"fillblank","hint":"3-4 cümle öğretici açıklama",'
                '"sentence":"Cümlede ___ boşluk var","options":["A) ...","B) ...","C) ...","D) ..."],'
                '"correct_index":0,"explanation":"neden bu kelime doğru"}'
                "\n\n4) matching (eşleştirme — 4 çift):"
                '\n{"type":"matching","hint":"3-4 cümle öğretici açıklama","instruction":"Terimleri tanımlarıyla eşleştir",'
                '"pairs":[{"left":"terim1","right":"tanım1"},{"left":"terim2","right":"tanım2"},'
                '{"left":"terim3","right":"tanım3"},{"left":"terim4","right":"tanım4"}]}'
                "\n\nTüm soruları şu JSON içinde döndür:"
                '\n{"questions":[...sorular...]}'
            ),
        )
 
        difficulty_note = ""
        if prev_attempts > 0:
            difficulty_note = (
                f"\nNot: Bu kullanıcı bu dersi daha önce {prev_attempts} kez denedi "
                f"ve toplam {prev_wrong} yanlış yaptı. "
                f"{'Sorular biraz daha kolay olsun.' if prev_wrong > 3 else 'Dengeli zorluk seviyesi koru.'}"
            )
 
        prompt = (
            f"Ders Başlığı: {lesson.title}\n\n"
            f"Ders İçeriği:\n{lesson.content}\n\n"
            f"Aşağıdaki sayılarda soru üret:{difficulty_note}\n"
            f"- mcq (çoktan seçmeli): {mcq_n} adet\n"
            f"- truefalse (doğru/yanlış): {tf_n} adet\n"
            f"- fillblank (boşluk doldurma): {fill_n} adet\n"
            f"- matching (eşleştirme): {match_n} adet\n\n"
            f"Toplam {total_q} soru. Her sorunun hint alanı o kavramı gerçekten öğretmeli "
            f"(sadece ipucu değil, 3-4 cümle açıklama). "
            f"Soruları karıştırılmış sırada döndür, aynı tipten arka arkaya gelmesin."
        )
 
        response = model.generate_content(prompt)
        raw = (
            response.text.strip()
            .removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )
        data = json.loads(raw)
        if isinstance(data, list):
            data = {"questions": data}
 
        return jsonify(data), 200
 
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
 
    try:
        ai_score_raw = request.form.get("ai_score")
        if ai_score_raw is not None:
            score = max(0, min(100, int(ai_score_raw)))
        else:
            score = max(0, min(100, int(request.form.get("score", 0))))
    except (TypeError, ValueError):
        score = 0
 
    # wrong_count ve attempts form'dan al
    try:
        session_wrong = max(0, int(request.form.get("wrong_count", 0)))
    except (TypeError, ValueError):
        session_wrong = 0
 
    progress = UserProgress.query.filter_by(
        user_id=current_user.id,
        lesson_id=lesson.id,
    ).first()
 
    if progress:
        progress.is_completed  = True
        progress.score         = score
        progress.completed_at  = datetime.now(timezone.utc)
        progress.attempts      = (progress.attempts or 0) + 1
        progress.wrong_count   = (progress.wrong_count or 0) + session_wrong
    else:
        progress = UserProgress(
            user_id      = current_user.id,
            lesson_id    = lesson.id,
            is_completed = True,
            score        = score,
            completed_at = datetime.now(timezone.utc),
            attempts     = 1,
            wrong_count  = session_wrong,
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
# Kullanıcı Profili
# ---------------------------------------------------------------------------

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Kullanıcı profil sayfası — bio ve avatar düzenleme + istatistikler."""
    from app.models import User  # noqa: PLC0415

    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.bio = form.bio.data or None
        current_user.avatar_url = form.avatar_url.data or None
        db.session.commit()
        flash("✅ Profilin başarıyla güncellendi.", "success")
        return redirect(url_for("main.profile"))

    if form.errors:
        flash("⚠️ Formda hatalar var, lütfen kontrol et.", "danger")

    # İstatistikler
    completed_lessons = UserProgress.query.filter_by(
        user_id=current_user.id,
        is_completed=True,
    ).all()
    total_completed = len(completed_lessons)
    total_score = sum(p.score or 0 for p in completed_lessons)

    return render_template(
        "main/profile.html",
        title=f"{current_user.username} — Profil",
        form=form,
        total_completed=total_completed,
        total_score=total_score,
    )


@main.route("/profile/avatar", methods=["POST"])
@login_required
def profile_avatar():
    """Sadece avatar_url günceller — profile.html'deki ayrı form action'ı."""
    avatar_url = request.form.get("avatar_url", "").strip()
    if avatar_url:
        current_user.avatar_url = avatar_url
        db.session.commit()
        flash("🎨 Avatar güncellendi.", "success")
    else:
        current_user.avatar_url = None
        db.session.commit()
        flash("Avatar temizlendi.", "success")
    return redirect(url_for("main.profile"))


# ---------------------------------------------------------------------------
# Public REST API — v1
# ---------------------------------------------------------------------------

@main.route("/api/v1/topics")
def api_topics():
    """GET /api/v1/topics — Tüm topic'leri JSON olarak döndür."""
    topics = (
        Topic.query
        .order_by(Topic.order, Topic.id)
        .all()
    )
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "icon": t.icon,
            "order": t.order,
        }
        for t in topics
    ])


@main.route("/api/v1/topics/<int:id>")
def api_topic_detail(id: int):
    """GET /api/v1/topics/<id> — Tek topic + dersleri JSON olarak döndür."""
    topic = db.session.get(Topic, id)
    if topic is None:
        return jsonify({"error": "Not found"}), 404

    lessons = (
        Lesson.query
        .filter_by(topic_id=topic.id)
        .order_by(Lesson.order, Lesson.id)
        .all()
    )
    return jsonify({
        "id": topic.id,
        "title": topic.title,
        "description": topic.description,
        "icon": topic.icon,
        "order": topic.order,
        "lessons": [
            {
                "id": l.id,
                "title": l.title,
                "difficulty": l.difficulty,
                "order": l.order,
            }
            for l in lessons
        ],
    })


@main.route("/api/v1/lessons/<int:id>")
def api_lesson_detail(id: int):
    """GET /api/v1/lessons/<id> — Tek ders JSON olarak döndür."""
    lesson = db.session.get(Lesson, id)
    if lesson is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": lesson.id,
        "title": lesson.title,
        "content": lesson.content,
        "difficulty": lesson.difficulty,
        "order": lesson.order,
        "topic_id": lesson.topic_id,
    })


# ---------------------------------------------------------------------------
# Statik Sayfalar
# ---------------------------------------------------------------------------

@main.route("/about")
def about():
    return render_template("main/about.html", title="Hakkında — CyberLearn.io")


@main.route("/faq")
def faq():
    return render_template("main/faq.html", title="S.S.S. — CyberLearn.io")


@main.route("/contact")
def contact():
    return render_template("main/contact.html", title="İletişim — CyberLearn.io")

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





