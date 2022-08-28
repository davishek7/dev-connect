from re import search
from flask import Blueprint

search = Blueprint('search', __name__)

from . import routes