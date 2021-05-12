from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, RadioField, SelectField, TextAreaField, PasswordField, SubmitField
from wtforms.fields.simple import SubmitField
from wtforms.validators import InputRequired, Email, Length


cities = ['Brooklyn', 'New York', 'Queens', 'Bronx', 'Staten Island']


class AddAddressForm(FlaskForm):
    """Form for adding new address"""

    management = SelectField("Management Company", coerce=int)
    street = StringField("Street",[InputRequired()])
    city = SelectField("City", [InputRequired()], choices=[(city, city) for city in cities])
    apartment_number = StringField("apartment", [InputRequired()])
    beds = FloatField("Number of bedrooms", [InputRequired()])
    baths = FloatField("Number of bathrooms", [InputRequired()])
    price = FloatField("Price")
    laundry = RadioField("Laundry", choices=[('bld', 'laundry in bulding'),('unit','laundry in unit'),('none', 'none')])
    backyard = RadioField("Backyard", choices=[('private', 'private backyard'),('shared', 'shared backyard'), ('none', 'none')])
    balcony = BooleanField("Balcony")
    rooftop_access = BooleanField("Rooftop access")
    access = StringField("Access info")
    neighborhood = StringField("Neighborhood")
    notes = TextAreaField("Notes")
    availability = SelectField("Availability", choices=[('occupied','occupied'),('vacant','vacant'), ('deposit', 'deposit')])

class FilterApartmentsForm(FlaskForm):
    """Form for filtering apartments"""

    management = SelectField("Management Company", coerce=int)
    street = StringField("Street")
    city = SelectField("City", choices=[(city, city) for city in cities])
    beds = FloatField("Number of bedrooms")
    baths = FloatField("Number of bathrooms")
    price = FloatField("Price")
    laundry = RadioField("Laundry", choices=[('bld', 'laundry in bulding'),('unit','laundry in unit')])
    backyard = RadioField("Backyard", choices=[('private', 'private backyard'),('shared', 'shared backyard')])
    balcony = RadioField(choices=[('True', 'balcony')])
    rooftop_access = RadioField(choices=[('True', 'Rooftop access')])
    neighborhood = StringField("Neighborhood")
    availability = SelectField("Availability", choices=[('occupied','occupied'),('vacant','vacant'), ('deposit', 'deposit')])


    
class RegisterForm(FlaskForm):
    """Register form"""

    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired(), Email()])
    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=10, max=20)])
    user_type = RadioField("user type", choices=[('admin', 'admin'), ('agent', 'agent')])

class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired(), Length(min=10, max=20)])

class AddApartmentForm(FlaskForm):
    """Add apartment to user list"""

    apartment = SelectField("Add apartment", coerce=int)



