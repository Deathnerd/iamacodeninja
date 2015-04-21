from .app import db
from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
	__tablename__ = "user"

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	admin = db.Column(db.Boolean, default=False)
	active = db.Column(db.Boolean, default=True)
	gender = db.Column(db.Enum("Male", "Female"), nullable=False)
	first_name = db.Column(db.String(60), nullable=False, default="Foo")
	middle_name = db.Column(db.String(60), nullable=True, default="B.")
	last_name = db.Column(db.String(60), nullable=False, default="Baz")
	birthday = db.Column(db.DateTime, nullable=False)
	email = db.Column(db.String(50), nullable=False)
	nickname = db.Column(db.String(60), nullable=True)  # Different from username. Like "B.A." Barakus
	username = db.Column(db.String(128), nullable=False, unique=True)
	password = db.Column(db.String(256), nullable=False)
	activate_token = db.Column(db.String(256), nullable=True)
	profile = db.relationship('Profile', uselist=False, backref=db.backref("user", uselist=False))

	def __init__(self, **kwargs):
		for key in kwargs:  # dynamic property setter to play nice with SuperAdmin
			if key == "password":  # if there's a password being sent to us
				self.set_password(kwargs.get(key))
			else:
				setattr(self, key, kwargs.get(key))

	def __repr__(self):
		return "{name}".format(name=self.username)

	# def set_password(self, password):
	# 	"""Sets the password using bcrypt"""
	# 	self.password = bcrypt.generate_password_hash(password)
	#
	# def check_password(self, value):
	# 	"""Checks the password"""
	# 	return bcrypt.check_password_hash(self.password, value)

	def is_admin(self):
		"""Is the user an administrator?"""
		return self.admin

	def is_active(self):
		"""Is this user account active?"""
		return self.active

	def get_id(self):
		"""Convenience Method to get the current user's id"""
		return self.id


class Profile(db.Model):
	__tablename__ = "Profile"

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	about_me = db.Column(db.Text, nullable=True, default="Coming soon!")
	motto = db.Column(db.String(255), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	picture = db.Column(db.String(256), nullable=True)	 # SHA256 hash of the user's name + current timestamp

	def __init__(self, **kwargs):
		for key in kwargs:  # dynamic property setter to play nice with SuperAdmin
			setattr(self, key, kwargs.get(key))

	def __repr__(self):
		return "Profile for User: {user_id}".format(user_id=self.user_id)