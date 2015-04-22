from .app import db
from sqlalchemy.orm import relationship


class CRUDMixin(object):
	"""Mixin to provide methods for CRUD operations. Not necessary, but really convenient"""

	@classmethod
	def create(cls, **kwargs):
		"""Create a new record and save it"""
		instance = cls(**kwargs)
		return instance.save()

	def update(self, commit=True, **kwargs):
		"""Update specific fields for a record"""
		for attr, value in kwargs.iteritems():
			setattr(self, attr, value)
		return commit and self.save() or self

	def save(self, commit=True):
		"""Save the record"""
		db.session.add(self)
		if commit:
			db.session.commit()
		return self

	def delete(self, commit=True):
		"""Remove the record from the database"""
		db.session.delete(self)
		return commit and db.session.commit()


class SurrogatePK(object):
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True)

	@classmethod
	def get_by_id(cls, id):
		if any(
				(isinstance(id, basestring) and id.isdigit(),
				 isinstance(id, (int, float)))
		):
			return cls.query.get(int(id))
		return None