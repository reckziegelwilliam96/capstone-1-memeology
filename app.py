from flask import Flask, g, render_template, request, session, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm
from models import db, connect_db, User, Images, ImageWords

import requests, random, base64

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///iconicle-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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

    return render_template('/users/login.html')

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

@app.route('/')
def homepage():
    """Show home page."""
    
    return render_template('home.html')



##*************************************************************************************************##

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

##*************************************************************************************************##

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
        
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occured: {req_err}')
    except Exception as e:
        print(f'An error occurred:{e}')

    return response.content, 200, {'Content-Type': 'application/octet-stream'}

