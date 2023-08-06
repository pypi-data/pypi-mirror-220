from foobar import __version__
from foobar.views import home
from foobar.views import user, session


def register_apispec(app):
    from apispec import APISpec
    from apispec.ext.marshmallow import MarshmallowPlugin
    from flask_apispec.extension import FlaskApiSpec

    app.config.update({
        'APISPEC_SPEC':
        APISpec(
            title='TestNewWithOptionsApp_Ap0',
            version=f'v{__version__}',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()]
        ),
        'APISPEC_SWAGGER_URL': '/spec-json',
        'APISPEC_SWAGGER_UI_URL': '/spec'
    })

    spec = FlaskApiSpec(app)

    spec.register(home.home, blueprint='home')

    spec.register(user.index, blueprint='user')
    spec.register(user.create, blueprint='user')
    spec.register(user.show, blueprint='user')
    spec.register(user.update, blueprint='user')
    spec.register(user.delete, blueprint='user')

    spec.register(session.create, blueprint='session')
    spec.register(session.delete, blueprint='session')
