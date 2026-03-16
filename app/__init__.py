from markupsafe import Markup
from flask import Flask
import mistune
from app.config import config
from app.extensions import db, migrate

_markdown = mistune.create_markdown(escape=False)


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import content, progress  # noqa: F401

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

    return app
