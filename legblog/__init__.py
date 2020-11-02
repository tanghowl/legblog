import click
import os
from flask import Flask, render_template
from flask_login import current_user
from legblog.settings import config
from legblog.blueprints.blog import blog_bp
from legblog.blueprints.admin import admin_bp
from legblog.blueprints.auth import auth_bp
from legblog.extensions import bootstrap, db, moment, ckeditor, mail, login_manager, csrf
from legblog.models import Admin, Post, Category, Comment, Link
from legblog.fakes import fake_admin, fake_categories, fake_posts, fake_comments
from flask_wtf.csrf import CSRFError


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('legblog')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_template_context(app)
    return app


def register_logging(app):
    login_manager.init_app(app)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin,
                    categories=categories,
                    unread_comments=unread_comments,
                    links=links)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continues?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Initialized database.')


    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
                  help='The password used to login.')
    def init(username, password):
        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                blog_title='LegBlog',
                blog_sub_title="No, I'm the real thing.",
                name='Admin',
                about='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--category', default=2, help='Quantity of categories, default is 10.')
    @click.option('--post', default=5, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=10, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""
        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo(f'Generating {category} categories...')
        fake_categories(category)

        click.echo(f'Generating {post} posts...')
        fake_posts(post)

        click.echo(f'Generating {comment} comment...')
        fake_comments(comment)

        click.echo('Done.')