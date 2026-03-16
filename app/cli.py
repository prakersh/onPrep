import click
from flask import current_app
from flask.cli import with_appcontext


def register_cli(app):
    @app.cli.command('seed')
    @click.argument('language')
    @with_appcontext
    def seed_command(language):
        """Seed the database with content for a language."""
        from seeds.seed_runner import run_seed
        run_seed(language)
        click.echo(f'Seeded content for {language}.')
