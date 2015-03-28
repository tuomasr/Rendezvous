# Django
from django import forms

# Project
from skills.models import Skill

class SearchForm(forms.Form):
	choices = (('skill', 'skill'), ('position', 'position'), ('location','location'), ('scheme', 'scheme'))

	choice = forms.ChoiceField(choices)
	search = forms.CharField()

class SchemeSearchForm(forms.Form):
	choices = (('name', 'name'), ('skill', 'skill'), ('position', 'position'))

	choice = forms.ChoiceField(choices)
	search = forms.CharField()
	location = forms.CharField(required=False)
	location_default = forms.BooleanField(required=False)

	def save(self):
		data = self.cleaned_data
		self.search = data['search']
		self.choice = data['choice']
		self.location = data['location']
		self.location_default = data['location_default']

class UserSearchForm(forms.Form):
	choices = (('name', 'name'), ('skill', 'skill'))

	choice = forms.ChoiceField(choices)
	search = forms.CharField()
	location = forms.CharField(required=False)
	location_default = forms.BooleanField(required=False)

	def save(self):
		data = self.cleaned_data
		self.search = data['search']
		self.choice = data['choice']
		self.location = data['location']
		self.location_default = data['location_default']