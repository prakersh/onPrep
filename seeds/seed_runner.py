import json
import os
from app.extensions import db
from app.models import Language, Concept, Question, Answer, ConceptRelationship


def run_seed(language_slug):
    """Seed content for a given language from JSON files."""
    seed_dir = os.path.join(os.path.dirname(__file__), language_slug)
    meta_path = os.path.join(seed_dir, '_meta.json')

    if not os.path.exists(meta_path):
        raise FileNotFoundError(f'No _meta.json found for {language_slug} at {meta_path}')

    with open(meta_path, 'r') as f:
        meta = json.load(f)

    # Upsert language
    language = db.session.query(Language).filter_by(slug=language_slug).first()
    if not language:
        language = Language(
            name=meta['name'],
            slug=language_slug,
            icon=meta.get('icon', ''),
            is_active=meta.get('is_active', True),
            display_order=meta.get('display_order', 0),
        )
        db.session.add(language)
        db.session.flush()
    else:
        language.name = meta['name']
        language.icon = meta.get('icon', '')
        language.is_active = meta.get('is_active', True)
        language.display_order = meta.get('display_order', 0)

    # Upsert concepts
    concept_map = {}
    for concept_def in meta.get('concepts', []):
        concept = (
            db.session.query(Concept)
            .filter_by(language_id=language.id, slug=concept_def['slug'])
            .first()
        )
        if not concept:
            concept = Concept(
                language_id=language.id,
                title=concept_def['title'],
                slug=concept_def['slug'],
                description=concept_def.get('description', ''),
                display_order=concept_def.get('display_order', 0),
                estimated_minutes=concept_def.get('estimated_minutes', 30),
                difficulty=concept_def.get('difficulty', 'beginner'),
            )
            db.session.add(concept)
            db.session.flush()
        else:
            concept.title = concept_def['title']
            concept.description = concept_def.get('description', '')
            concept.display_order = concept_def.get('display_order', 0)
            concept.estimated_minutes = concept_def.get('estimated_minutes', 30)
            concept.difficulty = concept_def.get('difficulty', 'beginner')

        concept_map[concept_def['slug']] = concept

    # Seed questions from numbered JSON files
    for filename in sorted(os.listdir(seed_dir)):
        if filename.startswith('_') or not filename.endswith('.json'):
            continue

        filepath = os.path.join(seed_dir, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)

        concept_slug = data['concept_slug']
        concept = concept_map.get(concept_slug)
        if not concept:
            raise ValueError(f'Concept {concept_slug} not found in _meta.json')

        for q_data in data.get('questions', []):
            # Check if question already exists (by title + concept)
            existing = (
                db.session.query(Question)
                .filter_by(concept_id=concept.id, title=q_data['title'])
                .first()
            )
            if existing:
                question = existing
                question.display_order = q_data.get('display_order', 0)
                question.difficulty = q_data.get('difficulty', concept.difficulty)
                question.tags = q_data.get('tags', [])
            else:
                question = Question(
                    concept_id=concept.id,
                    title=q_data['title'],
                    display_order=q_data.get('display_order', 0),
                    difficulty=q_data.get('difficulty', concept.difficulty),
                    tags=q_data.get('tags', []),
                )
                db.session.add(question)
                db.session.flush()

            # Upsert answers
            for a_data in q_data.get('answers', []):
                mode = a_data['mode']
                existing_answer = (
                    db.session.query(Answer)
                    .filter_by(question_id=question.id, mode=mode)
                    .first()
                )
                if existing_answer:
                    existing_answer.explanation = a_data.get('explanation', '')
                    existing_answer.pseudo_code = a_data.get('pseudo_code', '')
                    existing_answer.actual_code = a_data.get('actual_code', '')
                    existing_answer.code_language = a_data.get('code_language', 'python')
                    existing_answer.key_points = a_data.get('key_points', [])
                    existing_answer.gotchas = a_data.get('gotchas', [])
                else:
                    answer = Answer(
                        question_id=question.id,
                        mode=mode,
                        explanation=a_data.get('explanation', ''),
                        pseudo_code=a_data.get('pseudo_code', ''),
                        actual_code=a_data.get('actual_code', ''),
                        code_language=a_data.get('code_language', 'python'),
                        key_points=a_data.get('key_points', []),
                        gotchas=a_data.get('gotchas', []),
                    )
                    db.session.add(answer)

    # Seed relationships
    for rel_def in meta.get('relationships', []):
        from_concept = concept_map.get(rel_def['from'])
        to_concept = concept_map.get(rel_def['to'])
        if from_concept and to_concept:
            existing_rel = (
                db.session.query(ConceptRelationship)
                .filter_by(
                    concept_id=from_concept.id,
                    related_concept_id=to_concept.id,
                    relationship_type=rel_def.get('type', 'related'),
                )
                .first()
            )
            if not existing_rel:
                rel = ConceptRelationship(
                    concept_id=from_concept.id,
                    related_concept_id=to_concept.id,
                    relationship_type=rel_def.get('type', 'related'),
                )
                db.session.add(rel)

    db.session.commit()
