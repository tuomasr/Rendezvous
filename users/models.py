# Django
from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.utils import timezone

# Project
from skills.models import Skill, Preferences

# Geodata
from cities_light.models import City, Country

class UserProfileManager(UserManager):
	def user_by_linkedin_id(self, linkedin_id):
		return self.get_query_set().filter(linkedin_id=linkedin_id)

class UserProfile(AbstractUser):
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	fullname = models.CharField(max_length=511, blank=True) #2*255+1 (space)
	description = models.TextField(blank=True)							# description of the user, his/her interests etc.
	skills = models.ManyToManyField(Skill, blank=True, null=True, related_name="user")		# each user has one set of skills but the same skillset can be applied to multiple users
	preferences = models.ForeignKey(Preferences, blank=True, null=True)
	linkedin_id = models.CharField(max_length=255, blank=True)
	linkedin_public_profile_url = models.CharField(max_length=500, blank=True)
	linkedin_connections = models.ManyToManyField('self', blank=True, null=True)
	country = models.CharField(max_length=255, blank=True, null=True)
	city = models.CharField(max_length=255, blank=True, null=True)
	region = models.CharField(max_length=255, blank=True, null=True)

	# see https://github.com/django/django/blob/master/django/contrib/auth/models.py for AbstractUser fields
	
	objects = UserProfileManager()
	
	def __unicode__(self):
		return unicode(self.username)

	def get_profile_urls(self):
		linkedin_url = ''

		if self.linkedin_public_profile_url:
			linkedin_url = "<a href=\'" + self.linkedin_public_profile_url + "\'>LinkedIn Profile</a><br>"

		rendezvous_url = "<a href=\'/users/" + self.username + "/\'>Public Profile</a>"

		return linkedin_url + rendezvous_url