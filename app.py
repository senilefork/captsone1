from flask import Flask, redirect, render_template, redirect, flash, session, jsonify, request, g, url_for, send_from_directory, abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Management, Apartment, User, UserApartment,UserApartmentPhoto
from forms import AddAddressForm, FilterApartmentsForm, RegisterForm, LoginForm, AddApartmentForm
import requests, json, pdb, os
from werkzeug.utils import secure_filename

CURRENT_USER = "current_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///real-estate-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

connect_db(app)
#db.create_all()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bArt_mAnn-1999')

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

###########################################################################
# register/sign-in functions

@app.before_request
def add_user_to_g():
    """If we login successfully, add user to global g object"""

    if CURRENT_USER in session:
        g.user = User.query.get(session[CURRENT_USER])
    else:
        g.user = None

def login(user):
    """Log user in by setting their id to flask session"""

    session[CURRENT_USER] = user.id

def logout():
    """Log user out by removing them from session"""

    if CURRENT_USER in session:
        del session[CURRENT_USER]


####################################################
# apartment coords and json related functions

#get_coords is used in the /new_apartment route to take the input address and get coordiantes from the mapquest api
def get_coords(address):
    res = requests.get("http://www.mapquestapi.com/geocoding/v1/address", params={'key': API_KEY, 'location': address})

    data = res.json()
    lat = data["results"][0]["locations"][0]['latLng']['lat']
    lng = data["results"][0]["locations"][0]['latLng']['lng']
    coords = {'lat' : lat, 'lng': lng}
    return coords

#serialize apartment info to prepare for json
def serialize_apartments(apartment, name):

    serialized = {
            'id' : apartment.id,
            'management_id' : apartment.management,
            'management_name' : name,
            'street' : apartment.street,
            'city' : apartment.city,
            'state' : apartment.state,
            'apartment_number' : apartment.apartment_number,
            'beds' : apartment.beds,
            'baths' : apartment.baths,
            'price' : apartment.price,
            'laundry' : apartment.laundry,
            'backyard' : apartment.backyard,
            'balcony' : apartment.balcony,
            'rooftop_access' : apartment.rooftop_access,
            'access' : apartment.access,
            'neighborhood' : apartment.neighborhood,
            'availability' : apartment.availability,
            'notes' : apartment.notes,
            'coordinates' : apartment.coordinates
    }
    return serialized
######################################
# register and login routes

