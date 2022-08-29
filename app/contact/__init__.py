from flask import Blueprint

contact = Blueprint('contact', __name__)

from . import routes