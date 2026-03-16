class TestStudyLanguages:
    def test_languages_page(self, client, db, sample_language):
        resp = client.get('/study/languages')
        assert resp.status_code == 200
        assert b'Python' in resp.data


class TestStudyConcepts:
    def test_concept_list(self, client, db, sample_language, sample_concept):
        resp = client.get('/study/python')
        assert resp.status_code == 200
        assert b'Data Types' in resp.data

    def test_invalid_language_404(self, client, db):
        resp = client.get('/study/nonexistent')
        assert resp.status_code == 404


class TestStudyConceptDetail:
    def test_detailed_view_default(self, client, db, sample_language, sample_concept, sample_question, sample_answers):
        resp = client.get('/study/python/data-types-variables')
        assert resp.status_code == 200
        assert b'Switch to Quick Recap' in resp.data
        assert b'basic data types' in resp.data

    def test_quick_view(self, client, db, sample_language, sample_concept, sample_question, sample_answers):
        resp = client.get('/study/python/data-types-variables?mode=quick')
        assert resp.status_code == 200
        assert b'Switch to Detailed' in resp.data

    def test_invalid_concept_404(self, client, db, sample_language):
        resp = client.get('/study/python/nonexistent')
        assert resp.status_code == 404

    def test_related_concepts_shown(self, client, db, sample_language, sample_concept, sample_concept_b, sample_question, sample_answers):
        from app.models import ConceptRelationship
        rel = ConceptRelationship(
            concept_id=sample_concept.id,
            related_concept_id=sample_concept_b.id,
            relationship_type='related',
        )
        db.session.add(rel)
        db.session.commit()
        resp = client.get('/study/python/data-types-variables')
        assert b'Operators' in resp.data
