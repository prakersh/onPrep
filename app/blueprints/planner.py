from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date, datetime
from app.extensions import db
from app.models import Language, Deadline, ScheduleItem
from app.services.scheduler import generate_schedule

bp = Blueprint('planner', __name__, url_prefix='/planner')


@bp.route('/setup', methods=['GET'])
def setup():
    languages = db.session.query(Language).filter_by(is_active=True).order_by(Language.display_order).all()
    return render_template('planner/setup.html', languages=languages)


@bp.route('/setup', methods=['POST'])
def create_deadline():
    language_id = request.form.get('language_id', type=int)
    interview_date_str = request.form.get('interview_date')

    if not language_id or not interview_date_str:
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('planner.setup'))

    interview_date = datetime.strptime(interview_date_str, '%Y-%m-%d').date()

    if interview_date <= date.today():
        flash('Interview date must be in the future.', 'error')
        return redirect(url_for('planner.setup'))

    # Deactivate previous deadlines
    db.session.query(Deadline).filter_by(is_active=True).update({'is_active': False})

    deadline = Deadline(language_id=language_id, interview_date=interview_date, is_active=True)
    db.session.add(deadline)
    db.session.flush()

    generate_schedule(deadline)
    db.session.commit()

    return redirect(url_for('planner.schedule'))


@bp.route('/schedule')
def schedule():
    deadline = db.session.query(Deadline).filter_by(is_active=True).first()
    items = []
    if deadline:
        items = deadline.schedule_items
    return render_template('planner/schedule.html', deadline=deadline, items=items)
