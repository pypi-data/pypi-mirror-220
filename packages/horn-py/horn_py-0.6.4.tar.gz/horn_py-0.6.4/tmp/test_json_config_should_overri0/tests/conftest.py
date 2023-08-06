import pytest

from foobar.run import create_app
from foobar.core.database import db as _db


@pytest.fixture(scope='session')
def app(request):
    _app = create_app('test')

    ctx = _app.test_request_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='session')
def db(request, app):
    _db.app = app
    with app.app_context():
        _db.create_all()

    def teardown():
        _db.session.close()
        _db.drop_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture()
def client(app):
    return app.test_client()
