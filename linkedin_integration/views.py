# Django
from django.contrib.messages.api import get_messages
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

# Project
from skills.views import add_skills_for, create_preferences
from skills.models import Skill
from users.models import UserProfile
from linkedin_integration.forms import ReviewProfileForm

# GeoIP
import pygeoip

# Geolocation
from cities_light.models import City, Country

# Settings
from django.conf import settings

# A profile has been already created
def login_success(request):
	return HttpResponseRedirect('/')

# Handles first time logins
def login_new(request):
	user = request.user
	details = user.social_auth.get().extra_data

	print details

	if request.method == 'POST':
		form = ReviewProfileForm(request.POST)
		
		if form.is_valid() and user is not None:
			form.save()
			
			user.username = form.username
			user.firstname = form.firstname
			user.lastname = form.lastname
			user.fullname = user.firstname + ' ' + user.lastname
			user.description = form.description
			user.country = form.country
			if form.city:
				user.city = form.city
				try:
					user.region = City.objects.get(name=user.city).region.name
				except:
					user.region = None
			
			user.linkedin_id = details['id']
			user.linkedin_public_profile_url = details['public_profile_url']	# this is not shown to the user
			get_connections(details['connections'], user)

			# Add default preferences
			create_preferences(user)

			user.preferences.engineering = form.engineering
			user.preferences.design = form.design
			user.preferences.business = form.business
			user.preferences.communication = form.communication
			user.preferences.save()
			user.save()

			# test
			u = UserProfile.objects.user_by_linkedin_id(user.linkedin_id)
			print u.all()
			user.linkedin_connections.add(u.all()[0])
			user.save()
			
			# Save user's skills
			add_skills_for(user, form.skills)
			
			return HttpResponseRedirect('/')
	else:
		username = user.username
		email = user.email
		firstname = details['first_name']
		lastname = details['last_name']
		description = details['summary']	# description is linkedin summary
		skill_list = get_skills_from_request(request)
		skill_str = ', '.join(skill_list)
		country = details['location']['name']

		try:
			ip = request.META.get('REMOTE_ADDR')

			#if x_forwarded_for:
			#	ip = x_forwarded_for.split(',')[-1].strip()
			#else:
			#	ip = request.META.get('REMOTE_ADDR')

			gic = pygeoip.GeoIP(settings.PROJECT_PATH + settings.STATIC_URL + 'GeoLiteCity.dat')
			city = gic.record_by_addr('82.130.35.22')['city']
		except:
			city = ''

		
		form = ReviewProfileForm(initial={'username':username, 'firstname':firstname, 'lastname':lastname, 'email':email, 'description':description, 'skills':skill_str, 'country':country, 'city':city})
		
	return render_to_response('linkedin_integration/review_profile.html', RequestContext(request, {'form':form}))
	
def error(request):
	messages = get_messages(request)
	return render_to_response('404.html', RequestContext(request, {}))

def get_connections(connections, user):
	for i in range(1, len(connections['person'])):
		u = UserProfile.objects.user_by_linkedin_id(connections['person'][i]['id'])
		if u.count() == 1:
			user.linkedin_connections.add(u.all()[0])
	
# Use social auth to get skills from LinkedIn profile	
def get_skills_from_request(request):
	details = request.user.social_auth.get().extra_data
	skills = details['skills']
	skill_list = []
	
	for i in range(len(skills.values()[0])-1):
		skill_list.append(skills.values()[0][i].values()[0]['name'])
	
	return skill_list
