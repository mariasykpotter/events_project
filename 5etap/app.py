import threading
import time

import folium
import geopy
import requests
from datetime import date
from flask import Flask, render_template, redirect, url_for, request, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.exc import IntegrityError
from wtforms import StringField, PasswordField
from wtforms.validators import Email, EqualTo, DataRequired

from linked_list import LinkedList

# App Config ###########################################################################
app = Flask(__name__)


class Configuration:

    '''
    This is a class which decribes an app configuration.
    '''

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SECRET_KEY'] = 'very_secret_key'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['DEBUG'] = True
    app.config['MAIL_USERNAME'] = 'testovemylo805@gmail.com'
    app.config['MAIL_PASSWORD'] = 'january2019'


app.config.from_object(Configuration)

db = SQLAlchemy(app)
mail = Mail(app)

# Models ###############################################################################


history = db.Table('history',
                   db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                   db.Column('event_id', db.Integer, db.ForeignKey('events.id'))
                   )


class User(db.Model):
    """
    This a class for User representation.

    Parameters:
    ---------
    :param id: str
    :param email: str
    :param name: str
    :param role: str
    :param password: str
    :param confirmed: boolean
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, index=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(128))
    role = db.Column(db.String(5), default='user')
    confirmed = db.Column(db.Boolean, default=False)
    events = db.relationship('Event', secondary=history, backref=db.backref('users', lazy='dynamic'))


class Event(db.Model):
    """

    This is a class for an Event representation.

    Parameters:
    ---------
    :param id: str
    :param id_eventful_com: str
    :param latitude: float
    :param longitude: float
    :param start_time: str
    :param title: str
    :param url: str
    :param venue_address: str
    """
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    id_eventful_com = db.Column(db.String(30), index=True)
    title = db.Column(db.String(100), index=True)
    start_time = db.Column(db.Text)
    city_name = db.Column(db.Text)
    venue_address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    url = db.Column(db.Text)

    def __init__(self, id_eventful_com, title, start_time, city_name, venue_address, latitude, longitude, url):
        '''
        Initialises a class Event
        '''
        self.id_eventful_com = id_eventful_com
        self.title = title
        self.start_time = start_time
        self.city_name = city_name
        self.venue_address = venue_address
        self.latitude = latitude
        self.longitude = longitude
        self.url = url


# Views ################################################################################
events_list = LinkedList()


@app.route('/')
def index():
    '''
   Returns the rendered template of html code.
   '''
    today = str(date.today())
    user_key = 'SSqPdQ5xLbF6dwN2'
    event_location = request.args.get('city', '')
    date_start = ''.join(request.args.get('date_start', '').split('-'))
    date_end = ''.join(request.args.get('date_end', '').split('-'))
    page_size = 30

    def count_event_pages(user_key, event_location, date_start, date_end, page_size):
        url = "http://api.eventful.com/json/events/search?" \
              "&app_key={}&location={}&date={}00-{}00&page_size={}". \
            format(user_key, event_location, date_start, date_end, page_size)
        return int(requests.get(url).json()['page_count'])

    def get_event_page(user_key, event_location, date_start, date_end, page_size, page_number):
        url = "http://api.eventful.com/json/events/search?" \
              "&app_key={}&location={}&date={}00-{}00&page_size={}&page_number={}". \
            format(user_key, event_location, date_start, date_end, page_size, page_number)
        for i in requests.get(url).json()['events']['event']:
            event = Event(id_eventful_com=i['id'],
                          title=i['title'],
                          start_time=i['start_time'],
                          city_name=i['city_name'],
                          venue_address=i['venue_address'],
                          latitude=i['latitude'],
                          longitude=i['longitude'],
                          url=i['url'])
            events_list.insert(event)

    if request.args:
        count_event_pages = count_event_pages(user_key=user_key, event_location=event_location, date_start=date_start,
                                              date_end=date_end, page_size=page_size)
        threads = []
        for i in range(count_event_pages):
            t = threading.Thread(target=get_event_page, name='thread{}'.format(i),
                                 args=(user_key, event_location, date_start, date_end, page_size, i + 1))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        geolocator = geopy.Nominatim(user_agent='Event')
        location = geolocator.geocode(event_location)
        m = folium.Map(location=(location.latitude, location.longitude), zoom_start=12)
        for i in events_list:
            popup = folium.Popup(
                '<a href="{}" target="_blank">{}</a>'.format(url_for('event', id=i.id_eventful_com), i.title))

            folium.Marker([float(i.latitude), float(i.longitude)], popup=popup).add_to(m)
        m.save('templates/map.html')
    else:
        m = folium.Map(location=(39.467697, 3.036337), zoom_start=3)
        m.save('templates/map.html')

    return render_template('index.html', today=today)


@app.route('/map')
def map():
    '''
    Returns the rendered template of map page.
    Returns:
        html file 'map html'
    '''
    return render_template('map.html')


@app.route('/location')
def location():
    '''
    Returns the rendered template of location code.
    Returns:
        html file 'location html'
    '''
    return render_template('location.html')


@app.route('/event/<id>')
def event(id):
    for i in events_list:
        if i.id_eventful_com == id:
            geolocator = geopy.Nominatim(user_agent='Event')
            location = geolocator.geocode(i.city_name)
            m = folium.Map(location=(location.latitude, location.longitude), zoom_start=12)
            folium.Marker([float(i.latitude), float(i.longitude)]).add_to(m)
            m.save('templates/location.html')

            event = Event(id_eventful_com=i.id_eventful_com,
                          title=i.title,
                          start_time=i.start_time,
                          city_name=i.city_name,
                          venue_address=i.venue_address,
                          latitude=i.latitude,
                          longitude=i.longitude,
                          url=i.url)
            db.session.add(event)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

            event = Event.query.filter_by(id_eventful_com=id).first()
            user = User.query.filter_by(email=session['email']).first()
            user.events.append(event)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    url = 'http://eventful.com/events/formation-sur-le-changemen-/{}'.format(id)
    return render_template('event.html', url=url)


@app.route('/profile/<user_id>')
def profile(user_id):
    '''
    Returns the rendered template of html code for user history page.
    '''
    user = User.query.filter_by(id=user_id).first()
    events = user.events
    return render_template('profile.html', events=events)


@app.route('/register', methods=['POST', 'GET'])
def register():
    '''
    Returns the rendered template of html code for a RegistrationForm
    '''

    class Regih strationForm(FlaskForm):
        '''Initialises a RegistrationForm.
            Returns:
            'register.html'
        '''
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
            if User.query.filter_by(email=email).first():
                return redirect(url_for('email_already_exists'))
            else:
                db.session.add(new_user)
                db.session.commit()
            msg = Message('confirm events registration', sender=('Events team', 'testovemylo805@gmail.com'),
                          recipients=[email])
            msg.html = render_template('mail.html', name=name)
            mail.send(msg)
            session['unconfirmed_user'] = {'email': email, 'name': name}

            def del_if_unconfirmed():
                '''Deletes a form information if it is unconfirmed
                Returns:
                    register.html
                '''
                time.sleep(3600)
                user = User.query.filter_by(email=email).first()
                if not user.confirmed:
                    db.session.delete(user)
                    db.session.commit()

            t = threading.Thread(target=del_if_unconfirmed, name='thread1')
            t.start()

            return redirect(url_for('confirm_email'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    '''
    Returns the rendered template of login.html.
    Returns:
        login.html
    '''

    class LoginForm(FlaskForm):
        '''This is a class for LoginForm representation.'''
        email = StringField('email', validators=[DataRequired(), Email()])
        password = PasswordField('password', validators=[DataRequired()])

    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password2 = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if form.validate_on_submit():
                if all([user, user.password == password2, user.confirmed]):
                    session['email'] = email
                    session['name'] = user.name
                    session['user_id'] = user.id
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('login_error'))
        else:
            return redirect(url_for('login_error'))

    return render_template('login.html', form=form)


@app.route('/sign_out')
def sign_out():
    '''
    Returns the rendered template to sign out.
    '''
    if session.get('email', False):
        session.pop('email')
    return redirect(url_for('index'))


@app.route('/email')
def confirm_email():
    '''
    Returns the rendered template to confirm an email.
    '''
    return render_template('confirm_email.html')


@app.route('/success_registration')
def success_registration():
    '''
    Returns the rendered template to prove the success of registration.
    '''
    User.query.filter_by(email=session.get('unconfirmed_user', '')['email']).first().confirmed = True
    return render_template('register_success.html')


@app.route('/email_already_exists')
def email_already_exists():
    '''
    Returns the rendered template if email already exists.
    '''
    return render_template('email_already_exists.html')


@app.route('/login_error')
def login_error():
    '''
    Returns the rendered template if user enters incorrect data.
    '''
    return render_template('login_error.html')


# Start Programm ######################################################################
if __name__ == '__main__':
    app.run()
