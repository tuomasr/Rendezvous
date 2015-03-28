# Django
from __future__ import division
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Skill(models.Model):
	name = models.CharField(max_length=50, unique=True)
	#expertise = models.PositiveIntegerField() 	# the level of the skill
	#preference = models.PositiveIntegerField()	# let user define his/her interests
	
	def __unicode__(self):
		return self.name
	
class Preferences(models.Model):
	business		= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
	communication	= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
	design			= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
	engineering		= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

	def ratios(self):
		tot = self.engineering + self.business + self.design + self.communication

		return [100*self.business/tot, 100*self.communication/tot, 100*self.design/tot, 100*self.engineering/tot]

	def to_degrees(self):
		tot = self.engineering + self.business + self.design + self.communication

		return [360*self.business/tot, 360*self.communication/tot, 360*self.design/tot, 360*self.engineering/tot]