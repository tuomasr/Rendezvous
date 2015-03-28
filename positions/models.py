# Django
from django.db import models

# Project
from skills.models import Skill
from schemes.models import Scheme
from users.models import UserProfile

class PositionManager(models.Manager):
	# Return open positions in a scheme
	def open_positions(self, scheme):
		return self.get_query_set().filter(scheme=scheme, vacant=True)

	def filled_positions(self):
		return self.get_query_set().filter(vacant=False)

	# All the positions that a user holds
	def positions_for_user(self, user):
		return self.get_query_set().filter(holder=user.pk)

class Position(models.Model):
	name = models.CharField(max_length=50, blank=False)
	scheme = models.ForeignKey(Scheme, related_name='positions')	# A position has only one scheme but the scheme can have multiple positions
	skills = models.ManyToManyField(Skill, related_name='position', blank=True, null=True)
	vacant = models.BooleanField(default=True)
	holder = models.ForeignKey(UserProfile, blank=True, null=True) # A position has only one owner but the user can have multiple positions
	admin = models.BooleanField(default=False)
	member = models.BooleanField(default=True)

	objects = PositionManager()

	def __unicode__(self):
		return unicode(self.name)

	def mark_filled(self):
		self.vacant = False
		self.save()