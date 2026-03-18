from markupsafe import Markup
from flask import Flask
import mistune
from app.config import config
from app.extensions import db, migrate

_markdown = mistune.create_markdown(
    escape=False,
    plugins=['table', 'strikethrough', 'task_lists'],
)


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import content  # noqa: F401

    from app.blueprints.dashboard import bp as dashboard_bp
    from app.blueprints.study import bp as study_bp
    from app.blueprints.planner import bp as planner_bp
    from app.blueprints.api import bp as api_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(planner_bp)
    app.register_blueprint(api_bp)

    from app.cli import register_cli
    register_cli(app)

    @app.template_filter('markdown')
    def markdown_filter(text):
        if not text:
            return ''
        return Markup(_markdown(text))

    @app.template_filter('color_hex')
    def color_hex_filter(color_name):
        from app.blueprints.planner import COLOR_MAP
        return COLOR_MAP.get(color_name, '#6366f1')

    @app.template_filter('strip_expected_output')
    def strip_expected_output_filter(code):
        """Remove the Expected Output comment block from code."""
        if not code:
            return ''
        import re
        # C-style: /* Expected Output: ... */
        code = re.sub(r'\n*\s*/\*\s*Expected Output:.*?\*/', '', code, flags=re.DOTALL)
        # Python-style: # Expected Output:\n# line1\n# line2...
        code = re.sub(r'\n*# Expected Output:\n(?:#[^\n]*\n?)*', '', code)
        return code.rstrip()

    @app.template_filter('get_expected_output')
    def get_expected_output_filter(code):
        """Extract the Expected Output content from code."""
        if not code:
            return ''
        import re
        # C-style
        m = re.search(r'/\*\s*Expected Output:\s*\n(.*?)\*/', code, re.DOTALL)
        if m:
            return m.group(1).rstrip()
        # Python-style
        m = re.search(r'# Expected Output:\n((?:#[^\n]*\n?)*)', code)
        if m:
            return '\n'.join(line.lstrip('# ').rstrip() for line in m.group(1).strip().split('\n'))
        return ''

    return app
