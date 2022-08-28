import os
import harperdb
from dotenv import load_dotenv

load_dotenv()

db = harperdb.HarperDB(
    url = os.environ.get('HARPERDB_URL'),
    username = os.environ.get('HARPERDB_USERNAME'),
    password = os.environ.get('HARPERDB_PASSWORD'))

SCHEMA = os.environ.get('HARPERDB_SCHEMA')