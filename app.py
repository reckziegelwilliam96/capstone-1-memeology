from flask import Flask, g, render_template, request, session, flash, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import os

from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from forms import UserAddForm, LoginForm
from models import db, connect_db, User, Images, ImageWords
from iconicle import Iconicle

import requests, random

app = Flask(__name__)



CURR_USER_KEY = "curr_user"


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///iconicle-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'iconicle-key'
debug = DebugToolbarExtension(app)

iconicle_game = Iconicle()

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
##DISPLAY ROUTES##
@app.route('/')
def homepage():
    """Show home page."""

    if not g.user:
        return render_template('home-anon.html')

    return render_template("home.html")

@app.route('/start-game')
def gamepage():
    """Show game page."""

    if not g.user:
        return render_template('home-anon.html')

    board = iconicle_game.make_board()

    session["board"] = board
    session["round"] = 0

    return render_template("game.html", board=board, round=0)


##*************************************************************************************************##
##GAMEPLAY ROUTES##

@app.route("/save-meme", methods=["POST"])
def save_meme():
    
    if "meme" in request.files:
        file = request.files["meme"]
        if file:
            meme = session["meme"]
            print(meme)
            filename = f"{meme}_{secure_filename(file.filename)}"
            file.save(os.path.join("images", filename))
            response = jsonify({"message": "Meme saved successfully"})
            response.status_code = 200
            return response
        else:
            response = jsonify({"error": "File not found in the request"})
            response.status_code = 400
            return response
    else:
        response = jsonify({"error": "Meme field not found in the request"})
        response.status_code = 400
        return response


##*************************************************************************************************##
##EXTERN API: RAPID API'S MEME GENERATOR ROUTES##

@app.route('/api/get-images-list')
def get_api_list_images():
    """Get API list from Meme Generator API and send response to parseList function in JS"""

    url = "https://ronreiter-meme-generator.p.rapidapi.com/images"

    headers = {
    	"X-RapidAPI-Key": "4107f9a719msh7b803084f28bdd6p10d9b2jsn4c84f0422879",
    	"X-RapidAPI-Host": "ronreiter-meme-generator.p.rapidapi.com"
    }
    
    try:
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()

        return response.text

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occured: {req_err}')
    except Exception as e:
        print(f'An error occurred:{e}')

@app.route('/api/get-generate-meme')
def get_api_generate_meme():
    """Get random meme from session 
    using predefined images in API Meme Generator."""
    meme = session['meme']

    url = "https://ronreiter-meme-generator.p.rapidapi.com/meme"

    querystring = {"top":".",
                    "bottom":".",
                    "meme":f"{meme}",
                    "font_size":"1",
                    "font":"Impact"
                    }

    headers = {
	    "X-RapidAPI-Key": "4107f9a719msh7b803084f28bdd6p10d9b2jsn4c84f0422879",
	    "X-RapidAPI-Host": "ronreiter-meme-generator.p.rapidapi.com"
    }
    
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)

        image = Images.query.filter_by(phrase=meme).first()
        image.image_data = response.content
        db.session.commit()
        
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occured: {req_err}')
    except Exception as e:
        print(f'An error occurred:{e}')

    return (response.content, 200, {'Content-Type': 'application/octet-stream'})

##*************************************************************************************************##
##SEED DB ROUTES USING EXTERNAL API##

@app.route('/api/post-meme-names-seed-db', methods=["POST"])
def post_meme_names_seed_iconicle_db():
    """Seed database with post request from JS file, 
    parse random_images phrases into Meme class, 
    parse again into MemeWords class """
    

    try:
        random_images = request.get_json()
        
        for image_phrase in random_images:
            created_image = Images(phrase=image_phrase)
            db.session.add(created_image)
            db.session.commit()

            words = image_phrase.split("-")
            for word in words:
                print(f"created_image type:{type(created_image)}")
                image_word = ImageWords(word=word, image_id=created_image.id)
                db.session.add(image_word)
                db.session.commit()
    except Exception as e:
        print(f"Error processing data: {e}")
        db.session.rollback()
        return "Error processing data", 500


    response = random.choice(random_images)
    session['meme'] = response

    return response