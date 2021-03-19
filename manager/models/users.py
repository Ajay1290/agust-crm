import pytz
import datetime
from hashlib import md5
from collections import OrderedDict

from flask import current_app
from flask_login import UserMixin

from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer

from manager.ext import db
from manager.libs.utils.util_sqlalchemy import ResourceMixin, AwareDateTime

class User(UserMixin, ResourceMixin, db.Model):

    ROLE = OrderedDict([
        ('member', 'Member'),
        ('admin', 'Admin')
    ])

    id = db.Column(db.Integer, primary_key=True)

    # Authentication.
    role = db.Column(db.Enum(*ROLE, name='role_types', native_enum=False), index=True, nullable=False, server_default='member')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    username = db.Column(db.String(24), unique=True, index=True)
    phone = db.Column(db.String(13))
    email = db.Column(db.String(255), unique=True, nullable=False, server_default='')
    password = db.Column(db.String(128), nullable=False, server_default='')
    phone_confirmed = db.Column(db.Boolean(), nullable=False, server_default='0')
    email_confirmed = db.Column(db.Boolean(), nullable=False, server_default='0')

    # Billing.
    name = db.Column(db.String(128), index=True)
    organization = db.Column(db.String(128))
    payment_id = db.Column(db.String(128), index=True)
    cancelled_subscription_on = db.Column(AwareDateTime())
    previous_plan = db.Column(db.String(128))
    
    # Billing Relationships.
    # credit_card = db.relationship(CreditCard, uselist=False, backref='users', passive_deletes=True)
    # subscription = db.relationship(Subscription, uselist=False, backref='users', passive_deletes=True)
    # invoices = db.relationship(Invoice, backref='users', passive_deletes=True)

    # Activity tracking.
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))

    # Additional settings.
    locale = db.Column(db.String(5), nullable=False, server_default='en')

    # RelationShips
    companies = db.relationship('Company', backref='owner', lazy=True)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(User, self).__init__(**kwargs)
        self.password = User.encrypt_password(kwargs.get('password', ''))
    
    
    @classmethod
    def find_by_identity(cls, identity):
        return User.query.filter((User.email == identity) | (User.username == identity)).first()
    
    
    @classmethod
    def encrypt_password(cls, plaintext_password):
        if plaintext_password:
            return generate_password_hash(plaintext_password)

        return None
    
    def authenticated(self, with_password=True, password=''):        
        if with_password:
            return check_password_hash(self.password, password)

        return True
    
    def is_active(self, act=False):
        if act:
            self.active = True
            return self.active
        return self.active

    def get_auth_token(self):        
        private_key = current_app.config['SECRET_KEY']
        serializer = URLSafeTimedSerializer(private_key)
        data = [str(self.id), md5(self.password.encode('utf-8')).hexdigest()]

        return serializer.dumps(data)

    def serialize_token(self, expiration=3600):        
        private_key = current_app.config['SECRET_KEY']
        serializer = TimedJSONWebSignatureSerializer(private_key, expiration)

        return serializer.dumps({'user_email': self.email}).decode('utf-8')

    @classmethod
    def confirm_email_token(cls, username, email, password, expiration=3600):
        private_key = current_app.config['SECRET_KEY']
        serializer = TimedJSONWebSignatureSerializer(private_key, expiration)

        token = serializer.dumps({'user_username': username,'user_email': email,'user_password': password}).decode('utf-8')

        return token

    @classmethod
    def deserialize_token(cls, token):        
        private_key = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            decoded_payload = private_key.loads(token)
            data = {'user_username':decoded_payload.get('user_username'),
                    'user_email':decoded_payload.get('user_email'),
                    'user_password':decoded_payload.get('user_password')}
            return data
        except Exception:
            return None
    
    def update_activity_tracking(self, ip_address):
        self.sign_in_count += 1
        self.active = True

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_on = datetime.datetime.now(pytz.utc)
        self.current_sign_in_ip = ip_address

        return self.save()
    
class Company(ResourceMixin, db.Model):    

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(24), unique=True, index=True)

    # Contant Info
    phone = db.Column(db.String(15), server_default='')
    email = db.Column(db.String(255), server_default='')    
    website = db.Column(db.String(255), server_default='')
    
    # Address
    address = db.Column(db.String(300), server_default='')
    pincode = db.Column(db.String(25), server_default='')
    city = db.Column(db.String(255), server_default='')
    state = db.Column(db.String(255), server_default='')
    country = db.Column(db.String(255), server_default='')

    # Tax Info
    gst = db.Column(db.String(15), server_default='')
    pan = db.Column(db.String(10), server_default='')

    # Meta Info
    is_active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # RelationShips
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)