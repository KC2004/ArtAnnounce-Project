"""ArtAnnounce"""

from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session, url_for
from model import User, AppUser, Address, Artist, Patron, ArtFan, Artwork, connect_to_db, db
from helper_functions import HelperFunctions
#import ArtAnnounceTwitter
import random


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/login')
def login():
    """Login page shows login form"""

    return render_template("login_form.html")


@app.route('/login', methods=["POST"])
def login_form():
    """Handle submission of login form"""

    mylogin = request.form.get('login')
    password = request.form.get('pwd')

    # check to see if user exists
    user_rec = AppUser.query.filter_by(login=mylogin).first()

    # if user doesn't exist, send to Registration page.
    if not user_rec:
        return render_template("register_form.html")

    # check to see if submitted password matches user_rec.password in db
    # if not, redirect to Login page.
    # else, Successfully Logged in. Take to Welcome page.
    else:
        if user_rec.password != password:
            flash('your login is incorrect')
            return redirect('/login')
        else:
            session['login'] = mylogin
            flash('You are successfully logged in %s' % session['login'])
            return redirect("/welcome")


@app.route('/welcome')
def welcome():
    """Login page shows login form"""

    return render_template("welcome.html")



@app.route('/show_art_page')
def show_art():
    """show art page"""

    return render_template("show_art_page.html")


@app.route('/artists_artwork')
def pick_artists_art():
    """Pick an Artist and genre to show work"""

    return render_template("artwork_page.html")


@app.route('/artists_artwork', methods=["POST"])
def show_artists_art():
    """show artwork of a particular Artist"""

    artist = request.form.get('artist')
    genre = request.form.get('genre')

    # if artist == 'kushlani':
    #     # check to see if user exists
    artwork_list = Artwork.query.filter_by(artist_id=1).all()

    return render_template("artwork_page.html", artwork_list=artwork_list) 


@app.route('/share_art_form')
def share_art():
    """show share art page to pick the artist and set share parameters"""

    return render_template("share_art_page.html")


@app.route('/share_art', methods=["POST"])
def share_art_social_media():
    """share art onsocial media"""
    artist = request.form.get('artist')
    genre = request.form.get('genre')
    frequency = request.form.get('frequency')
    interval = request.form.get('interval')
    number = request.form.get('number')

    artworks = Artwork.query.filter_by(artist_id=1).all()
    curr_artist = Artist.query.filter_by(artist_id=1).first()

    for i in range (0, int(number)):
        rand = random.randint(0,(len(artworks)-1))
        a = artworks[rand]
        a_firstname = curr_artist.user.first_name
        a_lastname =  curr_artist.user.last_name
        a_website = curr_artist.website
        # include artist name?

        helper = HelperFunctions()

        caption = helper.create_caption(firstname=a_firstname, lastname=a_lastname,
         title=a.title, height=a.height, length=a.length, medium=a.medium, substrate=a.substrate, website=a_website, genre=a.genre)

        caption = caption[:144]  # tweets can only be a max of 144 chars

 #       ArtAnnounceTwitter.post_tweet(caption, a.url)

    return render_template("welcome.html")


@app.route('/add_art_form')
def add_art():
    """show page to add artwork"""

    return render_template("add_art_page.html")


@app.route('/add_art', methods=["POST"])
def add_art_db():
    """add artwork to database"""
    artist = request.form.get('artist')
    title = request.form.get('title')
    medium = request.form.get('medium')
    substrate = request.form.get('substrate')
    genre = request.form.get('genre')
    year = request.form.get('year')
    height = request.form.get('height')
    length = request.form.get('length')
    depth = request.form.get('depth')
    url = request.form.get('url')

    # add artwork to db
    artwork = Artwork(artist_id=1, title=title, medium=medium, 
        substrate=substrate, genre=genre, height=height, length=length,
        depth=depth, year_created=year, url=url)

     # add artwork to database
    db.session.add(artwork)
    db.session.commit()

    return render_template("welcome.html")


@app.route('/register')
def register_form():
    """Registration page"""
    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Registration page"""

    login = request.form.get('login')
    password = request.form.get('pwd')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    add_line1 = request.form.get('add_line1')
    add_line2 = request.form.get('add_line2')
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip_code')
    country = request.form.get('country')
    user_type = request.form.get('user_type')
    twitter_handle = request.form.get('twitter_handle')

    # check to see if login exists in name exists in db
    login_user = AppUser.query.filter_by(login=login).first()

    if not login_user: 
        # add user to db
        user = User(first_name=first_name, last_name=last_name, email=email, 
            phone=phone, login=login)
        # set user address
        user.address = Address(address_line1=add_line1, address_line2=add_line2, city=city, state=state, 
            zip_code=zip_code, country=country)
        # add user login data to app_user
        user.app_user = AppUser(login=login, password=password)
        
        # write new user / app_user to database
        db.session.add(user)
        db.session.commit()
        # put user's email in flask session
        session['email'] = email


        if user_type == 'artist':
            return render_template("artist_info.html", user_id=user.user_id)
        if user_type == 'patron':
            return render_template("patron_info.html", user_id=user.user_id)
        if user_type == 'fan':
            return render_template("fan_info.html", user_id=user.user_id)

        flash('You were successfully registered %s.' % session['email'])
        return redirect("/")
    else:   # login exists in database.
        flash('login: %s already exists please pick another.' % login)
        return redirect('/register')


@app.route('/artistInfo', methods=["POST"])
def register_artist():
    """Artist Registration page"""
    bio = request.form.get('bio')
    statement = request.form.get('statement')
    website = request.form.get('website')
    user_id = request.form.get('user_id')
    artist = Artist(user_id=user_id, bio=bio, statement=statement, website=website)
    db.session.add(artist)

    db.session.commit()
    return redirect("/")



@app.route('/patronInfo', methods=["POST"])
def register_patron():
    """Patron Registration page"""
    patron_info = request.form.get('patron_info')
    user_id = request.form.get('user_id')
    patron = Patron(user_id=user_id, patron_info=patron_info)
    db.session.add(patron)

    db.session.commit()
    return redirect("/")


@app.route('/fanInfo', methods=["POST"])
def register_fan():
    """Fan Registration page"""
    fan_info = request.form.get('fan_info')
    user_id = request.form.get('user_id')
    fan = ArtFan(user_id=user_id, fan_info=fan_info)
    db.session.add(fan)

    db.session.commit()
    return redirect("/")


@app.route('/logout')
def logout():
    """Logout clears session"""

    session.clear()

    return redirect("/")


# @app.route("/users")
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


# @app.route("/user_profile")
# def user_profile():
#     """Show user profile."""

#     return render_template("user_profile.html")




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
