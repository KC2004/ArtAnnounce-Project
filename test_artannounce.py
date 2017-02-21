from unittest import TestCase
from server import app

class seUp(self):
	"""Stuff to do before every test"""

	self.client = app.test_client()
	app.config['TESTING'] = True

	# connect to test database
	connect_to_db(app, "postgresql:///testdb")

	# Create tables and add sample data
	db.create_all()
	example_data()


def tear_down(self):
	"""do at end of every test"""

	db.session.close()
	db.drop_all()


def example_data():
	"""Create sample data"""
	# populate users table
	uk = User(first_name='Kushlani', last_name='Jayasinha', email='kushi@att.net',
			address_id=1, login='kushij')
	uc = User(first_name='Chris', last_name='Lane', email='chris@lane-jayasinha.com',
			address_id=2, login='chrisl')
	uv = User(first_name='Vidharshi', last_name='Dharmasens', email='V@gmail.com',
			address_id=3, login='v')
	ua = User(first_name='Alex', last_name='Hall', email='alex@gmail.com',
			address_id=4, login='alexh')


	# populate artists table
	a1 = Artist(bio='I am an artist.', statement='I love art!', website='http://KushlaniFineArt.com')

	# populate patrons table
	p1 = Patron(patron_info='I love Chris....')

	# populate app_users table
	au1 = AppUser(password='1234')

	# populate fans table
	f1 = ArtFan(='I love Alex.')

	# populate artworks table
	aw1 = Artwork(title='Mendocino', year_created='2015', medium='oil', substrate='canvas',
		genre='abstracts',length='40"', height='30"', depth='1.5"', url='https://fasoimages-4cde.kxcdn.com/25287_1438386l+v=201609181617c201609181617error/mendocino.jpg')
	aw2 = Artwork(title='Autumn', year_created='2015', medium='oil', substrate='canvas',
		genre='abstracts',length='8"', height='8"', depth='1.5"', url='https://fasoimages-4cde.kxcdn.com/25287_1322110l+v=201609181617c201609181617error/autumn.jpg')


def test_homepage_route(self):
	"""Test homepage"""

	result = self.client.get("/")
	self.assertEqual(result.status_code, 200)	# if working code should be 200
	self.assertIn('Login', result.data)


