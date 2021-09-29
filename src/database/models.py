import uuid

from werkzeug.security import generate_password_hash

from src import db

movies_actors = db.Table(
	'movies_actors',
	db.Column('actor_id', db.Integer, db.ForeignKey('actors.id', primary_key=True)),
	db.Column('film_id', db.Integer, db.ForeignKey('films.id', primary_key=True))
)


class Actor(db.Model):
	__tablename__ = 'actors'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	birthdate = db.Column(db.Date, index=True, nullable=False)
	is_active = db.Column(db.Boolean)
	uuid = db.Column(db.String(36), unique=True)
	
	def __init__(self, name, birthday, is_active):
		self.name = name
		self.birthdate = birthday
		self.is_active = is_active
		self.uuid = str(uuid.uuid4())
	
	def __repr__(self):
		return f'actor({self.id, self.name, self.birthdate, self.is_active})'


class Film(db.Model):
	__tablename__ = 'films'
	
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	release_date = db.Column(db.Date, index=True, nullable=False)
	uuid = db.Column(db.String(36), unique=True)
	description = db.Column(db.Text)
	distributed_by = db.Column(db.String(120), nullable=False)
	length = db.Column(db.Float)
	rating = db.Column(db.Float)
	actors = db.relationship('Actor', secondary=movies_actors, lazy=True, backref=db.backref('films', lazy=True))
	
	
	def __init__(self, title, release_date, description, distributed_by, length, rating, actors=None):
		self.title = title
		self.release_date = release_date
		self.description = description
		self.distributed_by = distributed_by
		self.length = length
		self.rating = rating
		self.uuid = str(uuid.uuid4())
		
		if not actors:
			self.actors = []
		else:
			self.actors = actors
	
	def __repr__(self):
		return f'film({self.title, self.uuid, self.distributed_by, self.release_date, self.rating, self.actors})'


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(120), nullable=False, unique=True)
	email = db.Column(db.String(120), nullable=False, unique=True)
	password = db.Column(db.String(120), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	uuid = db.Column(db.String(36), unique=True)
	
	def __init__(self, username, email, password, is_admin=False):
		self.username = username
		self.email = email
		self.password = generate_password_hash(password)
		self.is_admin = is_admin
		self.uuid = str(uuid.uuid4())
	
	def __repr__(self):
		return f'user({self.username, self.email, self.uuid})'
	
	@classmethod
	def find_user_by_username(cls, username):
		return cls.query.filter_by(username=username).first()
	
	@classmethod
	def find_user_by_uuid(cls, uuid):
		return cls.query.filter_by(uuid=uuid).first()
