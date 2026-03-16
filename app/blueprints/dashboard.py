from flask import Blueprint, render_template
from datetime import date, timezone, datetime
from app.extensions import db
from app.models import Language, Progress, Question, Deadline, ScheduleItem, Concept

bp = Blueprint('dashboard', __name__)


@bp.route('/')
def index():
    # Overall progress
    total_questions = db.session.query(Question).count()
    completed = db.session.query(Progress).filter_by(status='completed').count()
    progress_pct = round((completed / total_questions * 100) if total_questions > 0 else 0)

    # Active deadline
    active_deadline = db.session.query(Deadline).filter_by(is_active=True).first()
    days_remaining = None
    if active_deadline:
        days_remaining = (active_deadline.interview_date - date.today()).days

    # Today's scheduled concepts
    today_items = []
    if active_deadline:
        today_items = (
            db.session.query(ScheduleItem)
            .filter_by(deadline_id=active_deadline.id, scheduled_date=date.today())
            .all()
        )

    # Languages
    languages = db.session.query(Language).filter_by(is_active=True).order_by(Language.display_order).all()

    return render_template(
        'dashboard/index.html',
        progress_pct=progress_pct,
        total_questions=total_questions,
        completed=completed,
        active_deadline=active_deadline,
        days_remaining=days_remaining,
        today_items=today_items,
        languages=languages,
    )
