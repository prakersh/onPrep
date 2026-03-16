import json
from datetime import date, timedelta
from app.models import Progress, Deadline


class TestProgressAPI:
    def test_update_progress(self, client, db, sample_language, sample_concept, sample_question):
        resp = client.post('/api/progress', json={
            'question_id': sample_question.id,
            'status': 'completed',
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'ok'
        assert data['concept_progress_pct'] == 100

    def test_update_progress_creates_record(self, client, db, sample_language, sample_concept, sample_question):
        client.post('/api/progress', json={
            'question_id': sample_question.id,
            'status': 'in_progress',
        })
        p = db.session.query(Progress).filter_by(question_id=sample_question.id).first()
        assert p is not None
        assert p.status == 'in_progress'

    def test_update_progress_missing_fields(self, client, db):
        resp = client.post('/api/progress', json={'question_id': 1})
        assert resp.status_code == 400

    def test_update_progress_invalid_status(self, client, db, sample_question):
        resp = client.post('/api/progress', json={
            'question_id': sample_question.id,
            'status': 'invalid',
        })
        assert resp.status_code == 400

    def test_update_progress_question_not_found(self, client, db):
        resp = client.post('/api/progress', json={
            'question_id': 9999,
            'status': 'completed',
        })
        assert resp.status_code == 404


class TestConfidenceAPI:
    def test_update_confidence(self, client, db, sample_question):
        resp = client.post('/api/confidence', json={
            'question_id': sample_question.id,
            'confidence': 4,
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'ok'

    def test_confidence_out_of_range(self, client, db, sample_question):
        resp = client.post('/api/confidence', json={
            'question_id': sample_question.id,
            'confidence': 6,
        })
        assert resp.status_code == 400

    def test_confidence_missing_fields(self, client, db):
        resp = client.post('/api/confidence', json={'question_id': 1})
        assert resp.status_code == 400


class TestScheduleRegenerateAPI:
    def test_regenerate_no_deadline(self, client, db):
        resp = client.post('/api/schedule/regenerate')
        assert resp.status_code == 404

    def test_regenerate_schedule(self, client, db, sample_language, sample_concept):
        d = Deadline(
            language_id=sample_language.id,
            interview_date=date.today() + timedelta(days=30),
            is_active=True,
        )
        db.session.add(d)
        db.session.commit()
        resp = client.post('/api/schedule/regenerate')
        assert resp.status_code == 200
        assert resp.get_json()['status'] == 'ok'
