from datetime import date, timedelta
from app.models import Deadline


class TestPlannerSetup:
    def test_setup_page(self, client, db, sample_language):
        resp = client.get('/planner/setup')
        assert resp.status_code == 200
        assert b'Interview Date' in resp.data

    def test_create_deadline(self, client, db, sample_language, sample_concept):
        future = (date.today() + timedelta(days=30)).isoformat()
        resp = client.post('/planner/setup', data={
            'language_id': sample_language.id,
            'interview_date': future,
        }, follow_redirects=True)
        assert resp.status_code == 200
        deadline = db.session.query(Deadline).first()
        assert deadline is not None
        assert deadline.is_active is True

    def test_new_deadline_deactivates_previous(self, client, db, sample_language, sample_concept):
        future1 = (date.today() + timedelta(days=30)).isoformat()
        future2 = (date.today() + timedelta(days=60)).isoformat()
        client.post('/planner/setup', data={
            'language_id': sample_language.id,
            'interview_date': future1,
        })
        client.post('/planner/setup', data={
            'language_id': sample_language.id,
            'interview_date': future2,
        })
        deadlines = db.session.query(Deadline).all()
        active = [d for d in deadlines if d.is_active]
        assert len(active) == 1
        assert active[0].interview_date == date.today() + timedelta(days=60)


class TestPlannerSchedule:
    def test_schedule_page_no_deadline(self, client, db):
        resp = client.get('/planner/schedule')
        assert resp.status_code == 200
        assert b'No active schedule' in resp.data

    def test_schedule_page_with_items(self, client, db, sample_language, sample_concept):
        future = (date.today() + timedelta(days=30)).isoformat()
        client.post('/planner/setup', data={
            'language_id': sample_language.id,
            'interview_date': future,
        })
        resp = client.get('/planner/schedule')
        assert resp.status_code == 200
        assert b'Data Types' in resp.data
