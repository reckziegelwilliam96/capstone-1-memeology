from flask import Flask, g, render_template, request, session, flash, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from werkzeug.utils import secure_filename

from forms import UserAddForm, LoginForm
from models import GuessedImages, InProgressImages, db, connect_db, User, Images, ImageWords

import requests, random

app = Flask(__name__)


CURR_USER_KEY = "curr_user"


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///memeo-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'memeo-key'
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
            return render_template('users/signup.html', form=form)
        
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
        return redirect('/login')
    
    if not session:
        return redirect('/select-game-meme')
    else:
        return render_template('index.html')

@app.route('/home')
def render_home_page():
    
    if not g.user:
        return redirect('/login')

    round = session["round"]
    round_meme = session["round_meme"]
    
    guess_image_id = session["guess_image"]
    guess_image = GuessedImages.query.filter_by(id=guess_image_id).first()

    if round_meme is None or round >= 5 or guess_image.completed == True:
        return redirect('/select-game-meme')

    src = session["src"]
    
    return render_template("home.html", src=src)

@app.route('/instructions')
def render_instructions_page():

    return render_template("instructions.html")

@app.route('/game-over')
def render_game_over_page():

    return render_template("gameover.html")

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

@app.route('/api/caption-images', methods=['POST'])
def caption_image():
    """Get API list from Meme Generator API and send response to parseList function in JS"""
    print("GET_MEMES CALLED!")
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return "Internal Server Error", 500


@app.route('/api/save-memes', methods=['POST'])
def save_memes_to_db():
    """API call to save all memes into database."""
    print("SAVE_MEMES CALLED!")
    data = request.get_json()
    memes = data['memes']
    

    for meme in memes:
        new_image = Images(phrase=meme['name'], image_data=meme['url'])
        db.session.add(new_image)
        db.session.commit()
        for word in meme['name'].lower().replace("'", "").split():
            new_word = ImageWords(word=word, image_id=new_image.id)
            db.session.add(new_word)
            db.session.commit()

    return 'Memes saved to database'

##*************************************************************************************************##
## DB ROUTES##

### STILL NEEDS TO BE ADDED - GET METHOD?
@app.route('/select-game-meme')    
def select_meme_for_game():
    print("SELECT_GAME_MEME CALLED")

    if not g.user:
        return redirect('/login')

    user = g.user
    # SELECT RANDOM IMAGE FROM DATABASE
    current_image = Images.query.order_by(func.random()).first()

    # INSTANTIATE IMAGE FOR ROUND 
    round_meme = InProgressImages(
                image_id = current_image.id,
                user_id = user.id,
                in_round = True
                )
    guess_image = GuessedImages(
                image_id = current_image.id,
                user_id = user.id,
                round = 0,
                completed = False
                )

    db.session.add(round_meme)
    db.session.add(guess_image)
    db.session.commit()

    print(guess_image.round)

    # SAVE TO SESSION FOR REFERENCE ON INDEX
    session["round_meme"] = round_meme.id
    session["round"] = 0

    session["guess_image"] = guess_image.id
    session["src"] = guess_image.database_images.image_data

    print(session["round_meme"])
    return redirect('/home')
    

@app.route('/update-game-meme')
def update_guessed_image():
    print("UPDATE_GUESSED_IMAGE CALLED!")

    # ROUND NEEDS TO BE REFERENCED -  UPDATE GUESSEDIMAGE ROUND
    round = session['round']
    round_meme_id = session["round_meme"]
    round_meme = InProgressImages.query.filter_by(id=round_meme_id).first()
    guess_image_id = session["guess_image"]
    guess_image = GuessedImages.query.filter_by(id=guess_image_id).first()

    update_image = round_meme.guessed_images[0]
    print(f"BEFORE UPDATE: {update_image.round}")

    if guess_image != update_image:
        return 'Internal Reference Error: Session and Database'

    # FROM GAME.JS
    keyword = request.args['keyword']

    if update_image is None or round_meme.in_round == False or update_image.completed == True:
        return 'No game meme found in session'

    image = update_image.database_images

    if image is None:
        return 'No image found for game meme'

    words = {word.word.lower() for word in image.image_words}
    if keyword.lower() in words:
        round += 1
        session["round"] = round
        update_image.round = round
        phrase = update_image.database_images.phrase
        print(phrase)
        guess_image.completed = True
        db.session.commit()
        session.clear()
        return jsonify({'result': 'correct', 'message': 'You are a Lord over Lords.', 'phrase': phrase})

    else:
        # Update the game round and save the updated object
        if round >= 5:
            phrase = update_image.database_images.phrase
            print(phrase)
            update_image.completed = True
            db.session.commit()
            session.clear()
            return jsonify({'result': 'game-over', 'message': "You've run out of guesses.", 'phrase': phrase})
            
        else:
            round += 1
            session["round"] = round
            update_image.round = round
            print(f"AFTER UPDATE:{update_image.round}")
            db.session.commit()
            # Return the updated game_meme object in the JSON response
            return jsonify({'result': 'not-correct', 'message': 'Better luck next time.'})

