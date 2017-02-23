import unittest
from unittest import TestCase
from server import app
from model import User, AppUser, Address, Artist, Patron, ArtFan, Artwork, connect_to_test_db, db
from flask_sqlalchemy import SQLAlchemy


# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)
# db = SQLAlchemy()

class FlaskTest(TestCase):
	""" test harness to test ArtAnnounce"""

	
	def example_data(self):
		"""Create sample data"""
		# populate users table
		uk = User(first_name='Kushlani', last_name='Jayasinha', email='kushi@att.net',
				address_id=1)
		uk.app_user = AppUser(login='kushij', password='1234')
		
		uk.address = Address(address_line1='myhome')
		uc = User(first_name='Chris', last_name='Lane', email='chris@lane-jayasinha.com',
				address_id=2)
		uc.app_user = AppUser(login='chrisl', password='1234')
		uc.address = Address(address_line1='myhome')

		uv = User(first_name='Vidharshi', last_name='Dharmasens', email='V@gmail.com',
				address_id=3)
		uv.app_user = AppUser(login='v', password='1234')
		uv.address = Address(address_line1='myhome')

		ua = User(first_name='Alex', last_name='Hall', email='alex@gmail.com',
				address_id=4)
		ua.app_user = AppUser(login='alexh', password='1234')
		ua.address = Address(address_line1='myhome')



		# populate artists table
		a1 = Artist(bio='I am an artist.', statement='I love art!', website='http://KushlaniFineArt.com')

		# populate patrons table
		p1 = Patron(patron_info='I love Chris....')

		# populate fans table
		f1 = ArtFan(fan_info='I love Alex.')

		# populate artworks table
		aw1 = Artwork(title='Mendocino', year_created='2015', medium='oil', substrate='canvas',
			genre='abstracts',length='40"', height='30"', depth='1.5"', url='https://fasoimages-4cde.kxcdn.com/25287_1438386l+v=201609181617c201609181617error/mendocino.jpg')
		aw2 = Artwork(title='Autumn', year_created='2015', medium='oil', substrate='canvas',
			genre='abstracts',length='8"', height='8"', depth='1.5"', url='https://fasoimages-4cde.kxcdn.com/25287_1322110l+v=201609181617c201609181617error/autumn.jpg')

		#db.session.add_all([uk, uk.app_user, uk.address, uc, uc.app_user, uc.address, ua, ua.app_user, ua.address, uv, uv.app_user, uv.address, a1, p1, f1, aw1, aw2])
		db.session.add_all([uk, uc, ua, uv, a1, p1, f1, aw1, aw2])
		db.session.commit()



	def setUp(self):
		"""Stuff to do before every test"""

		self.client = app.test_client()
		app.config['TESTING'] = True

		db.create_all()
		self.example_data()
        

	def tearDown(self):
		"""do at end of every test"""
		
		db.drop_all()
		db.session.close()
		
		#db.drop_all()

	
	
	def test_homepage_route(self):
		"""Test homepage"""

		result = self.client.get("/")
		self.assertEqual(result.status_code, 200)	# if working code should be 200
		self.assertIn('login', result.data)
		self.assertIn('registered', result.data)
	
	def test_login_get(self):
		"""Test if gets to login page"""

		result = self.client.get("/login")
		self.assertIn('login', result.data)	# if working code should be 200

	
	def test_login_correct(self):
		"""Test if login correct if so shows Welcome page"""

		result = self.client.post("/login", data={'login':'kushij', 'pwd':'1234'},
			follow_redirects=True)
		self.assertIn('Welcome to ArtAnnounce', result.data)	


	def test_login_wrong(self):
		"""Test if it goes to registration page user doesn't exist"""

		result = self.client.post("/login", data={'login':'wrong_user', 'pwd':'1234'},
			follow_redirects=True)
		self.assertIn('Zip code:', result.data)	


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
 #   from FlaskTest import example_data

    connect_to_test_db(app)
    print "Connected to DB."

    


    unittest.main()

    


    