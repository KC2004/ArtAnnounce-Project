"""Models and database functions for artshare db."""

from flask_sqlalchemy import SQLAlchemy

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Compose ORM
##############################################################################
# User Info Tables
##############################################################################

class User(db.Model):
    """User table"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'), nullable=True)
    login = db.Column(db.String(25), db.ForeignKey('app_users.login'), nullable=True)

    app_user = db.relationship('AppUser')
    address = db.relationship('Address', backref=db.backref('user'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s name=%s %s >" % (self.user_id,
                                                self.first_name,
                                                self.last_name)

class TwitterUser(db.Model):
    twitter_handle = db.Column(db.String(20), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', backref=db.backref('twitter_user'))
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User_id %s, Twitter handle: %s>" % (self.user_id,
                                                    self.twitter_handle)



class AppUser(db.Model):
    """App registrant's login info"""

    __tablename__ = "app_users"
    
    login = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    # authorization_code_id = db.Column(db.Integer, db.ForeignKey('authorizations.auth_id'), nullable=True)
    
    # user = db.relationship('User')
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Login info: classified>" 



class Address(db.Model):
    """Addresses of users"""

    __tablename__ = "addresses"

    address_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    address_line1 = db.Column(db.String(100), nullable=True)
    address_line2 = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(30), nullable=True)
    state = db.Column(db.String(5), nullable=True)
    zip_code = db.Column(db.String(12), nullable=True)
    country = db.Column(db.String(30), nullable=True)
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User %s, City: %s, State: %s >" % (self.user_id,
                                                self.city,
                                                self.state)


class Artist(db.Model):
    """Artist's info"""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bio = db.Column(db.String(2000), nullable=True)
    statement = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    # jpg = db.Column(db.Blob, nullable=True)

    user = db.relationship('User', backref=db.backref('artist'))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Artist_id: %s>" % (self.artist_id)


class Patron(db.Model):
    """Patron's info"""

    __tablename__ = "patrons"

    patron_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    patron_info = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    artworks = db.relationship('Artwork', secondary='artwork_patron')
    user = db.relationship('User', backref=db.backref('patron'))
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Patron id: %s\n>" % (self.patron_id)


class ArtFan(db.Model):
    """Art fan info"""

    __tablename__ = "fans"

    fan_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    patron_info = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('User', backref=db.backref('fan'))
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Fan id: %s>" % (self.fan_id)


# class AuthorizationCodes(db.Model):
#     """App user's authorization info for different social media sites"""
#     """"work in progress"""

#     __tablename__ = "authorizations"
    
#     auth_id = db.Column(db.String(20), primary_key=True)
#     login = db.Column(db.String(20), primary_key=True)
#     password = db.Column(db.String(20), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
#     user = db.relationship('User')
    
#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Login info: classified>" 



##############################################################################
# ArtWork and Sharing Tables
##############################################################################

class Artwork(db.Model):
    """Artwork table"""

    __tablename__ = "artworks"

    artwork_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))
    title = db.Column(db.String(50), nullable=True)
    year_created = db.Column(db.Integer, nullable=True)
    medium_id = db.Column(db.Integer, db.ForeignKey('mediums.medium_id'), nullable=True)
    substrate_id = db.Column(db.Integer, db.ForeignKey('substrates.substrate_id'), nullable=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=True)
    length = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    depth = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(200), nullable=True)
    # jpg = db.Column(db.Blob, nullable=True)
    availability_id = db.Column(db.Integer, db.ForeignKey('availabilities.availability_id'))

    artist = db.relationship('Artist', backref=db.backref('artwork'))
    medium = db.relationship('Medium')
    substrate = db.relationship('Substrate')
    genre = db.relationship('Genre')
    availability = db.relationship('Availability')
    patron = db.relationship('Patron', secondary='artwork_patron')

    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Artwork_id: = %s \nArtist_id: %s\n title: %s\n medium_id: %s >" % (self.artwork_id,
                                                self.artist_id,
                                                self.title,
                                                self.medium_id)


