from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date, datetime
from app.extensions import db
from app.models import Language, Deadline, ScheduleItem
from app.services.scheduler import generate_schedule

bp = Blueprint('planner', __name__, url_prefix='/planner')

COLORS = ['indigo', 'emerald', 'rose', 'amber', 'cyan', 'violet', 'orange', 'teal']


@bp.route('/setup', methods=['GET'])
def setup():
    languages = db.session.query(Language).filter_by(is_active=True).order_by(Language.display_order).all()
    deadlines = (
        db.session.query(Deadline)
        .filter_by(is_active=True)
        .order_by(Deadline.interview_date)
        .all()
    )
    from datetime import date as _date
    return render_template('planner/setup.html', languages=languages, deadlines=deadlines, _today=_date.today())


@bp.route('/setup', methods=['POST'])
def create_deadline():
    language_id = request.form.get('language_id', type=int)
    interview_date_str = request.form.get('interview_date')
    company_name = request.form.get('company_name', '').strip()
    role = request.form.get('role', '').strip()

    if not language_id or not interview_date_str:
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('planner.setup'))

    interview_date = datetime.strptime(interview_date_str, '%Y-%m-%d').date()

    if interview_date <= date.today():
        flash('Interview date must be in the future.', 'error')
        return redirect(url_for('planner.setup'))

    # Pick a color based on how many active deadlines exist
    active_count = db.session.query(Deadline).filter_by(is_active=True).count()
    color = COLORS[active_count % len(COLORS)]

    deadline = Deadline(
        language_id=language_id,
        interview_date=interview_date,
        company_name=company_name or 'Interview',
        role=role,
        is_active=True,
        color=color,
    )
    db.session.add(deadline)
    db.session.flush()

    generate_schedule(deadline)
    db.session.commit()

    return redirect(url_for('planner.setup'))


@bp.route('/delete/<int:deadline_id>', methods=['POST'])
def delete_deadline(deadline_id):
    deadline = db.session.get(Deadline, deadline_id)
    if deadline:
        db.session.delete(deadline)
        db.session.commit()
    return redirect(url_for('planner.setup'))


@bp.route('/schedule')
def schedule():
    deadlines = (
        db.session.query(Deadline)
        .filter_by(is_active=True)
        .order_by(Deadline.interview_date)
        .all()
    )
    return render_template('planner/schedule.html', deadlines=deadlines)


@bp.route('/schedule/<int:deadline_id>')
def schedule_detail(deadline_id):
    deadline = db.session.get(Deadline, deadline_id)
    if not deadline:
        return redirect(url_for('planner.schedule'))
    return render_template('planner/schedule_detail.html', deadline=deadline)
