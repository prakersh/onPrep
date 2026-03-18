from flask import Blueprint, jsonify
from app.extensions import db
from app.models import Language, Concept

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/concepts/<lang_slug>')
def concepts(lang_slug: str):
    """Return concepts for a language as JSON (used by client-side scheduler)."""
    language = db.session.query(Language).filter_by(slug=lang_slug, is_active=True).first()
    if not language:
        return jsonify({'error': 'Language not found'}), 404

    concepts_list = (
        db.session.query(Concept)
        .filter_by(language_id=language.id)
        .order_by(Concept.display_order)
        .all()
    )
    return jsonify([
        {
            'slug': c.slug,
            'title': c.title,
            'estimated_minutes': c.estimated_minutes,
            'display_order': c.display_order,
        }
        for c in concepts_list
    ])
