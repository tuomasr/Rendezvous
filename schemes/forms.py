# Django
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

# Project
from users.models import UserProfile
from schemes.models import Scheme
from skills.models import Skill
from skills.views import add_skills_for
from positions.models import Position
from messaging.models import Invitation

# Geolocation
from cities_light.models import City, Country

class SchemeBasicForm(forms.ModelForm):
	# A form for storing the basic values of the Scheme
	admin_position = forms.CharField(max_length=50)
	location = forms.CharField(required=False, max_length=255)
	url = forms.URLField(required=False)
	progress = forms.IntegerField(min_value=0, max_value=100)
	file = forms.FileField(required=False)

	class Meta:
		model = Scheme
		fields = ('name', 'description')
		widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

	
	def save(self, user):
		data = self.cleaned_data
		new_scheme = Scheme(name = data['name'], description = data['description'], progress = data['progress'])
		new_scheme.save()

		if 'location' in data:
			new_scheme.location = data['location']

			if Country.objects.filter(name=new_scheme.location).count() == 1:
				new_scheme.country = new_scheme.location
			elif City.objects.filter(name=new_scheme.location).count() == 1:
				new_scheme.city = new_scheme.location
				new_scheme.country = City.objects.get(name=new_scheme.location).country.name
				new_scheme.region = City.objects.get(name=new_scheme.location).region.name

		if 'url' in data:
			new_scheme.url = data['url']

		admin_position = Position(name=data['admin_position'], scheme=new_scheme, vacant=False, holder=user, admin=True)
		admin_position.save()
		admin_position.skills = user.skills.all()
		admin_position.save()
		new_scheme.save()
		return new_scheme

	def update(self, user, scheme):
		data = self.cleaned_data
		scheme.name = data['name']
		scheme.description = data['description']

		if 'location' in data:
			new_scheme.location = data['location']

			if Country.objects.filter(name=new_scheme.location).count() == 1:
				new_scheme.country = new_scheme.location
			elif City.objects.filter(name=new_scheme.location).count() == 1:
				new_scheme.city = new_scheme.location
				new_scheme.country = City.objects.get(name=new_scheme.location).country.name
				new_scheme.region = City.objects.get(name=new_scheme.location).region.name

		if 'url' in data:
			scheme.url = data['url']
		
		scheme.progress = data['progress']

		admin_position = Position.objects.get(scheme=scheme, holder=user)
		admin_position.name = data['admin_position']
		admin_position.save()
		Position.objects.open_positions(scheme).delete()
		scheme.update_date()
		scheme.save()

		return scheme
		
class SchemePositionForm(forms.Form):
	error_messages = {'both':'Both fields are missing!'}

	# A form for storing available position data
	position = forms.CharField(max_length=50, error_messages={'required': 'Please enter a name for the position.'})
	skills = forms.CharField(widget=forms.Textarea, error_messages={'required': 'Please enter skills for the position.'})
	invited = forms.CharField(max_length=50, required=False)

	def clean(self):
		data = super(SchemePositionForm, self).clean()
		position = data.get('position')
		skills = data.get('skills')
		invited = data.get('invited')

		if not position and not skills:
			msg = 'Both fields (position and skills) are missing!'
			self._errors['position'] = self.error_class([msg])
			return False
		elif invited:
			if UserProfile.objects.filter(username=invited).count() == 0:
				msg = 'The user does not exist!'
				self._errors['invited'] = self.error_class([msg])
				return False
		return data
	
	def save(self, scheme, user):
		data = self.cleaned_data
		
		new_position = Position(name=data['position'], scheme=scheme)
		new_position.save()
		add_skills_for(new_position, data['skills'])
		scheme.save()

		if 'invited' in data:
			if UserProfile.objects.filter(username=data['invited']).count() == 1:

				new_invitation = Invitation(sender=user, recipient=UserProfile.objects.get(username=data['invited']), scheme=scheme, headline='Invitation to ' + scheme.name, position=new_position, contents=user.fullname + ' invites you to ' + scheme.name)
				new_invitation.save()
