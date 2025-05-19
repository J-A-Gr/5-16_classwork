from . import db # __init__ import


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    
    profile = db.relationship('UserPersonalData', back_populates='user', uselist=False) # uselist one-to-one užtikrina

    def __repr__(self):
        return f'<User {self.email}>'
    
class UserPersonalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    phone_number =  db.Column(db.Integer, unique=True)
    gender = db.Column(db.String(10), nullable=True)
    
    user = db.relationship('User', back_populates='profile')