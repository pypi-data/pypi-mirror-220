from factory.alchemy import SQLAlchemyModelFactory

from foobar.core.database import db


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""
        abstract = True
        sqlalchemy_session = db.session
