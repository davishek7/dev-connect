from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_toastr import Toastr


bcrypt = Bcrypt()
csrf = CSRFProtect()
toastr = Toastr()