import json
import os
import tempfile
import pytest
from app.models import Language, Concept, Question, Answer, ConceptRelationship
from seeds.seed_runner import run_seed


@pytest.fixture
def seed_dir(tmp_path, monkeypatch):
    """Create a temporary seed directory with test data."""
    lang_dir = tmp_path / 'testlang'
    lang_dir.mkdir()

    meta = {
        'name': 'TestLang',
        'icon': 'test',
        'is_active': True,
        'display_order': 1,
        'concepts': [
            {
                'title': 'Basics',
                'slug': 'basics',
                'description': 'Basic concepts',
                'display_order': 1,
                'estimated_minutes': 20,
                'difficulty': 'beginner',
            },
            {
                'title': 'Advanced',
                'slug': 'advanced',
                'description': 'Advanced concepts',
                'display_order': 2,
                'estimated_minutes': 40,
                'difficulty': 'advanced',
            },
        ],
        'relationships': [
            {'from': 'basics', 'to': 'advanced', 'type': 'prerequisite'},
        ],
    }
    (lang_dir / '_meta.json').write_text(json.dumps(meta))

    questions_file = {
        'concept_slug': 'basics',
        'questions': [
            {
                'title': 'What is a variable?',
                'display_order': 1,
                'difficulty': 'beginner',
                'tags': ['fundamentals'],
                'answers': [
                    {
                        'mode': 'detailed',
                        'explanation': 'A variable stores data.',
                        'pseudo_code': 'x = value',
                        'actual_code': 'x = 42',
                        'code_language': 'python',
                        'key_points': ['Variables store references'],
                        'gotchas': ['Mutable default arguments'],
                    },
                    {
                        'mode': 'quick',
                        'explanation': 'Named reference to data.',
                        'key_points': ['Reference to object'],
                        'gotchas': ['Mutable defaults'],
                    },
                ],
            },
        ],
    }
    (lang_dir / '01_basics.json').write_text(json.dumps(questions_file))

    # Monkeypatch seed_runner to use tmp_path
    import seeds.seed_runner as sr
    original_dir = os.path.dirname(sr.__file__)
    monkeypatch.setattr(os.path, 'join',
                        lambda *args: str(lang_dir / args[-1]) if len(args) == 2 and args[0] == original_dir and args[1] == 'testlang'
                        else os.sep.join(args) if not callable(getattr(os.path, '_original_join', None))
                        else os.path._original_join(*args))

    # Simpler approach: just create files in the actual seeds directory
    monkeypatch.undo()

    actual_seed_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'seeds', 'testlang')
    os.makedirs(actual_seed_dir, exist_ok=True)

    with open(os.path.join(actual_seed_dir, '_meta.json'), 'w') as f:
        json.dump(meta, f)
    with open(os.path.join(actual_seed_dir, '01_basics.json'), 'w') as f:
        json.dump(questions_file, f)

    yield actual_seed_dir

    # Cleanup
    import shutil
    shutil.rmtree(actual_seed_dir, ignore_errors=True)


class TestSeedRunner:
    def test_creates_language(self, app, db, seed_dir):
        run_seed('testlang')
        lang = db.session.query(Language).filter_by(slug='testlang').first()
        assert lang is not None
        assert lang.name == 'TestLang'

    def test_creates_concepts(self, app, db, seed_dir):
        run_seed('testlang')
        lang = db.session.query(Language).filter_by(slug='testlang').first()
        concepts = db.session.query(Concept).filter_by(language_id=lang.id).order_by(Concept.display_order).all()
        assert len(concepts) == 2
        assert concepts[0].display_order < concepts[1].display_order

    def test_creates_questions_with_answers(self, app, db, seed_dir):
        run_seed('testlang')
        questions = db.session.query(Question).all()
        assert len(questions) == 1
        q = questions[0]
        assert len(q.answers) == 2
        modes = {a.mode for a in q.answers}
        assert modes == {'detailed', 'quick'}

    def test_creates_relationships(self, app, db, seed_dir):
        run_seed('testlang')
        rels = db.session.query(ConceptRelationship).all()
        assert len(rels) == 1
        assert rels[0].relationship_type == 'prerequisite'

    def test_idempotency(self, app, db, seed_dir):
        run_seed('testlang')
        run_seed('testlang')
        langs = db.session.query(Language).filter_by(slug='testlang').all()
        assert len(langs) == 1
        questions = db.session.query(Question).all()
        assert len(questions) == 1

    def test_missing_meta_raises(self, app, db):
        with pytest.raises(FileNotFoundError):
            run_seed('nonexistent_language')
