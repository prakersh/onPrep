class TestHome:
    def test_home_redirect_page(self, client):
        """/ serves a JS redirect page."""
        resp = client.get('/')
        assert resp.status_code == 200
        assert b'awesomeprep:visited' in resp.data


class TestLanding:
    def test_landing_page(self, client):
        resp = client.get('/landing')
        assert resp.status_code == 200
        assert b'awesomePrep' in resp.data
        assert b'Start Studying' in resp.data

    def test_landing_with_content(self, client, db, sample_language, sample_concept, sample_question):
        resp = client.get('/landing')
        assert resp.status_code == 200
        assert b'Python' in resp.data


class TestDashboard:
    def test_dashboard_empty_state(self, client):
        resp = client.get('/dashboard')
        assert resp.status_code == 200
        assert b'Welcome to' in resp.data and b'awesomePrep' in resp.data

    def test_dashboard_renders_with_content(self, client, db, sample_language, sample_concept, sample_question):
        resp = client.get('/dashboard')
        assert resp.status_code == 200
        assert b'Dashboard' in resp.data
        assert b'Python' in resp.data

    def test_dashboard_no_server_deadlines(self, client, db, sample_language, sample_concept, sample_question):
        """Dashboard should use localStorage for deadlines, not server data."""
        resp = client.get('/dashboard')
        assert resp.status_code == 200
        assert b'awesomeprep:deadlines' in resp.data

    def test_dashboard_difficulty_stats(self, client, db, sample_language, sample_concept, sample_question):
        resp = client.get('/dashboard')
        assert resp.status_code == 200
        assert b'beginner' in resp.data

    def test_dashboard_includes_progress_js(self, client, db, sample_language, sample_concept, sample_question):
        resp = client.get('/dashboard')
        assert resp.status_code == 200
        assert b'awesomePrepProgress' in resp.data
