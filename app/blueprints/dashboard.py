from flask import Blueprint, render_template, redirect, Response
from datetime import date
from app.extensions import db
from app.models import Language, Question, Deadline, ScheduleItem, Concept

bp = Blueprint('dashboard', __name__)


@bp.route('/robots.txt')
def robots():
    content = "User-agent: *\nAllow: /\nSitemap: https://awesomeprep.prakersh.in/sitemap.xml\n"
    return Response(content, mimetype='text/plain')


@bp.route('/sitemap.xml')
def sitemap():
    languages = db.session.query(Language).filter_by(is_active=True).all()
    urls = [
        'https://awesomeprep.prakersh.in/landing',
        'https://awesomeprep.prakersh.in/dashboard',
        'https://awesomeprep.prakersh.in/study/languages',
    ]
    for lang in languages:
        urls.append(f'https://awesomeprep.prakersh.in/study/{lang.slug}')
        for c in lang.concepts:
            urls.append(f'https://awesomeprep.prakersh.in/study/{lang.slug}/{c.slug}')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f'  <url><loc>{url}</loc></url>\n'
    xml += '</urlset>'
    return Response(xml, mimetype='application/xml')


@bp.route('/')
def home():
    """Serve a tiny page that checks localStorage and redirects."""
    return render_template('home_redirect.html')


@bp.route('/landing')
def landing():
    """Public landing page for first-time visitors."""
    total_questions = db.session.query(Question).count()
    languages = db.session.query(Language).filter_by(is_active=True).order_by(Language.display_order).all()
    lang_data = []
    for lang in languages:
        total_q = sum(len(c.questions) for c in lang.concepts)
        lang_data.append({
            'name': lang.name,
            'slug': lang.slug,
            'concept_count': len(lang.concepts),
            'question_count': total_q,
        })
    return render_template('landing.html', total_questions=total_questions, languages=lang_data)


@bp.route('/dashboard')
def index():
    total_questions = db.session.query(Question).count()

    # All active deadlines sorted by date
    deadlines = (
        db.session.query(Deadline)
        .filter_by(is_active=True)
        .order_by(Deadline.interview_date)
        .all()
    )

    deadline_data = []
    for d in deadlines:
        days_remaining = (d.interview_date - date.today()).days
        deadline_data.append({'deadline': d, 'days_remaining': days_remaining})

    # Languages with question IDs for client-side progress hydration
    languages = db.session.query(Language).filter_by(is_active=True).order_by(Language.display_order).all()

    language_stats = []
    for lang in languages:
        qids = []
        concepts_data = []
        for c in lang.concepts:
            c_qids = [q.id for q in c.questions]
            qids.extend(c_qids)
            concepts_data.append({
                'concept': c,
                'qids': c_qids,
                'total': len(c_qids),
            })
        language_stats.append({
            'language': lang,
            'total': len(qids),
            'qids': qids,
            'concept_count': len(lang.concepts),
            'concepts': concepts_data,
        })

    # Per-difficulty stats with question IDs
    difficulty_stats = []
    for diff in ['beginner', 'intermediate', 'advanced']:
        concepts = db.session.query(Concept).filter_by(difficulty=diff).all()
        qids = []
        for c in concepts:
            qids.extend(q.id for q in c.questions)
        difficulty_stats.append({
            'difficulty': diff,
            'total': len(qids),
            'qids': qids,
        })

    # Question metadata for recent-viewed hydration (JS needs title + URL info)
    all_questions = {}
    for ls in language_stats:
        for cd in ls['concepts']:
            for q in cd['concept'].questions:
                all_questions[q.id] = {
                    'title': q.title,
                    'url': f"/study/{ls['language'].slug}/{cd['concept'].slug}?q={q.id}",
                }

    return render_template(
        'dashboard/index.html',
        total_questions=total_questions,
        deadline_data=deadline_data,
        language_stats=language_stats,
        difficulty_stats=difficulty_stats,
        all_questions=all_questions,
    )
