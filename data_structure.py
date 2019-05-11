from flask import Flask, render_template, redirect, url_for, request, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired
from geopy.geocoders import Nominatim
import requests, threading, time, folium
from linked_list import Set

# App Config ###########################################################################
app = Flask(__name__)


class Authentificator:
    DEBUG = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/cursova/untitled/data.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/cursova/untitled/data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SECRET_KEY'] = 'very_secret_key'
    WTF_CSRF_ENABLED = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'testovemylo805@gmail.com'
    app.config['MAIL_PASSWORD'] = 'january2019'


app.config.from_object(Authentificator)
db = SQLAlchemy(app)
mail = Mail(app)


# Models ###############################################################################
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, index=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(128))
    role = db.Column(db.String(5), default='user')
    is_logged_in = db.Column(db.Boolean, default=False)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, index=True)
    start_time = db.Column(db.DateTime)
    city_name = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    url = db.Column(db.Text)

    def __init__(self, title, start_time, city_name, latitude, longitude, url):
        self.title = title
        self.start_time = start_time
        self.city_name = city_name
        self.latitude = latitude
        self.longitude = longitude
        self.url = url


# db.drop_all()
db.create_all()


# Views ################################################################################
@app.route('/')
def index():
    def event_json():
        user_key = 'SSqPdQ5xLbF6dwN2'
        event_location = 'London'
        start_date = 20190509
        end_date = 20190509
        url = "http://api.eventful.com/json/events/search?"
        url += "&app_key={}".format(user_key)
        url += "&location={}".format(event_location)
        url += "&date={}00-{}00".format(start_date, end_date)
        url += '&page_size=10'
        url += '&page_number=1'
        response = requests.get(url)
        return response.json()['events']['event']

    events_list = Set()
    for i in event_json():
        event = Event(title=i['title'],
                      start_time=i['start_time'],
                      city_name=i['city_name'],
                      latitude=i['latitude'],
                      longitude=i['longitude'],
                      url=i['url'])
        events_list.add(event)
    return render_template('index.html', events_list=events_list)


@app.route('/map')
def map():
    user_key = 'SSqPdQ5xLbF6dwN2'
    event_location = request.args.get('city', '')
    date_start = request.args.get('date_start', '')  # 20190501
    date_end = request.args.get('date_end', '')  # 20190531
    print(date_start, date_end)
    url = "http://api.eventful.com/json/events/search?"
    url += "&app_key={}".format(user_key)
    url += "&location={}".format(event_location)
    url += "&date={}00-{}00".format(date_start, date_end)
    url += '&page_size=250'
    response = requests.get(url)

    if not event_location:
        m = folium.Map(location=(39.467697, 3.036337), zoom_start=3)
    else:
        geolocator = Nominatim()
        location = geolocator.geocode(event_location)
        try:
            m = folium.Map(location=(location.latitude, location.longitude), zoom_start=12)
        except:
            m = folium.Map(location=(39.467697, 3.036337), zoom_start=3)

    for i in response.json()['events']['event']:
        popup = folium.Popup('<a href="{}" target="_blank">{}</a>'.format(i['url'], i['title']))
        try:
            folium.Marker([float(i['latitude']), float(i['longitude'])], popup=popup).add_to(m)
        except:
            m = folium.Map(location=(39.467697, 3.036337), zoom_start=3)
    m.save('templates/map.html')
    return render_template('map.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    class RegistrationForm(FlaskForm):
        email = StringField('email', validators=[DataRequired(), Email()])
        name = StringField('name', validators=[DataRequired()])
        password1 = PasswordField('password', validators=[DataRequired()])
        password2 = PasswordField('confirm password',
                                  validators=[DataRequired(), EqualTo('password1', message='Passwords must match.')])

    form = RegistrationForm()
    if request.method == 'POST':
        email = form.email.data
        name = form.name.data
        password2 = form.password2.data
        if form.validate_on_submit():
            new_user = User(email=email, name=name, password=password2)
            db.session.add(new_user)
            try:
                db.session.commit()
            except:
                return redirect(url_for('email_already_exists'))
            msg = Message('confirm events registration', sender=('Events team', 'testovemylo805@gmail.com'),
                          recipients=[email])
            msg.html = render_template('mail.html', name=name)
            mail.send(msg)
            session['unconfirmed_user'] = {'email': email, 'name': name}

            def del_if_unconfirmed():
                time.sleep(3600)
                user = User.query.filter_by(email=email).first()
                if not user.is_logged_in:
                    db.session.delete(user)
                    db.session.commit()

            t = threading.Thread(target=del_if_unconfirmed, name='thread1')
            t.start()

            return redirect(url_for('confirm_email'))
        else:
            print("1ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    class LoginForm(FlaskForm):
        email = StringField('email', validators=[DataRequired(), Email()])
        password = PasswordField('password', validators=[DataRequired()])

    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password2 = form.password.data
        user = User.query.filter_by(email=email).first()
        if form.validate_on_submit():
            if all([user, user.password == password2, user.is_logged_in]):
                session['email'] = email
                return redirect(url_for('index'))
        else:
            print("ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    return render_template('login.html', form=form)


@app.route('/sign_out')
def sign_out():
    if session.get('email', False):
        session.pop('email')
    return redirect(url_for('index'))


@app.route('/email')
def confirm_email():
    return render_template('confirm_email.html')


@app.route('/success_registration')
def success_registration():
    User.query.filter_by(email=session.get('unconfirmed_user', '')['email']).first().is_logged_in = True
    return render_template('register_success.html')


@app.route('/email_already_exists')
def email_already_exists():
    return render_template('register_success.html')


# Start Programm ######################################################################
if __name__ == '__main__':
    app.run()
