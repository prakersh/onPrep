class TestPlannerSetup:
    def test_setup_page_renders(self, client, db, sample_language):
        """Setup page should render with language options."""
        resp = client.get('/planner/setup')
        assert resp.status_code == 200
        assert b'Interview Planner' in resp.data
        assert b'Python' in resp.data

    def test_setup_page_has_form(self, client, db, sample_language):
        """Setup page should have the add interview form."""
        resp = client.get('/planner/setup')
        assert resp.status_code == 200
        assert b'Add Interview' in resp.data
        assert b'interview_date' in resp.data

    def test_setup_page_has_localstorage_js(self, client, db, sample_language):
        """Setup page should use localStorage for deadlines."""
        resp = client.get('/planner/setup')
        assert resp.status_code == 200
        assert b'awesomeprep:deadlines' in resp.data

    def test_setup_page_passes_languages_as_json(self, client, db, sample_language):
        """Setup page should include language data for JS."""
        resp = client.get('/planner/setup')
        assert resp.status_code == 200
        assert b'python' in resp.data


class TestPlannerSchedule:
    def test_schedule_page_renders(self, client, db):
        """Schedule page should render (data comes from localStorage)."""
        resp = client.get('/planner/schedule')
        assert resp.status_code == 200
        assert b'Study Schedules' in resp.data

    def test_schedule_page_has_localstorage_js(self, client, db):
        """Schedule page should read from localStorage."""
        resp = client.get('/planner/schedule')
        assert resp.status_code == 200
        assert b'awesomeprep:deadlines' in resp.data

    def test_schedule_detail_page_renders(self, client, db):
        """Schedule detail page should render (data from localStorage via query param)."""
        resp = client.get('/planner/schedule/detail')
        assert resp.status_code == 200
        assert b'awesomeprep:deadlines' in resp.data
