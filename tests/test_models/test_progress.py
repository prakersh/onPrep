import pytest
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError
from app.models import Progress, Deadline, ScheduleItem


class TestProgress:
    def test_create_progress(self, db, sample_question):
        p = Progress(question_id=sample_question.id, status='not_started')
        db.session.add(p)
        db.session.commit()
        assert p.id is not None
        assert p.status == 'not_started'
        assert p.confidence == 0
        assert p.times_reviewed == 0

    def test_unique_question_constraint(self, db, sample_question):
        p1 = Progress(question_id=sample_question.id, status='not_started')
        p2 = Progress(question_id=sample_question.id, status='completed')
        db.session.add(p1)
        db.session.commit()
        db.session.add(p2)
        with pytest.raises(IntegrityError):
            db.session.commit()

    def test_progress_linked_to_question(self, db, sample_question):
        p = Progress(question_id=sample_question.id, status='completed', confidence=4)
        db.session.add(p)
        db.session.commit()
        assert p.question == sample_question
        assert sample_question.progress == p


class TestDeadline:
    def test_create_deadline(self, db, sample_language):
        d = Deadline(
            language_id=sample_language.id,
            interview_date=date.today() + timedelta(days=30),
            is_active=True,
        )
        db.session.add(d)
        db.session.commit()
        assert d.id is not None
        assert d.is_active is True

    def test_toggle_active(self, db, sample_language):
        d = Deadline(
            language_id=sample_language.id,
            interview_date=date.today() + timedelta(days=30),
            is_active=True,
        )
        db.session.add(d)
        db.session.commit()
        d.is_active = False
        db.session.commit()
        assert d.is_active is False


class TestScheduleItem:
    def test_create_schedule_item(self, db, sample_language, sample_concept):
        d = Deadline(
            language_id=sample_language.id,
            interview_date=date.today() + timedelta(days=30),
            is_active=True,
        )
        db.session.add(d)
        db.session.flush()
        item = ScheduleItem(
            deadline_id=d.id,
            concept_id=sample_concept.id,
            scheduled_date=date.today() + timedelta(days=1),
            is_review=False,
        )
        db.session.add(item)
        db.session.commit()
        assert item.id is not None
        assert item.concept == sample_concept
        assert item.deadline == d

    def test_schedule_items_ordered_by_date(self, db, sample_language, sample_concept, sample_concept_b):
        d = Deadline(
            language_id=sample_language.id,
            interview_date=date.today() + timedelta(days=30),
            is_active=True,
        )
        db.session.add(d)
        db.session.flush()
        item1 = ScheduleItem(
            deadline_id=d.id, concept_id=sample_concept.id,
            scheduled_date=date.today() + timedelta(days=3),
        )
        item2 = ScheduleItem(
            deadline_id=d.id, concept_id=sample_concept_b.id,
            scheduled_date=date.today() + timedelta(days=1),
        )
        db.session.add_all([item1, item2])
        db.session.commit()
        items = d.schedule_items
        dates = [i.scheduled_date for i in items]
        assert dates == sorted(dates)
