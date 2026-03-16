from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from app.extensions import db
from app.models import Progress, Question, Deadline, Concept
from app.services.scheduler import generate_schedule

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/progress', methods=['POST'])
def update_progress():
    data = request.get_json()
    question_id = data.get('question_id')
    status = data.get('status')

    if not question_id or not status:
        return jsonify({'error': 'question_id and status required'}), 400

    if status not in ('not_started', 'in_progress', 'completed'):
        return jsonify({'error': 'Invalid status'}), 400

    question = db.session.get(Question, question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    progress = db.session.query(Progress).filter_by(question_id=question_id).first()
    if not progress:
        progress = Progress(question_id=question_id)
        db.session.add(progress)

    progress.status = status
    progress.last_studied_at = datetime.now(timezone.utc)
    progress.times_reviewed = (progress.times_reviewed or 0) + 1
    db.session.commit()

    # Calculate concept progress
    concept = question.concept
    total = len(concept.questions)
    completed = sum(1 for q in concept.questions if q.progress and q.progress.status == 'completed')
    concept_pct = round(completed / total * 100) if total > 0 else 0

    return jsonify({'status': 'ok', 'concept_progress_pct': concept_pct})


@bp.route('/view', methods=['POST'])
def record_view():
    data = request.get_json()
    question_id = data.get('question_id')
    if not question_id:
        return jsonify({'status': 'ok'})

    progress = db.session.query(Progress).filter_by(question_id=question_id).first()
    if not progress:
        progress = Progress(question_id=question_id, status='in_progress')
        db.session.add(progress)
    progress.last_studied_at = datetime.now(timezone.utc)
    progress.times_reviewed = (progress.times_reviewed or 0) + 1
    if progress.status == 'not_started':
        progress.status = 'in_progress'
    db.session.commit()
    return jsonify({'status': 'ok'})


@bp.route('/confidence', methods=['POST'])
def update_confidence():
    data = request.get_json()
    question_id = data.get('question_id')
    confidence = data.get('confidence')

    if not question_id or confidence is None:
        return jsonify({'error': 'question_id and confidence required'}), 400

    if not (1 <= confidence <= 5):
        return jsonify({'error': 'Confidence must be 1-5'}), 400

    progress = db.session.query(Progress).filter_by(question_id=question_id).first()
    if not progress:
        progress = Progress(question_id=question_id)
        db.session.add(progress)

    progress.confidence = confidence
    db.session.commit()

    return jsonify({'status': 'ok'})


@bp.route('/schedule/regenerate', methods=['POST'])
def regenerate_schedule():
    deadline = db.session.query(Deadline).filter_by(is_active=True).first()
    if not deadline:
        return jsonify({'error': 'No active deadline'}), 404

    # Clear existing schedule items
    for item in list(deadline.schedule_items):
        db.session.delete(item)
    db.session.flush()

    generate_schedule(deadline)
    db.session.commit()

    return jsonify({'status': 'ok'})
