#db model is needed for users and also notes
# . is current package. website folder.

from . import db
from flask_login import UserMixin # custom class helps users login// user object inherits from userMixin
from sqlalchemy.sql import func

#note object
# db model, all notes must look like this. makes info consistent
#db software automatically increments id's, +1 each time
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    #func will get us current date and time and store it as default value
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #foriegn key(key on db table that referneces id to another db column) relationships/all notes must belong to a user
    #for every note, the user id will tell us which user created it
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#1 to many relationship./1 user can have many notes./ lowercase for foreignkey


# to make a new db model, store a different type of object. define name then inherit from db.model
class User(db.Model, UserMixin):
    #define all columns we want stored in this table
    # primary key is unique identifier to differentiate 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # max length is 150, unique=True means no user can have same email
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # all users should be able to find all of there notes, will store all notes user creates
    notes = db.relationship('Note') #uppercase when referencing class