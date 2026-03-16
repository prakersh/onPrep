import pytest
from sqlalchemy.exc import IntegrityError
from app.models import Language, Concept, Question, Answer, ConceptRelationship


class TestLanguage:
    def test_create_language(self, db, sample_language):
        assert sample_language.id is not None
        assert sample_language.name == 'Python'
        assert sample_language.slug == 'python'

    def test_slug_uniqueness(self, db, sample_language):
        dup = Language(name='Python2', slug='python')
        db.session.add(dup)
        with pytest.raises(IntegrityError):
            db.session.commit()

    def test_language_repr(self, sample_language):
        assert 'Python' in repr(sample_language)


class TestConcept:
    def test_create_concept(self, db, sample_concept):
        assert sample_concept.id is not None
        assert sample_concept.title == 'Data Types & Variables'

    def test_concept_belongs_to_language(self, sample_concept, sample_language):
        assert sample_concept.language_id == sample_language.id
        assert sample_concept.language == sample_language

    def test_concepts_ordered_by_display_order(self, db, sample_language):
        c1 = Concept(language_id=sample_language.id, title='First', slug='first', display_order=2)
        c2 = Concept(language_id=sample_language.id, title='Second', slug='second', display_order=1)
        db.session.add_all([c1, c2])
        db.session.commit()
        concepts = sample_language.concepts
        orders = [c.display_order for c in concepts]
        assert orders == sorted(orders)

    def test_unique_slug_per_language(self, db, sample_concept, sample_language):
        dup = Concept(language_id=sample_language.id, title='Dup', slug='data-types-variables')
        db.session.add(dup)
        with pytest.raises(IntegrityError):
            db.session.commit()


class TestQuestion:
    def test_create_question(self, db, sample_question):
        assert sample_question.id is not None
        assert sample_question.concept_id is not None

    def test_question_belongs_to_concept(self, sample_question, sample_concept):
        assert sample_question.concept == sample_concept

    def test_question_tags_json(self, sample_question):
        assert 'fundamentals' in sample_question.tags


class TestAnswer:
    def test_create_detailed_answer(self, db, sample_answers):
        detailed, _ = sample_answers
        assert detailed.mode == 'detailed'
        assert detailed.explanation != ''
        assert detailed.actual_code != ''

    def test_create_quick_answer(self, db, sample_answers):
        _, quick = sample_answers
        assert quick.mode == 'quick'
        assert len(quick.key_points) > 0

    def test_answer_gotchas(self, db, sample_answers):
        detailed, quick = sample_answers
        assert len(detailed.gotchas) > 0
        assert len(quick.gotchas) > 0

    def test_answer_belongs_to_question(self, db, sample_answers, sample_question):
        detailed, _ = sample_answers
        assert detailed.question == sample_question


class TestConceptRelationship:
    def test_create_relationship(self, db, sample_concept, sample_concept_b):
        rel = ConceptRelationship(
            concept_id=sample_concept.id,
            related_concept_id=sample_concept_b.id,
            relationship_type='prerequisite',
        )
        db.session.add(rel)
        db.session.commit()
        assert rel.id is not None
        assert rel.concept == sample_concept
        assert rel.related_concept == sample_concept_b

    def test_outgoing_relationships(self, db, sample_concept, sample_concept_b):
        rel = ConceptRelationship(
            concept_id=sample_concept.id,
            related_concept_id=sample_concept_b.id,
            relationship_type='related',
        )
        db.session.add(rel)
        db.session.commit()
        assert len(sample_concept.outgoing_relationships) == 1
        assert sample_concept.outgoing_relationships[0].related_concept == sample_concept_b


class TestCascadeDeletes:
    def test_delete_language_cascades(self, db, sample_language, sample_concept, sample_question, sample_answers):
        lang_id = sample_language.id
        db.session.delete(sample_language)
        db.session.commit()
        assert db.session.query(Concept).filter_by(language_id=lang_id).count() == 0
        assert db.session.query(Question).count() == 0
        assert db.session.query(Answer).count() == 0

    def test_delete_concept_cascades(self, db, sample_concept, sample_question, sample_answers):
        concept_id = sample_concept.id
        db.session.delete(sample_concept)
        db.session.commit()
        assert db.session.query(Question).filter_by(concept_id=concept_id).count() == 0
        assert db.session.query(Answer).count() == 0
