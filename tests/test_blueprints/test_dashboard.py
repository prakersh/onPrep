from datetime import date, timedelta
from app.models import Progress, Deadline, ScheduleItem


class TestDashboard:
    def test_dashboard_empty_state(self, client):
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'Welcome to onPrep' in resp.data

    def test_dashboard_shows_progress(self, client, db, sample_language, sample_concept, sample_question):
        p = Progress(question_id=sample_question.id, status='completed')
        db.session.add(p)
        db.session.commit()
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'100%' in resp.data

    def test_dashboard_shows_deadline_countdown(self, client, db, sample_language, sample_concept, sample_question):
        d = Deadline(
            language_id=sample_language.id,
            interview_date=date.today() + timedelta(days=10),
            is_active=True,
        )
        db.session.add(d)
        db.session.commit()
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'10 days' in resp.data

    def test_dashboard_shows_todays_items(self, client, db, sample_language, sample_concept, sample_question):
        d = Deadline(
            language_id=sample_language.id,
            interview_date=date.today() + timedelta(days=10),
            is_active=True,
        )
        db.session.add(d)
        db.session.flush()
        item = ScheduleItem(
            deadline_id=d.id,
            concept_id=sample_concept.id,
            scheduled_date=date.today(),
        )
        db.session.add(item)
        db.session.commit()
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'Data Types' in resp.data
