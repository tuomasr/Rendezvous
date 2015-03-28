# Django
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

# Project
from linkedin_integration.forms import ReviewProfileForm
from users.models import UserProfile
from skills.models import Skill
from skills.views import update_skills, add_skills_for, create_preferences
from cities_light.models import City, Country

# A form for creating new users.
class UserProfileCreationForm(UserCreationForm):
	firstname = forms.CharField()
	lastname = forms.CharField()
	email = forms.EmailField()
	description = forms.CharField(widget=forms.Textarea)
	skills = forms.CharField(widget=forms.Textarea)
	country = forms.CharField()
	city = forms.CharField()

	# Preferences
	engineering = forms.IntegerField(min_value=0, max_value=100)
	design = forms.IntegerField(min_value=0, max_value=100)
	business = forms.IntegerField(min_value=0, max_value=100)
	communication = forms.IntegerField(min_value=0, max_value=100)

	# This must be hacked because the default form does not support custom User model. ;ASD
	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			self._meta.model._default_manager.get(username=username)
		except self._meta.model.DoesNotExist:
			return username
		raise forms.ValidationError(self.error_messages['duplicate_username'])

	class Meta:
		model = UserProfile
		exclude = ('skills', 'country', 'city', 'password', 'last_login', 'date_joined')

	def get_skills(self):
		data = self.cleaned_data
		return data['skills']
	
	def save(self):
		data = self.cleaned_data
		print data

		try:
			user = UserProfile.objects.create_user(username=data['username'], firstname=data['firstname'], lastname=data['lastname'], fullname=data['firstname'] + ' ' + data['lastname'], email=data['email'], description=data['description'], password=data['password1'], country=data['country'], city=data['city'])
			
			if user.city:
				try:
					user.region = City.objects.get(name=user.city).region.name
				except:
					user.region = None

			create_preferences(user)
			user.preferences.engineering = data['engineering']
			user.preferences.design = data['design']
			user.preferences.business = data['business']
			user.preferences.communication = data['communication']
			user.preferences.save()
			add_skills_for(user, self.get_skills())
		except:
			raise forms.ValidationError('Ebig error')
				
		return user
		
class UpdateProfileForm(ReviewProfileForm):	
	# Override this method

	def save(self, user):
		data = self.cleaned_data
		
		user.username = data['username']
		user.firstname = data['firstname']
		user.lastname = data['lastname']
		user.fullname = user.firstname + ' ' + user.lastname
		user.email = data['email']
		user.description = data['description']
		user.country = data['country']
		user.city = data['city']
		user.preferences.engineering = data['engineering']
		user.preferences.design = data['design']
		user.preferences.business = data['business']
		user.preferences.communication = data['communication']
		user.preferences.save()

		update_skills(user, data['skills'])
		
		user.save()
		
		return user