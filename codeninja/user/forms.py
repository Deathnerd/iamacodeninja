from flask_wtf import Form
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from ..models import Template


class AccountManagementForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
	active = BooleanField('Account Active')
	nickname = StringField('Nickname')
	first_name = StringField('First Name')
	middle_name = StringField('Middle Name')
	last_name = StringField('Last Name')
	gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')])
	templates = SelectField('Profile template', validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		self.templates.kwargs['choices'] = [(template.filename, template.filename) for template in Template.query.all()]
		super(AccountManagementForm, self).__init__(*args, **kwargs)
		self.user = None

	def validate(self):
		"""
		Validates that the user has all the information needed in their account page
		:return:
		"""
		return super(AccountManagementForm, self).validate()