from foobar import views


def register_blueprints(app):
    app.register_blueprint(views.home.bp, url_prefix='/api')
    app.register_blueprint(views.user.bp, url_prefix='/api')
    app.register_blueprint(views.session.bp, url_prefix='/api')
