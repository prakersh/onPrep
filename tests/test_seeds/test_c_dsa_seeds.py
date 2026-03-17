"""Tests for C DSA seed files (12-15): linked lists, stacks/queues/trees, sorting/searching, bitwise.

Validates structure, completeness, and correctness of seed data
before it gets loaded into the database.
"""

import json
import os
import pytest

SEEDS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'seeds', 'c'
)

REQUIRED_FILES = {
    '12_linked_lists.json': {
        'concept_slug': 'linked-lists',
        'expected_count': 15,
        'difficulty': 'intermediate',
    },
    '13_stacks_queues_trees.json': {
        'concept_slug': 'stacks-queues-trees',
        'expected_count': 15,
        'difficulty': 'intermediate',
    },
    '14_sorting_searching.json': {
        'concept_slug': 'sorting-searching',
        'expected_count': 15,
        'difficulty': 'intermediate',
    },
    '15_bitwise_operations.json': {
        'concept_slug': 'bitwise-operations',
        'expected_count': 18,
        'difficulty': 'intermediate',
    },
}

ANSWER_REQUIRED_KEYS = {
    'mode', 'explanation', 'actual_code', 'code_language',
    'key_points', 'gotchas',
}


def load_seed(filename: str) -> dict:
    """Load and parse a seed JSON file."""
    filepath = os.path.join(SEEDS_DIR, filename)
    with open(filepath, 'r') as f:
        return json.load(f)


class TestSeedFilesExist:
    """Verify all required seed files exist."""

    @pytest.mark.parametrize('filename', REQUIRED_FILES.keys())
    def test_file_exists(self, filename: str) -> None:
        filepath = os.path.join(SEEDS_DIR, filename)
        assert os.path.isfile(filepath), f"Missing seed file: {filepath}"

    @pytest.mark.parametrize('filename', REQUIRED_FILES.keys())
    def test_valid_json(self, filename: str) -> None:
        data = load_seed(filename)
        assert isinstance(data, dict)


class TestSeedStructure:
    """Verify the structure of each seed file matches expected schema."""

    @pytest.mark.parametrize('filename,spec', REQUIRED_FILES.items())
    def test_concept_slug(self, filename: str, spec: dict) -> None:
        data = load_seed(filename)
        assert data['concept_slug'] == spec['concept_slug']

    @pytest.mark.parametrize('filename,spec', REQUIRED_FILES.items())
    def test_question_count(self, filename: str, spec: dict) -> None:
        data = load_seed(filename)
        assert len(data['questions']) == spec['expected_count'], (
            f"{filename}: expected {spec['expected_count']} questions, "
            f"got {len(data['questions'])}"
        )

    @pytest.mark.parametrize('filename,spec', REQUIRED_FILES.items())
    def test_display_orders_sequential(self, filename: str, spec: dict) -> None:
        data = load_seed(filename)
        orders = [q['display_order'] for q in data['questions']]
        assert orders == list(range(1, len(orders) + 1)), (
            f"{filename}: display_order should be sequential starting from 1"
        )


class TestQuestionFields:
    """Verify each question has all required fields."""

    @pytest.mark.parametrize('filename,spec', REQUIRED_FILES.items())
    def test_question_required_fields(self, filename: str, spec: dict) -> None:
        data = load_seed(filename)
        for i, q in enumerate(data['questions']):
            assert 'title' in q, f"Q{i+1} missing title"
            assert isinstance(q['title'], str) and len(q['title']) > 10
            assert 'display_order' in q
            assert 'difficulty' in q
            assert q['difficulty'] == spec['difficulty']
            assert 'tags' in q
            assert isinstance(q['tags'], list) and len(q['tags']) >= 1
            assert 'answers' in q

    @pytest.mark.parametrize('filename,spec', REQUIRED_FILES.items())
    def test_titles_unique(self, filename: str, spec: dict) -> None:
        data = load_seed(filename)
        titles = [q['title'] for q in data['questions']]
        assert len(titles) == len(set(titles)), (
            f"{filename}: duplicate question titles found"
        )


class TestAnswerFields:
    """Verify each answer has all required fields and dual-mode coverage."""

    @pytest.mark.parametrize('filename', REQUIRED_FILES.keys())
    def test_dual_mode_answers(self, filename: str) -> None:
        """Every question must have both detailed and quick mode answers."""
        data = load_seed(filename)
        for i, q in enumerate(data['questions']):
            modes = {a['mode'] for a in q['answers']}
            assert modes == {'detailed', 'quick'}, (
                f"{filename} Q{i+1} '{q['title']}': "
                f"must have both detailed and quick modes, got {modes}"
            )

    @pytest.mark.parametrize('filename', REQUIRED_FILES.keys())
    def test_answer_required_keys(self, filename: str) -> None:
        data = load_seed(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                missing = ANSWER_REQUIRED_KEYS - set(a.keys())
                assert not missing, (
                    f"{filename} Q{i+1} {a['mode']}: missing keys {missing}"
                )

    @pytest.mark.parametrize('filename', REQUIRED_FILES.keys())
    def test_code_language_is_c(self, filename: str) -> None:
        data = load_seed(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                assert a['code_language'] == 'c', (
                    f"{filename} Q{i+1} {a['mode']}: "
                    f"code_language must be 'c', got '{a['code_language']}'"
                )

    @pytest.mark.parametrize('filename', REQUIRED_FILES.keys())
    def test_gotchas_not_empty(self, filename: str) -> None:
        data = load_seed(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                assert len(a['gotchas']) >= 1, (
                    f"{filename} Q{i+1} {a['mode']}: must have at least 1 gotcha"
                )

    @pytest.mark.parametrize('filename', REQUIRED_FILES.keys())
    def test_key_points_not_empty(self, filename: str) -> None:
        data = load_seed(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                assert len(a['key_points']) >= 1, (
                    f"{filename} Q{i+1} {a['mode']}: "
                    f"must have at least 1 key point"
                )

    @pytest.mark.parametrize('filename', REQUIRED_FILES.keys())
    def test_detailed_has_pseudo_code(self, filename: str) -> None:
        """Detailed answers should have pseudo_code field."""
        data = load_seed(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                if a['mode'] == 'detailed':
                    assert 'pseudo_code' in a, (
                        f"{filename} Q{i+1}: detailed answer missing pseudo_code"
                    )

    @pytest.mark.parametrize('filename', REQUIRED_FILES.keys())
    def test_actual_code_not_empty(self, filename: str) -> None:
        data = load_seed(filename)
        for i, q in enumerate(data['questions']):
            for a in q['answers']:
                assert len(a['actual_code'].strip()) > 0, (
                    f"{filename} Q{i+1} {a['mode']}: actual_code is empty"
                )


class TestMetaConceptAlignment:
    """Verify seed slugs match _meta.json concepts."""

    def test_slugs_in_meta(self) -> None:
        meta_path = os.path.join(SEEDS_DIR, '_meta.json')
        with open(meta_path) as f:
            meta = json.load(f)
        meta_slugs = {c['slug'] for c in meta['concepts']}

        for filename, spec in REQUIRED_FILES.items():
            assert spec['concept_slug'] in meta_slugs, (
                f"{filename}: slug '{spec['concept_slug']}' not found in _meta.json"
            )
