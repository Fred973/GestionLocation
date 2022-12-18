from soft import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Create Model
class Users(db.Model, UserMixin):
    """
    Users databases structure:
        - id
        - username
        - category (
                    0 = normal user
                    1 = admin
                    2 = gestion location
                    3 =
                    )
        - password_hash
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    category = db.Column(db.Integer, nullable=False)

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a String
    def __repr__(self):
        return '<Username %r>' % self.username
