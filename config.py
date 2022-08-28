import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MEDIA_DIR = 'media'
    TOASTR_POSITION_CLASS = 'toast-top-center'
    TOASTR_OPACITY = False