"""Movie Ratings."""

from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session, url_for
from model import User, AppUser, Address, connect_to_db, db


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
    # a = jsonify([1,3])
    # return a
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/user_profile")
def user_profile():
    """Show user profile."""

    # email = session['email']
    # user = User.query.filter_by(email=email).first()
    # user_ratings = Rating.query.filter_by(userid = user.user_id).all()
    # user_movies = Movie.query.filter_by(user_ratings.movie_id).all()
    # return render_template("user_profile.html", user=user, movies=user_ratings)
    return render_template("user_profile.html")


@app.route('/login')
def login():
    """Login page shows login form"""

    return render_template("login_form.html")


@app.route('/login', methods=["POST"])
def login_form():
    """Handle submission of login form"""

    email = request.form.get('email')
    password = request.form.get('pwd')

    # login page gets email and pwd, then redirects to home page?
        # if user doesnt exist, go to /register route, and add them to the db?

    # check to see if user exists
    user_rec = User.query.filter_by(email=email).first()

    # print user_rec
    # TODO: check to see if submitted password matches user_rec.pass in db

    if not user_rec:
        # call other post and add to db?
        # if pwd doessnt match, reload form with alert try again
        return render_template("register_form.html")
        # return render_template("register_form.html", email=email,password=password )
        # print(url_for('register_form', email = email, password = password))
        # return redirect(url_for('register_form', email = email))
    else:
        if user_rec.password != password:
            flash('your login is incorrect')
            return redirect('/login')
        else:
            # TODO: add username and email to flask session to set alert
            session['email'] = email
            flash('You were successfully logged in %s' % session['email'])
            return redirect("/")


@app.route('/register')
def register_form():
    """Registration page"""
    # email = request.args.get('email')
    # password = request.args.get('password')
    # print(email)
    # print(password)
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

 
    # if user does not exist, add to db
    app_user = AppUser(login=login, password=password)
    address = Address(addresss_line1=add_line1, addresss_line2=add_line2, city=city, state=state, 
        zip_code=zip_code, country=country)

    db.session.add(address)
    db.session.add(app_user)

    db.session.commit()
    # user.address_id = address
    user = User(first_name=first_name, last_name=last_name, email=email, 
        phone=phone, login=login, address_id=address.address_id)
    db.session.add(user)
    db.session.commit()
    session['email'] = email
    flash('You were successfully registered %s.' % session['email'])
    return redirect("/")


@app.route('/logout')
def logout():
    """Logout clears session"""

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
