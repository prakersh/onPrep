from datetime import date, timedelta
from app.models import Deadline


class TestDashboard:
    def test_dashboard_empty_state(self, client):
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'Welcome to' in resp.data and b'awesomePrep' in resp.data

    def test_dashboard_renders_with_content(self, client, db, sample_language, sample_concept, sample_question):
        """Dashboard renders when content exists (progress is now client-side)."""
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'Dashboard' in resp.data
        assert b'Python' in resp.data

    def test_dashboard_shows_deadlines(self, client, db, sample_language, sample_concept, sample_question):
        d = Deadline(
            language_id=sample_language.id,
            company_name='Google',
            interview_date=date.today() + timedelta(days=10),
            is_active=True,
        )
        db.session.add(d)
        db.session.commit()
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'Google' in resp.data

    def test_dashboard_difficulty_stats(self, client, db, sample_language, sample_concept, sample_question):
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'beginner' in resp.data

    def test_dashboard_includes_progress_js(self, client, db, sample_language, sample_concept, sample_question):
        """Dashboard includes localStorage hydration script."""
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'awesomePrepProgress' in resp.data
