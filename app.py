from flask import Flask, g, render_template, request, session, flash, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import os, base64

from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from forms import UserAddForm, LoginForm
from models import GuessedImages, db, connect_db, User, Images, ImageWords

import requests, random

app = Flask(__name__)


CURR_USER_KEY = "curr_user"


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///iconicle-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'iconicle-key'
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()
##*************************************************************************************************##

@app.before_request
def add_user_to_g():
    """If logged in, add user to global G variable."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    """Handle user signup."""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data
            )
            db.session.commit()

        except IntegrityError:
            flash('Username taken', 'danger')
            return render_template('users/signup.html', form-form)
        
        do_login(user)

        return redirect('/')
    
    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["POST", "GET"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                form.password.data)
        
        if user:
            do_login(user)
            flash(f"Welcome back, {user.username}", 'success')

            return redirect('/')

        flash("Invalid credentials", 'danger')

    return render_template('/users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle user logout."""
    user = g.user

    if user:
        do_logout()
        flash(f"Until next time, {user.username}!", 'success')

        return redirect('/')

    form = UserAddForm()
    return render_template("users/signup.html", form=form)

##*************************************************************************************************##
##REQUEST ROUTES##
@app.route('/')
def index():
    """Show index page."""

    if not g.user:
        return render_template('home-anon.html')


    return render_template('index.html')

@app.route('/home')
def display_home():
    
    if not g.user:
        return render_template("home-anon.html")

    user = g.user
    game_meme = GuessedImages.query.filter_by(user_id=user.id, round=0).first()
    src = game_meme.database_images.image_data



    return render_template("home.html", src=src)



##*************************************************************************************************##
##EXTERNAL API##

@app.route('/api/get-memes', methods=['GET'])
def get_memes():
    """Get API list from Meme Generator API and send response to parseList function in JS"""
    print("GET_MEMES CALLED!")
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return "Internal Server Error", 500



##*************************************************************************************************##
## DB ROUTES##

@app.route('/api/save-memes-to-db', methods=['POST'])
def save_memes_to_db():
    print("SAVE_MEMES CALLED!")
    data = request.get_json()
    memes = data['memes']
    user = g.user

    for meme in memes:
        new_image = Images(phrase=meme['name'], image_data=meme['url'])
        print(new_image.image_data)
        db.session.add(new_image)
        db.session.commit()
        for word in meme['name'].lower().replace("'", "").split():
            new_word = ImageWords(word=word, image_id=new_image.id)
            db.session.add(new_word)
            db.session.commit()
    
    game_image = GuessedImages(
                image_id=new_image.id,
                user_id=user.id,
                round=0
                )
    db.session.add(game_image)
    db.session.commit()

    return 'Memes saved to database'


@app.route('/compare-word-to-db')
def compare_word_to_db():
    print("COMPARE_WORDS CALLED!")
    user = g.user

    keyword = request.args['keyword']

    game_meme = GuessedImages.query.filter_by(user_id=user.id).first()

    if game_meme is None:
        return 'No game meme found in session'

    
    image = game_meme.database_images
    if image is None:
        return 'No image found for game meme'

    words = {word.word.lower() for word in image.image_words}
    if keyword.lower() in words:
        return jsonify({'result': 'correct', 'message': 'Correct keyword!'})
    else:
        # Update the game round and save the updated object
        game_meme.round += 1
        db.session.add(game_meme)
        db.session.commit()
        # Return the updated game_meme object in the JSON response
        return jsonify({'result': 'not-correct', 'message': 'Incorrect keyword.'})
