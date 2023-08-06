from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

from foo_bar.helpers import jwt_identity, identity_loader  # noqa

jwt = JWTManager()
jwt.user_loader_callback_loader(jwt_identity)
jwt.user_identity_loader(identity_loader)
