from flask import Blueprint, render_template
from datetime import date
from app.extensions import db
from app.models import Language, Progress, Question, Deadline, ScheduleItem, Concept

bp = Blueprint('dashboard', __name__)


@bp.route('/')
def index():
    total_questions = db.session.query(Question).count()
    completed = db.session.query(Progress).filter_by(status='completed').count()
    in_progress = db.session.query(Progress).filter_by(status='in_progress').count()
    progress_pct = round((completed / total_questions * 100) if total_questions > 0 else 0)

    # All active deadlines sorted by date
    deadlines = (
        db.session.query(Deadline)
        .filter_by(is_active=True)
        .order_by(Deadline.interview_date)
        .all()
    )

    # Compute days remaining for each
    deadline_data = []
    for d in deadlines:
        days_remaining = (d.interview_date - date.today()).days
        deadline_data.append({'deadline': d, 'days_remaining': days_remaining})

    # Today's items across all deadlines
    today_items = []
    for d in deadlines:
        items = (
            db.session.query(ScheduleItem)
            .filter_by(deadline_id=d.id, scheduled_date=date.today())
            .all()
        )
        for item in items:
            today_items.append({'item': item, 'deadline': d})

    # Languages
    languages = db.session.query(Language).filter_by(is_active=True).order_by(Language.display_order).all()

    # Per-difficulty stats
    difficulty_stats = []
    for diff in ['beginner', 'intermediate', 'advanced']:
        concepts = db.session.query(Concept).filter_by(difficulty=diff).all()
        total_q = sum(len(c.questions) for c in concepts)
        done_q = 0
        for c in concepts:
            for q in c.questions:
                if q.progress and q.progress.status == 'completed':
                    done_q += 1
        pct = round(done_q / total_q * 100) if total_q > 0 else 0
        difficulty_stats.append({'difficulty': diff, 'total': total_q, 'done': done_q, 'pct': pct})

    # Recently studied (last 5)
    recent = (
        db.session.query(Progress)
        .filter(Progress.last_studied_at.isnot(None))
        .order_by(Progress.last_studied_at.desc())
        .limit(5)
        .all()
    )

    # Concepts with progress for language breakdown
    language_stats = []
    for lang in languages:
        total_q = sum(len(c.questions) for c in lang.concepts)
        done_q = 0
        for c in lang.concepts:
            for q in c.questions:
                if q.progress and q.progress.status == 'completed':
                    done_q += 1
        pct = round(done_q / total_q * 100) if total_q > 0 else 0
        language_stats.append({
            'language': lang,
            'total': total_q,
            'done': done_q,
            'pct': pct,
            'concept_count': len(lang.concepts),
        })

    return render_template(
        'dashboard/index.html',
        progress_pct=progress_pct,
        total_questions=total_questions,
        completed=completed,
        in_progress=in_progress,
        deadline_data=deadline_data,
        today_items=today_items,
        languages=languages,
        difficulty_stats=difficulty_stats,
        recent=recent,
        language_stats=language_stats,
    )
