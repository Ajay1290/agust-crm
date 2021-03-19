from flask import Blueprint

customers = Blueprint('customers', __name__)

from .contacts import *
from .customers import *