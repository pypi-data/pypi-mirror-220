from foobar import views


def register_blueprints(app):
    app.register_blueprint(views.home.bp, url_prefix='/api')
