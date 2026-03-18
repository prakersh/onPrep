from flask import Blueprint, render_template
from app.extensions import db
from app.models import Language

bp = Blueprint('planner', __name__, url_prefix='/planner')

COLOR_MAP = {
    'indigo': '#6366f1', 'emerald': '#10b981', 'rose': '#f43f5e',
    'amber': '#f59e0b', 'cyan': '#06b6d4', 'violet': '#8b5cf6',
    'orange': '#f97316', 'teal': '#14b8a6',
}
COLORS = list(COLOR_MAP.keys())


@bp.route('/setup', methods=['GET'])
def setup():
    """Render planner setup page. All deadline data is in localStorage."""
    languages = (
        db.session.query(Language)
        .filter_by(is_active=True)
        .order_by(Language.display_order)
        .all()
    )
    lang_data = [
        {'id': lang.id, 'name': lang.name, 'slug': lang.slug}
        for lang in languages
    ]
    return render_template(
        'planner/setup.html',
        languages=languages,
        lang_data=lang_data,
        colors=COLORS,
        color_map=COLOR_MAP,
    )


@bp.route('/schedule')
def schedule():
    """Render schedule list page. All data comes from localStorage via JS."""
    return render_template('planner/schedule.html')


@bp.route('/schedule/detail')
def schedule_detail():
    """Render schedule detail page. Deadline ID comes from query param, data from localStorage."""
    return render_template('planner/schedule_detail.html')
