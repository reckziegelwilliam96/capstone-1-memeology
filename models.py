"""Models for Iconicle app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt

db = SQLAlchemy()

class User(db.Model):
    """Game User class."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    unique=True,
                    nullable=False)
        
    username = db.Column(db.Text,
                        nullable=False)
    
    password = db.Column(db.Text,
                        nullable=False)

    email = db.Column(db.Text,
                        nullable=False)

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Images(db.Model):
    """Meme Images class."""

    __tablename__ = "database_images"

    id = db.Column(db.Integer,
                    primary_key=True,
                    unique=True,
                    nullable=False)

    phrase = db.Column(db.Text,
                    nullable=False)
    
    image_data = db.Column(db.LargeBinary,
                    nullable=True)
    
    image_words = db.relationship('ImageWords', backref='images')

    guessed_images = db.relationship('GuessedImages', backref='database_images')

    generated_memes = db.relationship('GeneratedMemes', backref='database_images')

    in_progress_images = db.relationship('InProgessImages', backref='database_images') 


class ImageWords(db.Model):
    """Meme Image Keywords class."""

    __tablename__ = "image_words"

    id = db.Column(db.Integer,
                    primary_key=True,
                    unique=True,
                    nullable=False)

    word = db.Column(db.Text,
                    nullable=False)
    
    image_id = db.Column(db.Integer,
                        db.ForeignKey("database_images.id"))

class GuessedImages(db.Model):
    """Images with User Guesses class."""

    __tablename__ = "guessed_images"

    image_id = db.Column(db.Integer,
                        db.ForeignKey("database_images.id"),
                        primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        primary_key=True)
    
    status = db.Column(db.Text,
                        nullable=True)

    guessed_by = db.relationship('User', backref='users')

class InProgessImages(db.Model):
    """Incoplete User Guesses class."""

    __tablename__ = "in_progess_images"

    id = db.Column(db.Integer,
                    primary_key=True,
                    unique=True,
                    nullable=False)
    
    image_id = db.Column(db.Integer,
                        db.ForeignKey("database_images.id"))
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))
    
    status = db.Column(db.Text, 
                        db.ForeignKey("guessed_images.status"))

class GeneratedMemes(db.Model):
    """Generated Memes from Images class."""

    __tablename__ = "generated_memes"

    id = db.Column(db.Integer,
                    primary_key=True,
                    unique=True,
                    nullable=False)

    image_id = db.Column(db.Integer,
                        db.ForeignKey("database_images.id"))

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))
    
    is_favorite = db.Column(db.Boolean,
                        nullable=False)

    generated_by = db.relationship('User', backref='generated_memes')
                        
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)