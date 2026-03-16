import pytest
from app import create_app
from app.extensions import db as _db
from app.models import Language, Concept, Question, Answer, ConceptRelationship


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_language(db):
    lang = Language(name='Python', slug='python', icon='python', is_active=True, display_order=1)
    db.session.add(lang)
    db.session.commit()
    return lang


@pytest.fixture
def sample_concept(db, sample_language):
    concept = Concept(
        language_id=sample_language.id,
        title='Data Types & Variables',
        slug='data-types-variables',
        description='Learn about Python data types',
        display_order=1,
        estimated_minutes=30,
        difficulty='beginner',
    )
    db.session.add(concept)
    db.session.commit()
    return concept


@pytest.fixture
def sample_question(db, sample_concept):
    question = Question(
        concept_id=sample_concept.id,
        title='What are the basic data types in Python?',
        display_order=1,
        difficulty='beginner',
        tags=['fundamentals'],
    )
    db.session.add(question)
    db.session.commit()
    return question


@pytest.fixture
def sample_answers(db, sample_question):
    detailed = Answer(
        question_id=sample_question.id,
        mode='detailed',
        explanation='Python has several built-in data types...',
        pseudo_code='# Check type\ntype(variable)',
        actual_code='x = 42\nprint(type(x))  # <class \'int\'>',
        code_language='python',
        key_points=['int, float, str, bool, None are basic types'],
        gotchas=['Python 3 has no long type — int handles arbitrary precision'],
    )
    quick = Answer(
        question_id=sample_question.id,
        mode='quick',
        explanation='Basic types: int, float, str, bool, None, list, tuple, dict, set',
        key_points=['int, float, str, bool, None', 'list, tuple, dict, set'],
        gotchas=['Python 3 has no long type'],
    )
    db.session.add_all([detailed, quick])
    db.session.commit()
    return detailed, quick


@pytest.fixture
def sample_concept_b(db, sample_language):
    concept = Concept(
        language_id=sample_language.id,
        title='Operators & Expressions',
        slug='operators-expressions',
        description='Python operators',
        display_order=2,
        estimated_minutes=25,
        difficulty='beginner',
    )
    db.session.add(concept)
    db.session.commit()
    return concept
