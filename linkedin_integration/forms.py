# Django
from django import forms

# Project
from skills.models import Skill
	
class ReviewProfileForm(forms.Form):
	# A profile is created from Linkedin. Review details.
	
	username = forms.CharField(max_length=30)
	firstname = forms.CharField(max_length=255)
	lastname = forms.CharField(max_length=255)
	email = forms.EmailField()
	description = forms.CharField(widget=forms.Textarea)
	skills = forms.CharField(widget=forms.Textarea)
	country = forms.CharField(max_length=255)
	city = forms.CharField(required=False, max_length=255)

	# Preferences
	engineering = forms.IntegerField(min_value=0, max_value=100)
	design = forms.IntegerField(min_value=0, max_value=100)
	business = forms.IntegerField(min_value=0, max_value=100)
	communication = forms.IntegerField(min_value=0, max_value=100)
	
	def save(self):
		data = self.cleaned_data
		self.username = data['username']
		self.firstname = data['firstname']
		self.lastname = data['lastname']
		self.description = data['description']
		self.skills = data['skills']
		self.country = data['country']
		self.city = data['city']
		self.engineering = data['engineering']
		self.design = data['design']
		self.business = data['business']
		self.communication = data['communication']
		
	def get_skills(self):
		data = self.cleaned_data
		return data['skills']