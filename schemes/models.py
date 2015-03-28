# Python
import datetime

# Django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Project
from users.models import UserProfile

class Scheme(models.Model):
	# Scheme details
	name			= models.CharField(max_length=50, blank=False, unique=True)
	description 	= models.TextField(blank=False)
	location 		= models.CharField(max_length=255, blank=True, null=True)
	country			= models.CharField(max_length=255, blank=True, null=True)
	city   			= models.CharField(max_length=255, blank=True, null=True)
	region   		= models.CharField(max_length=255, blank=True, null=True)
	url 			= models.URLField(blank=True, null=True)
	progress		= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
	
	# Automatic fields for creation and update dates
	pub_date 		= models.DateTimeField('date published', auto_now_add=True)
	updated			= models.DateTimeField('date modified', blank=True, null=True)
	
	# Relation to users
	admins			= models.ManyToManyField(UserProfile, blank=False, related_name="admin_in_schemes")	# avoid clashes by using related_name
	members			= models.ManyToManyField(UserProfile, blank=True, related_name="member_in_schemes")

	#From positions:
	# scheme = models.ForeignKey(Scheme, related_name='positions')

	# what to return when the object is called
	def __unicode__(self):
		return unicode(self.name)

	def get_absolute_url(self):
		return "/schemes/%i/" % self.id

	def update_date(self):
		self.updated = datetime.datetime.now() 
		self.save()
