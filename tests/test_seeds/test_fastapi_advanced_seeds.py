"""Tests to validate FastAPI advanced seed JSON files conform to the expected schema and quality standards."""

import json
import os
import pytest


SEEDS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'seeds', 'fastapi')

EXPECTED_FILES = [
    ('12_websockets_realtime.json', 'websockets-realtime', 12),
    ('13_background_tasks_events.json', 'background-tasks-events', 12),
    ('14_performance_optimization.json', 'performance-optimization', 15),
    ('15_deployment_production.json', 'deployment-production', 15),
]

REQUIRED_ANSWER_FIELDS = ['mode', 'explanation', 'actual_code', 'code_language', 'key_points', 'gotchas']
REQUIRED_QUESTION_FIELDS = ['title', 'display_order', 'difficulty', 'tags', 'answers']


def load_seed_file(filename: str) -> dict:
    """Load and parse a seed JSON file."""
    filepath = os.path.join(SEEDS_DIR, filename)
    with open(filepath, 'r') as f:
        return json.load(f)


def load_meta() -> dict:
    """Load the _meta.json file."""
    meta_path = os.path.join(SEEDS_DIR, '_meta.json')
    with open(meta_path, 'r') as f:
        return json.load(f)


class TestFastAPIAdvancedFilesExist:
    """Verify all 4 advanced seed files exist and are valid JSON."""

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_file_exists(self, filename: str, slug: str, count: int) -> None:
        filepath = os.path.join(SEEDS_DIR, filename)
        assert os.path.exists(filepath), f'{filename} does not exist'

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_valid_json(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        assert isinstance(data, dict)


class TestFastAPIAdvancedSchema:
    """Verify each seed file conforms to the required schema."""

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_concept_slug_matches(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        assert data['concept_slug'] == slug

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_concept_slug_in_meta(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        meta = load_meta()
        meta_slugs = [c['slug'] for c in meta['concepts']]
        assert data['concept_slug'] in meta_slugs, f'{data["concept_slug"]} not found in _meta.json'

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_question_count(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        actual_count = len(data['questions'])
        assert actual_count == count, f'{filename}: expected {count} questions, got {actual_count}'

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_questions_have_required_fields(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        for i, q in enumerate(data['questions']):
            for field in REQUIRED_QUESTION_FIELDS:
                assert field in q, f'{filename} Q{i+1} missing field: {field}'

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_display_order_sequential(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        orders = [q['display_order'] for q in data['questions']]
        assert orders == list(range(1, len(orders) + 1)), f'{filename}: display_order not sequential from 1'


class TestFastAPIAdvancedAnswers:
    """Verify each question has proper dual-mode answers."""

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_dual_mode_answers(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        for i, q in enumerate(data['questions']):
            modes = {a['mode'] for a in q['answers']}
            assert modes == {'detailed', 'quick'}, (
                f'{filename} Q{i+1} ("{q["title"]}") must have both detailed and quick answers, got {modes}'
            )

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_answers_have_required_fields(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                for field in REQUIRED_ANSWER_FIELDS:
                    assert field in a, f'{filename} Q{i+1} {a["mode"]} answer missing: {field}'

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_code_language_is_python(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                assert a['code_language'] == 'python', (
                    f'{filename} Q{i+1} {a["mode"]}: code_language must be "python", got "{a["code_language"]}"'
                )

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_gotchas_not_empty(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                assert len(a['gotchas']) > 0, (
                    f'{filename} Q{i+1} {a["mode"]}: gotchas must not be empty'
                )

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_key_points_not_empty(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                assert len(a['key_points']) > 0, (
                    f'{filename} Q{i+1} {a["mode"]}: key_points must not be empty'
                )

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_detailed_has_pseudo_code(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        for i, q in enumerate(data['questions']):
            detailed = [a for a in q['answers'] if a['mode'] == 'detailed']
            for a in detailed:
                assert 'pseudo_code' in a, f'{filename} Q{i+1} detailed answer missing pseudo_code'
                assert len(a['pseudo_code']) > 0, f'{filename} Q{i+1} detailed pseudo_code is empty'

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_actual_code_not_empty(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                assert len(a['actual_code'].strip()) > 0, (
                    f'{filename} Q{i+1} {a["mode"]}: actual_code is empty'
                )

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_difficulty_valid(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        valid_difficulties = {'beginner', 'intermediate', 'advanced'}
        for i, q in enumerate(data['questions']):
            assert q['difficulty'] in valid_difficulties, (
                f'{filename} Q{i+1}: difficulty "{q["difficulty"]}" not in {valid_difficulties}'
            )

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_tags_minimum_three(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        for i, q in enumerate(data['questions']):
            assert len(q['tags']) >= 3, f'{filename} Q{i+1}: must have at least 3 tags, got {len(q["tags"])}'

    @pytest.mark.parametrize('filename,slug,count', EXPECTED_FILES)
    def test_detailed_key_points_minimum_two(self, filename: str, slug: str, count: int) -> None:
        data = load_seed_file(filename)
        for i, q in enumerate(data['questions']):
            detailed = [a for a in q['answers'] if a['mode'] == 'detailed']
            for a in detailed:
                assert len(a['key_points']) >= 2, (
                    f'{filename} Q{i+1} detailed: must have at least 2 key_points, got {len(a["key_points"])}'
                )
