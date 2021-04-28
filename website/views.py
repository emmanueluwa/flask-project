from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json

# current useer package is used to detect if a user is logged in or not
##---- gives us all info about user that is logged in, if not user will be anonymous
from .models import Note
# define this file is a blueprint of app, aka has a bunch of routes inside it, bunch of urls defined
views = Blueprint('views', __name__) # setup blueprint for flask app
from . import db


#defining route. function will run whenever we go to / route. allowing post method for this route(methods..)
@views.route('/', methods=['GET', 'POST'])
#login required decorator, meaning you can only access homepage if logged in
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note') #allowing us to post a note

        if len(note) < 1:
            flash('Length of Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')


    return render_template("home.html", user=current_user)#we can reference current user and check authentication
    # all this needs to be registered into init.py

#view needed to delete post
# request will be loaded as json since it comes in in the data parameter of request object, note id needs to be looked for
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) #request data(from POST request) is a string which is sent from index.js
    #string is turned into a python dictionary object, noteID attribute is acessed and note is found
    noteId = note['noteId']
    note = Note.query.get(noteId)# look for note with this ID
    if note: #does note exist
        if note.user_id == current_user.id: #does user who is signed in own note
            #to delete object, query it then put it inside delete
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({}) # return empty response, something needs to be returned(req from flask)

