from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects import postgresql
# for tokens
from datetime import datetime,timedelta
import secrets

class User(db.Model):
    # user is a reserved word in Postgres, so we'll call our table users (plural, not singular)
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, index=True, unique=True, nullable=False)
    email = db.Column(db.Text, index=True, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    is_host = db.Column(db.Boolean())
    token = db.Column(db.Text, index=True, unique=True)
    token_expiration = db.Column(db.DateTime) #date and time at which the token expires
    phone = db.Column(db.Text, unique=True) 
    gender = db.Column(db.Text)  
    # not actually a column in table. but you can find all listings by a host
    # by using host.listings
    listings = db.relationship('Accommodation', backref='host', lazy='dynamic')
    reservations = db.relationship('Reservation', backref='guest', lazy='dynamic')
    #favourites = db.relationship('Favourite', backref='user', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        if self.phone:
            data['phone'] = self.phone

        if self.gender:
            data['gender'] = self.gender

        return data
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self,expiration=3600):
        now = datetime.utcnow()
        #check if the current token has at least a minute left before expiration
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            #if true, the existing token is returned
            return self.token

        self.token = secrets.token_urlsafe(24)
        self.token_expiration = now + timedelta(seconds=expiration)
        db.session.add(self)
        return self.token

    def revoke_token(self):#revoke a token immediately
        #set the expiration date to one second before the current time
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
    
    @staticmethod
    # TODO: should this also revoke token if it is expired?
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        #if the token is invalid  or expired,return none
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user #otherwise, return the user object

    def __repr__(self):
        return '<User {}>'.format(self.username)
    

class Accommodation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    num_guests = db.Column(db.Integer, nullable=False)
    num_bedrooms = db.Column(db.Integer, nullable=False)
    num_beds = db.Column(db.Integer, nullable=False)
    num_bathrooms = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    property_type = db.Column(db.Text, nullable=False)
    num_reviews = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text)
    suburb = db.Column(db.Text)
    state = db.Column(db.Text)
    amenities = db.Column(postgresql.ARRAY(db.Text))
    image_urls = db.Column(postgresql.ARRAY(db.Text))
    is_deleted = db.Column(db.Boolean(), nullable=False)

    #the average of other ratings from all the reviews(corresponding to one reservation)
    rating = db.Column(db.Float)    
    scores_accuracy = db.Column(db.Integer) # 0-10
    scores_location = db.Column(db.Integer)
    scores_communication = db.Column(db.Integer)
    scores_check_in = db.Column(db.Integer)
    scores_cleanliness = db.Column(db.Integer)
    scores_value = db.Column(db.Integer)

    reservations = db.relationship('Reservation', backref='accommodation', lazy='dynamic')

    #all the favourites record related to this accommodation
    #favourites = db.relationship('Favourite', backref='accommodation', lazy='dynamic')

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            cname = column.name
            attr = getattr(self, cname)
            if attr:
                if cname in ['name', 'description', 'suburb', 'city', 'state', 'country', 'property_type']:
                    d[cname] = str(attr)
                else:
                    d[cname] = attr
        return d

    def to_dict_1(self):
        d = {}
        for column in self.__table__.columns:
            cname = column.name
            attr = getattr(self, cname)
            if attr:
                if cname in ['id', 'name', 'suburb', 'city', 'price', 'rating','num_reviews']:
                    d[cname] = str(attr)
                if cname in ['image_urls']:
                    d[cname] = attr
        return d

    def update_with_dict(self, d):
        for col, val in d.items():
            setattr(self, col, val)

    def __repr__(self):
        return '<Accommodation {}>'.format(self.name)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodation.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Text, nullable=False) # booked, checked_in, checked_out, cancelled

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            cname = column.name
            if cname in ['check_in_date', 'check_out_date', 'status']:
                d[cname] = str(getattr(self, cname))
            else:
                d[cname] = getattr(self, cname)
        return d

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodation.id'), nullable=False)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) #overall/average rating  0-10
    # user must rate all the following six if giving review
    scores_accuracy = db.Column(db.Integer, nullable=False) # 0-10
    scores_location = db.Column(db.Integer, nullable=False)
    scores_communication = db.Column(db.Integer, nullable=False)
    scores_check_in = db.Column(db.Integer, nullable=False)
    scores_cleanliness = db.Column(db.Integer, nullable=False)
    scores_value = db.Column(db.Integer, nullable=False)
    is_anonymous = db.Column(db.Boolean()) #if True, guest's username should not be presented
    review = db.Column(db.Text) #optional
    
    def to_dict(self):
        data = {
            'id': self.id,
            'reservation_id':self.reservation_id,
            'guest_id': self.guest_id,
            'rating': self.rating,
            'is_anonymous':self.is_anonymous,
            'review':self.review
            }
        return data
'''
class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodation.id'), nullable=False)
    is_valid = db.Column(db.Boolean()) # False means the saved acc has been deleted
'''
