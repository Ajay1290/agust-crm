from flask import Blueprint

users = Blueprint('users', __name__)

from .auths import *
from .genrearl import *