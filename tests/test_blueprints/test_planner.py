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
            'company_name': 'Google',
            'role': 'SWE',
        }, follow_redirects=True)
        assert resp.status_code == 200
        deadline = db.session.query(Deadline).first()
        assert deadline is not None
        assert deadline.company_name == 'Google'
        assert deadline.is_active is True

    def test_multiple_deadlines_supported(self, client, db, sample_language, sample_concept):
        future1 = (date.today() + timedelta(days=30)).isoformat()
        future2 = (date.today() + timedelta(days=60)).isoformat()
        client.post('/planner/setup', data={
            'language_id': sample_language.id,
            'interview_date': future1,
            'company_name': 'Google',
        })
        client.post('/planner/setup', data={
            'language_id': sample_language.id,
            'interview_date': future2,
            'company_name': 'Meta',
        })
        deadlines = db.session.query(Deadline).filter_by(is_active=True).all()
        assert len(deadlines) == 2

    def test_delete_deadline(self, client, db, sample_language, sample_concept):
        future = (date.today() + timedelta(days=30)).isoformat()
        client.post('/planner/setup', data={
            'language_id': sample_language.id,
            'interview_date': future,
            'company_name': 'Test',
        })
        deadline = db.session.query(Deadline).first()
        resp = client.post(f'/planner/delete/{deadline.id}', follow_redirects=True)
        assert resp.status_code == 200
        assert db.session.query(Deadline).count() == 0


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
            'company_name': 'TestCorp',
        })
        resp = client.get('/planner/schedule')
        assert resp.status_code == 200
        assert b'TestCorp' in resp.data

    def test_schedule_detail(self, client, db, sample_language, sample_concept):
        future = (date.today() + timedelta(days=30)).isoformat()
        client.post('/planner/setup', data={
            'language_id': sample_language.id,
            'interview_date': future,
            'company_name': 'Amazon',
        })
        deadline = db.session.query(Deadline).first()
        resp = client.get(f'/planner/schedule/{deadline.id}')
        assert resp.status_code == 200
        assert b'Amazon' in resp.data
