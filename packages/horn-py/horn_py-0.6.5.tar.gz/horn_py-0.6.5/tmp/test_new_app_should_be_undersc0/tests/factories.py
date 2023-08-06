from factory.alchemy import SQLAlchemyModelFactory
from factory import PostGenerationMethodCall, Sequence

from foo_bar.core.database import db
from foo_bar.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""
        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    username = Sequence(lambda n: f'user{n}')
    email = Sequence(lambda n: f'user{n}@example.com')
    password = PostGenerationMethodCall('set_password', 'example')

    class Meta:
        model = User
