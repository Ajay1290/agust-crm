import pytz
import datetime
from hashlib import md5
from collections import OrderedDict

from flask import current_app
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from manager.ext import db,dbt
from manager.libs.utils.util_sqlalchemy import ResourceMixin, AwareDateTime

class Employee(UserMixin, ResourceMixin, db.Model):
    ROLE = OrderedDict([
        ('engineer', 'Engineer'),
        ('manager', 'Manager'),
        ('admin', 'Admin')
    ])

    id = db.Column(db.Integer, primary_key=True)
    
    # Authentication.
    role = db.Column(db.Enum(*ROLE, name='role_types', native_enum=False), nullable=False, server_default='engineer')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    name = db.Column(db.String(24), unique=True)
    phone = db.Column(db.String(13))
    email = db.Column(db.String(255), unique=True, nullable=False, server_default='')
    password = db.Column(db.String(128), nullable=False, server_default='')

    # Activity tracking.
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))

    def __init__(self, **kwargs):
        super(Employee, self).__init__(**kwargs)
        self.password = Employee.encrypt_password(kwargs.get('password', ''))

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

    def update_activity_tracking(self, ip_address):
        self.sign_in_count += 1
        self.active = True

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_on = datetime.datetime.now(pytz.utc)
        self.current_sign_in_ip = ip_address

        return self.save()