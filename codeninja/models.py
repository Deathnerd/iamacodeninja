from .app import db
from flask.ext.login import UserMixin
from codeninja.extensions import bcrypt
from .database import CRUDMixin, SurrogatePK


class User(db.Model, UserMixin, CRUDMixin, SurrogatePK):
	__tablename__ = "user"

	username = db.Column(db.String(128), nullable=False, unique=True)
	password = db.Column(db.String(256), nullable=True)
	email = db.Column(db.String(50), nullable=False)
	admin = db.Column(db.Boolean, default=False)
	active = db.Column(db.Boolean, default=True)
	gender = db.Column(db.Enum("Male", "Female"), nullable=False, default="Male")
	first_name = db.Column(db.String(60), nullable=False, default="Foo")
	middle_name = db.Column(db.String(60), nullable=True, default="B.")
	last_name = db.Column(db.String(60), nullable=False, default="Baz")
	# birthday = db.Column(db.DateTime, nullable=False)
	nickname = db.Column(db.String(60), nullable=True)  # Different from username. Like "B.A." Barakus
	# activate_token = db.Column(db.String(256), nullable=True)
	profile = db.relationship('Profile', uselist=False, backref=db.backref("user", uselist=False))

	def __init__(self, username, email, password=None, **kwargs):
		db.Model.__init__(self, username=username, email=email, **kwargs)
		if password:
			self.set_password(password)
		else:
			self.password = None

	def __repr__(self):
		return "{name}".format(name=self.username)

	def set_password(self, password):
		"""Sets the password using bcrypt"""
		self.password = bcrypt.generate_password_hash(password)

	def check_password(self, value):
		"""Checks the password"""
		return bcrypt.check_password_hash(self.password, value)

	def is_admin(self):
		"""Is the user an administrator?"""
		return self.admin

	def is_active(self):
		"""Is this user account active?"""
		return self.active

	def get_id(self):
		"""Convenience Method to get the current user's id"""
		return self.id


class Profile(db.Model, CRUDMixin, SurrogatePK):
	__tablename__ = "profile"

	about_me = db.Column(db.Text, nullable=True, default="Coming soon!")
	motto = db.Column(db.String(255), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	picture = db.Column(db.String(256), nullable=True)	 # SHA256 hash of the user's name + current timestamp
	template_id = db.Column(db.Integer, db.ForeignKey('template.id'))

	def __init__(self, user_id, template_id, *args, **kwargs):
		db.Model.__init__(self, user_id=user_id, template_id=template_id, *args, **kwargs)

	def __repr__(self):
		return "Profile for User: {user_id}".format(user_id=self.user_id)


class Template(db.Model, CRUDMixin, SurrogatePK):
	__tablename__ = "template"

	filename = db.Column(db.String(50), nullable=False, unique=True)
	active = db.Column(db.Boolean, default=True)
	profiles = db.relationship('Profile', backref='template', lazy='dynamic')

	def __init__(self, template_name, *args, **kwargs):
		db.Model.__init__(self, filename=template_name, *args, **kwargs)

	def __repr__(self):
		return "Profile Template: {filename}".format(filename=self.filename)