@app.route('/register', methods=["GET", "POST"])
def register():

    form = RegisterForm()
    
    if form.validate_on_submit():
        try:
            user = User.register(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
                user_type=form.user_type.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("user name taken")
            return render_template('register.html', form=form)
        
        login(user)

        return redirect('/')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login_form():

    form= LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            login(user)
            flash(f'Hello {user.first_name}!')
            return redirect('/')

        flash('invalid login credentials')

    else:
        return render_template('login.html', form=form)   

@app.route('/sign_out')
def sign_out():
    """Remove user from g"""
    logout()

    return redirect('/login')


####################################################################
# routes for logged in user
 
@app.route('/')
def home():

    if not g.user:
        flash("Unauthorized access, please login or register")
        return redirect('/register')

    form = FilterApartmentsForm()
    blank_choice = [(0, "")]
    choices = [choice for choice in db.session.query(Management.id, Management.company_name)]
    choices.insert(0, blank_choice[0])
    form.management.choices =choices
    
    return render_template('home_page.html', form=form)

@app.route('/new_apartment', methods=["GET","POST"])
def new_apartment():
    """Submit new apartment to real-estate-db"""

    if not g.user:
        flash("Unauthorized access, please login or register")
        return redirect('/register')

    form = AddAddressForm()
    form.management.choices = (db.session.query(Management.id, Management.company_name))
    

    if form.validate_on_submit():
        management = form.management.data
        street = form.street.data
        city = form.city.data
        apartment_number = form.apartment_number.data
        beds = form.beds.data
        baths = form.baths.data
        price = form.price.data
        laundry = form.laundry.data
        backyard = form.backyard.data
        balcony = form.balcony.data
        rooftop_access = form.rooftop_access.data
        access = form.access.data
        neighborhood = form.neighborhood.data
        notes = form.notes.data
        address = f'{street} {city},NY'
        coordinates = get_coords(address)
        availability = form.availability.data

        new_apartment = Apartment(
            management = management,
            street = street,
            city = city,
            apartment_number = apartment_number,
            beds = beds,
            baths = baths,
            price = price,
            laundry = laundry,
            backyard = backyard,
            balcony = balcony,
            rooftop_access = rooftop_access,
            access = access,
            neighborhood = neighborhood,
            notes = notes,
            coordinates = coordinates,
            availability = availability
        )
        db.session.add(new_apartment)
        db.session.commit()
        return redirect('/map')
    else:
        return render_template('apartment_form.html', form=form)

@app.route('/get_apartments_json')
def get_apartments():

    if not g.user:
        flash("Unauthorized access, please login or register")
        return redirect('/register')

    all_apartments = [serialize_apartments(apartment, apartment.management_company.company_name ) for apartment in Apartment.query.all()]
    return jsonify(apartments=all_apartments)

@app.route('/filter_apartments')
def filter_apartments():

    if not g.user:
        flash("Unauthorized access, please login or register")
        return redirect('/register')

    if request.args:
        apartments = Apartment.query
        if request.args.get("price"):
            price = request.args["price"]
            apartments = apartments.filter((Apartment.price<price)|(Apartment.price==price))
        else:
            apartments = Apartment.query.filter()
        if request.args.get("management_id"):
            management = request.args["management_id"]        
            apartments = apartments.filter_by(management=management)
        if request.args.get("street"):
            street = request.args["street"]
            apartments = apartments.filter_by(street=street)
        if request.args.get("city"):
            city = request.args["city"]
            apartments = apartments.filter_by(city=city)
        if request.args.get("beds"):
            beds = request.args["beds"]
            apartments = apartments.filter_by(beds=beds)
        if request.args.get("baths"):
            baths = request.args["baths"]
            apartments = apartments.filter_by(baths=baths)
        if request.args.get("laundry"):
            laundry = request.args["laundry"]
            apartments = apartments.filter_by(laundry=laundry)
        if request.args.get("backyard"):
            backyard = request.args["backyard"]
            apartments = apartments.filter_by(backyard=backyard)
        if request.args.get("balcony"):
            balcony = request.args["balcony"]
            apartments = apartments.filter_by(balcony=balcony)
        if request.args.get("rooftop_access"):
            rooftop_access = request.args["rooftop_access"]
            apartments = apartments.filter_by(rooftop_access=rooftop_access)
        if request.args.get("neighborhood"):
            neighborhood = request.args["neighborhood"]
            apartments = apartments.filter_by(neighborhood=neighborhood)
        if request.args.get("availability"):
            availability = request.args["availability"]
            apartments = apartments.filter_by(availability=availability)
        apartments =  [serialize_apartments(apartment, apartment.management_company.company_name ) for apartment in apartments]
        return jsonify(apartments=apartments)
    
@app.route('/edit_apartment/<int:id>', methods=["GET", "POST"])
def edit_apartments(id):

    if not g.user:
        flash("Unauthorized access, please login or register")
        return redirect('/register')

    apartment = Apartment.query.get_or_404(id)
    form = AddAddressForm(obj=apartment)
    form.management.choices = (db.session.query(Management.id, Management.company_name))

    if form.validate_on_submit():
        apartment.management = form.management.data
        apartment.street = form.street.data
        apartment.city = form.city.data
        apartment.beds = form.beds.data
        apartment.baths = form.baths.data
        apartment.price = form.price.data
        apartment.laundry = form.laundry.data
        apartment.backyard = form.backyard.data
        apartment.balcony = form.balcony.data
        apartment.rooftop_access = form.rooftop_access.data
        apartment.access = form.access.data
        apartment.neighborhood = form.neighborhood.data
        apartment.notes = form.notes.data
        address = f'{apartment.street} {apartment.city},NY'
        apartment.coordinates = get_coords(address)

        db.session.commit()
        return redirect('/')

    else:
        return render_template('edit_apartment.html', form=form)   

@app.route('/delete/<int:id>')
def delete(id):

    apartment = Apartment.query.get_or_404(id)
    db.session.delete(apartment)
    db.session.commit()
    return redirect('/')


@app.route('/detail/<int:id>', methods=["GET", "POST"])
def detail(id):
    """apartment detail"""

    if not g.user:
        flash("Unauthorized access, please login or register")
        return redirect('/register')


    apartment = Apartment.query.get_or_404(id)
    form = AddApartmentForm()
    form.apartment.choices = [(apartment.id, apartment.street)]
    user = g.user.id

    if form.validate_on_submit():
        apartment = form.apartment.data
        new_user_apartment = UserApartment(user_id=user, apartment_id=apartment)
        db.session.add(new_user_apartment)
        db.session.commit()
        return redirect('/my_apartments')

    return render_template('detail.html', apartment=apartment, form=form)

@app.route('/my_apartments')
def my_apartments():
    if not g.user:
        flash("Unauthorized access, please login or register")
        return redirect('/register')

    return render_template('my_apartments.html')

@app.route('/user_apartment/<int:id>')
def user_apartment(id):
    """Get details of an apartment listed by a user"""
    if not g.user:
        flash("Unauthorized access, please login or register")
        return redirect('/register')

    apartment = Apartment.query.get_or_404(id)
    user_apartment_id = UserApartment.query
    user_apartment_id = user_apartment_id.filter(UserApartment.user_id== g.user.id, UserApartment.apartment_id==id)

    apartment_photos = UserApartmentPhoto.query.filter_by(user_apartment_id=id)
    files = [photo.name for photo in apartment_photos]

    return render_template('user_apartment_detail.html', apartment=apartment, user_apartment_id=user_apartment_id[0], files=files)



@app.route('/upload_photo/<int:id>', methods=["GET","POST"])
def upload(id):
    if not g.user:
        flash("Unauthorized access, please login or register")
        return redirect('/register')

    user_apartment_id = id 
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            #########add to db here
            new_photo = UserApartmentPhoto(user_apartment_id=user_apartment_id, name=filename)
            db.session.add(new_photo)
            db.session.commit()
        return redirect(url_for('upload', id=user_apartment_id))
    return render_template('add_photo.html')

@app.route('/get_uploads/<filename>')
def get_upload(filename):
    if not g.user:
        flash("Unauthorized access, please login or register")
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

#########################################################
# map route
@app.route('/map')
def map():
    """Map route"""

    if not g.user:
        flash("Unauthorized access, please login or register")
        return redirect('/register')

    form = FilterApartmentsForm()
    blank_choice = [(0, "")]
    choices = [choice for choice in db.session.query(Management.id, Management.company_name)]
    choices.insert(0, blank_choice[0])
    form.management.choices =choices
    
    return render_template('map.html', form=form)


    
