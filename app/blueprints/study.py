from flask import Blueprint, render_template, request, abort
from app.extensions import db
from app.models import Language, Concept, Question, Progress

bp = Blueprint('study', __name__, url_prefix='/study')


def get_concept_progress(concept):
    """Calculate progress percentage for a concept."""
    total = len(concept.questions)
    if total == 0:
        return 0
    completed = sum(
        1 for q in concept.questions
        if q.progress and q.progress.status == 'completed'
    )
    return round(completed / total * 100)


@bp.route('/languages')
def languages():
    langs = db.session.query(Language).order_by(Language.display_order).all()
    return render_template('study/languages.html', languages=langs)


@bp.route('/<lang_slug>')
def concepts(lang_slug):
    language = db.session.query(Language).filter_by(slug=lang_slug).first_or_404()
    concept_list = []
    for c in language.concepts:
        concept_list.append({
            'concept': c,
            'progress_pct': get_concept_progress(c),
        })
    return render_template('study/concepts.html', language=language, concept_list=concept_list)


@bp.route('/<lang_slug>/<concept_slug>')
def concept_detail(lang_slug, concept_slug):
    language = db.session.query(Language).filter_by(slug=lang_slug).first_or_404()
    concept = (
        db.session.query(Concept)
        .filter_by(language_id=language.id, slug=concept_slug)
        .first_or_404()
    )
    mode = request.args.get('mode', 'detailed')
    if mode not in ('detailed', 'quick'):
        mode = 'detailed'

    # Get related concepts
    related = [r.related_concept for r in concept.outgoing_relationships]

    return render_template(
        f'study/{mode}.html',
        language=language,
        concept=concept,
        mode=mode,
        related_concepts=related,
    )
