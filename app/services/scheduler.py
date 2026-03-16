from datetime import date, timedelta
from app.extensions import db
from app.models import Concept, ScheduleItem, Progress, Question


def generate_schedule(deadline):
    """Generate a study schedule for the given deadline.

    Assigns concepts to available days between now and interview date.
    Last day is reserved for review. Completed concepts are excluded.
    """
    today = date.today()
    interview_date = deadline.interview_date

    if interview_date <= today:
        raise ValueError('Interview date must be in the future')

    available_days = (interview_date - today).days
    if available_days < 1:
        raise ValueError('Interview date must be in the future')

    # Get concepts for this language ordered by display_order
    concepts = (
        db.session.query(Concept)
        .filter_by(language_id=deadline.language_id)
        .order_by(Concept.display_order)
        .all()
    )

    # Exclude completed concepts
    incomplete_concepts = []
    for concept in concepts:
        question_ids = [q.id for q in concept.questions]
        if not question_ids:
            incomplete_concepts.append(concept)
            continue
        completed = (
            db.session.query(Progress)
            .filter(Progress.question_id.in_(question_ids), Progress.status == 'completed')
            .count()
        )
        if completed < len(question_ids):
            incomplete_concepts.append(concept)

    if not incomplete_concepts:
        return  # Nothing to schedule

    # Reserve last day for review
    study_days = available_days - 1 if available_days > 1 else available_days

    # Distribute concepts across study days
    if study_days <= 0:
        # All on day 1
        for concept in incomplete_concepts:
            item = ScheduleItem(
                deadline_id=deadline.id,
                concept_id=concept.id,
                scheduled_date=today + timedelta(days=1),
                is_review=False,
            )
            db.session.add(item)
    else:
        concepts_per_day = max(1, len(incomplete_concepts) // study_days)
        day_offset = 1
        for i, concept in enumerate(incomplete_concepts):
            scheduled = today + timedelta(days=day_offset)
            if scheduled >= interview_date:
                scheduled = interview_date - timedelta(days=1)
            item = ScheduleItem(
                deadline_id=deadline.id,
                concept_id=concept.id,
                scheduled_date=scheduled,
                is_review=False,
            )
            db.session.add(item)
            if (i + 1) % concepts_per_day == 0 and day_offset < study_days:
                day_offset += 1

    # Add review day on the last day (if more than 1 day available)
    if available_days > 1:
        for concept in incomplete_concepts:
            review_item = ScheduleItem(
                deadline_id=deadline.id,
                concept_id=concept.id,
                scheduled_date=interview_date,
                is_review=True,
            )
            db.session.add(review_item)
