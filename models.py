from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#import json

db = SQLAlchemy()


bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Management(db.Model):
    """Management Companies"""

    __tablename__ = "management_companies"

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    company_name = db.Column(db.String, unique=True, nullable=False)
    contact = db.Column(db.Text)


class Apartment(db.Model):
    """Apartments"""

    __tablename__ = "apartments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    management = db.Column(db.Integer, db.ForeignKey("management_companies.id"))
    street = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String, default="NY")
    apartment_number = db.Column(db.String)
    beds = db.Column(db.Float)
    baths = db.Column(db.Float)
    price = db.Column(db.Float)
    laundry = db.Column(db.String)
    backyard = db.Column(db.String)
    balcony = db.Column(db.Boolean)
    rooftop_access = db.Column(db.Boolean)
    access = db.Column(db.String)
    neighborhood = db.Column(db.String)
    notes = db.Column(db.Text)
    coordinates = db.Column(db.PickleType)
    availability = db.Column(db.Text)

    management_company = db.relationship('Management', backref="apartments")

class User(db.Model):
    """Users"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    user_type = db.Column(db.Text, nullable=False)

    apartments = db.relationship('Apartment', secondary='users_apartments', backref='user')

    @classmethod
    def register(cls, first_name, last_name, email, username, password, user_type):
        """Create new user and add to db"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed_pwd,
            user_type=user_type
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, pwd):

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False


class UserApartment(db.Model):
    """user's listed apartments"""

    __tablename__ = "users_apartments"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', primary_key=True))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'), primary_key=True)














