from foobar import __version__
from foobar.views import home


def register_apispec(app):
    from apispec import APISpec
    from apispec.ext.marshmallow import MarshmallowPlugin
    from flask_apispec.extension import FlaskApiSpec

    app.config.update({
        'APISPEC_SPEC':
        APISpec(
            title='TestFromLocal_Json_App_0',
            version=f'v{__version__}',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()]
        ),
        'APISPEC_SWAGGER_URL': '/spec-json',
        'APISPEC_SWAGGER_UI_URL': '/spec'
    })

    spec = FlaskApiSpec(app)

    spec.register(home.home, blueprint='home')
