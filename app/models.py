from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
#from app import db
from flask_login import UserMixin

class User( UserMixin ):
    def __init__(self, id, email, password, rol):
        self.id = id
        self.email = email
        self.password = generate_password_hash( password )
        self.rol = rol
   # password_hash = db.Column( db.String( 128 ) )

    def __repr__( self ):
        return "< Usuario {} >".format( self.email)

    def set_password( self , password ) :
        self.password_hash = generate_password_hash( password )

    def check_password( self , password ):
        return check_password_hash( self.password , password )



# login testing users

users = []

def get_user(email):
    for user in users:
        if user.email == email:
            return user

    return None


'''
@login.user_loader
def load_user( id ):
    return User.query.get( int( id ) )'''