class Medium(db.Model):
    """Artwork Medium"""

    __tablename__ = "mediums"
    
    medium_id = db.Column(db.Integer, primary_key=True)
    medium = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Medium id: %s\nMedium:%s\n>" % (self.medium_id,
                                                self.medium)

class Substrate(db.Model):
    """Artwork Substrate"""

    __tablename__ = "substrates"
    
    substrate_id = db.Column(db.Integer, primary_key=True)
    substrate = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Substrate id: %s\Substrate:%s\n>" % (self.substrate_id,
                                                self.substrate)


class Genre(db.Model):
    """Artwork Substrate"""

    __tablename__ = "genres"
    
    genre_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Genre id: %s\Genre:%s\n>" % (self.genre_id,
                                                self.genre)


class Availability(db.Model):
    """Artwork Availability"""

    __tablename__ = "availabilities"
    
    availability_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    availability = db.Column(db.String(20), nullable=False)
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.gallery_id'), nullable=True)
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.patron_id'), nullable=True)
    

    artworks = db.relationship('Artwork')
    gallery = db.relationship('Gallery')
    patron = db.relationship('Patron')
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Artwork id: %s\nAvailability id: %s\nAvailability:%s\n>" % (self.artwork_id,
                                                                            self.availability_id,
                                                                            self.availability)

class Gallery(db.Model):
    """Gallery table"""

    __tablename__ = "galleries"
    
    gallery_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    address_id = db.Column(db.String(200), nullable=False)
    # genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=True)

    # genre = db.relationship('Genre')


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Gallery id: %s\ngallery:%s\n>" % (self.gallery_id,
                                                self.name)



class Artwork_Gallery(db.Model):
    """Availability through Gallery: Artwork_Gallery association table"""

    __tablename__ = "artwork_gallery"
    
    avail_glry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artwork_id = db.Column(db.Integer, 
                        db.ForeignKey('artworks.artwork_id'),
                        nullable=False)
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.gallery_id'),
                        nullable=False)

    
    gallery = db.relationship('Gallery')
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Artwork id: %s\nGallery id:%s\n>" % (self.artwork_id,
                                                        self.gallery_id)


class Artwork_Patron(db.Model):
    """If artwork is with patron: artwork-patron association table"""

    __tablename__ = "artwork_patron"
    
    artwork_ptrn_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artwork_id = db.Column(db.Integer, 
                        db.ForeignKey('artworks.artwork_id'),
                        nullable=False)
    patron_id = db.Column(db.Integer, db.ForeignKey('patrons.patron_id'),
                        nullable=False)

    
        
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Artwork id: %s\nPatron id:%s\n>" % (self.artwork_id,
                                                        self.patron_id)



class ArtShareInfo(db.Model):
    """table of shared artwork"""

    artshare_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artworks.artwork_id'),
                        nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False)
    socialmedia_id = db.Column(db.Integer, db.ForeignKey('socialmedia_tbl.socialmedia_id'),
                        nullable=False)
    
    artwork = db.relationship('Artwork')
    socialmedia = db.relationship('SocialMedia')

    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Caption: %s\nArtshareInfo id: %s\nSocialMedia id: %s\nArtwork_id id:%s\n>" % ( self.caption,
                                                            self.artshare_id,
                                                            self.socialmedia_id,
                                                            self.artwork_id)

class SocialMedia(db.Model):
    """ Social media sites"""
    __tablename__ = "socialmedia_tbl"

    socialmedia_id = db.Column(db.Integer, primary_key=True)
    socialmedia_name = db.Column(db.String(20), nullable=False)  # whether fb, twitter etc.
   
   
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<SocialMedia id: %s\Social Media name:%s\n>" % ( self.socialmedia_id,
                                                            self.socialmedia_name)


##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///artshare'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
