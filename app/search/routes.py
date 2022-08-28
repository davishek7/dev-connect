from flask import render_template, request
from . import search
from ..database import db, SCHEMA
from app.auth.decorators import login_required


@search.route('/', methods=['GET'])
@login_required
def search_dev():
    search_term = request.args.get('q')
    user = db.sql(f'SELECT * FROM flaskdev.user WHERE username LIKE {search_term}')
    print(user)
    return render_template('index.html')