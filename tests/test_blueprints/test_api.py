class TestConceptsAPI:
    def test_concepts_endpoint_returns_json(self, client, db, sample_language, sample_concept):
        resp = client.get(f'/api/concepts/{sample_language.slug}')
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['slug'] == 'data-types-variables'
        assert data[0]['title'] == 'Data Types & Variables'
        assert data[0]['estimated_minutes'] == 30
        assert data[0]['display_order'] == 1

    def test_concepts_endpoint_unknown_language(self, client, db):
        resp = client.get('/api/concepts/unknown-lang')
        assert resp.status_code == 404
        data = resp.get_json()
        assert 'error' in data

    def test_concepts_ordered_by_display_order(self, client, db, sample_language, sample_concept, sample_concept_b):
        resp = client.get(f'/api/concepts/{sample_language.slug}')
        data = resp.get_json()
        assert len(data) == 2
        assert data[0]['display_order'] < data[1]['display_order']

    def test_concepts_endpoint_multiple_fields(self, client, db, sample_language, sample_concept):
        resp = client.get(f'/api/concepts/{sample_language.slug}')
        data = resp.get_json()
        item = data[0]
        assert 'slug' in item
        assert 'title' in item
        assert 'estimated_minutes' in item
        assert 'display_order' in item
