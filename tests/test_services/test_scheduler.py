import pytest
from datetime import date, timedelta
from app.models import Language, Concept, Question, Progress, Deadline, ScheduleItem
from app.services.scheduler import generate_schedule


class TestScheduler:
    @pytest.fixture
    def language_with_concepts(self, db):
        lang = Language(name='Python', slug='python', display_order=1)
        db.session.add(lang)
        db.session.flush()
        for i in range(28):
            c = Concept(
                language_id=lang.id,
                title=f'Concept {i+1}',
                slug=f'concept-{i+1}',
                display_order=i+1,
                estimated_minutes=30,
            )
            db.session.add(c)
            db.session.flush()
            q = Question(concept_id=c.id, title=f'Q for concept {i+1}', display_order=1)
            db.session.add(q)
        db.session.commit()
        return lang

    def test_30_days_for_28_concepts(self, db, language_with_concepts):
        d = Deadline(
            language_id=language_with_concepts.id,
            interview_date=date.today() + timedelta(days=30),
            is_active=True,
        )
        db.session.add(d)
        db.session.flush()
        generate_schedule(d)
        db.session.commit()
        items = db.session.query(ScheduleItem).filter_by(deadline_id=d.id).all()
        assert len(items) > 28  # 28 study + review items

    def test_5_days_for_28_concepts(self, db, language_with_concepts):
        d = Deadline(
            language_id=language_with_concepts.id,
            interview_date=date.today() + timedelta(days=5),
            is_active=True,
        )
        db.session.add(d)
        db.session.flush()
        generate_schedule(d)
        db.session.commit()
        items = db.session.query(ScheduleItem).filter_by(deadline_id=d.id, is_review=False).all()
        assert len(items) == 28  # All concepts scheduled

    def test_1_day_available(self, db, language_with_concepts):
        d = Deadline(
            language_id=language_with_concepts.id,
            interview_date=date.today() + timedelta(days=1),
            is_active=True,
        )
        db.session.add(d)
        db.session.flush()
        generate_schedule(d)
        db.session.commit()
        items = db.session.query(ScheduleItem).filter_by(deadline_id=d.id).all()
        assert len(items) == 28
        # All on same day
        dates = set(i.scheduled_date for i in items)
        assert len(dates) == 1

    def test_excludes_completed_concepts(self, db, language_with_concepts):
        # Mark first concept's question as completed
        concepts = db.session.query(Concept).filter_by(language_id=language_with_concepts.id).order_by(Concept.display_order).all()
        first_q = concepts[0].questions[0]
        p = Progress(question_id=first_q.id, status='completed')
        db.session.add(p)
        db.session.flush()

        d = Deadline(
            language_id=language_with_concepts.id,
            interview_date=date.today() + timedelta(days=30),
            is_active=True,
        )
        db.session.add(d)
        db.session.flush()
        generate_schedule(d)
        db.session.commit()

        scheduled_concept_ids = set(
            i.concept_id for i in db.session.query(ScheduleItem).filter_by(deadline_id=d.id).all()
        )
        assert concepts[0].id not in scheduled_concept_ids

    def test_last_day_is_review(self, db, language_with_concepts):
        d = Deadline(
            language_id=language_with_concepts.id,
            interview_date=date.today() + timedelta(days=30),
            is_active=True,
        )
        db.session.add(d)
        db.session.flush()
        generate_schedule(d)
        db.session.commit()
        review_items = (
            db.session.query(ScheduleItem)
            .filter_by(deadline_id=d.id, is_review=True)
            .all()
        )
        assert len(review_items) > 0
        for item in review_items:
            assert item.scheduled_date == d.interview_date

    def test_past_date_raises_error(self, db, language_with_concepts):
        d = Deadline(
            language_id=language_with_concepts.id,
            interview_date=date.today() - timedelta(days=1),
            is_active=True,
        )
        db.session.add(d)
        db.session.flush()
        with pytest.raises(ValueError, match='future'):
            generate_schedule(d)
