import bcrypt
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, id, username, password, name ="", lastname="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.name= name
        self.lastname = lastname
    
    @classmethod
    def check_password(self, hashed_password, password):
        password = password.encode()
        hashed_password = hashed_password.encode()
        return bcrypt.checkpw(password, hashed_password)
    
    def encodepass(self, password):
        password = password.encode()
        step = bcrypt.gensalt()
        hash = bcrypt.hashpw(password, step)
        return hash
