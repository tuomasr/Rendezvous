# Django
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.db.models import Count

# JSON
import simplejson

# Project
from skills.models import Skill
from users.models import UserProfile
from positions.models import Position
from messaging.models import Message, Application, Invitation
from schemes.models import Scheme
from forms import SearchForm, SchemeSearchForm, UserSearchForm
from skills.views import get_skills

# Geolocation
from cities_light.models import City, Country, Region

def home(request):
	user = request.user

	if not user.is_authenticated() and request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		form = AuthenticationForm(data=request.POST)

		user = authenticate(username=username, password=password)
		
		if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/')
				else:
					return HttpResponse('user.is_active failed')
		else:
			return render_to_response('registration/login.html', RequestContext(request, {'form': form}))

	elif user.is_authenticated():
		if request.method == 'GET':
			form = SearchForm()
			scheme_form = SchemeSearchForm()
			user_form = UserSearchForm()
			new_messages_count = Message.objects.inbox(user).count()
			new_applications_count = Application.objects.filter(recipient=user, read=False).count()
			new_invitations_count = Invitation.objects.filter(recipient=user, read=False).count()
			return render_to_response('rendezvous/home_logged_in.html', RequestContext(request, {'new_messages':new_messages_count, 'new_applications':new_applications_count, 'new_invitations':new_invitations_count, 'form':form, 'scheme_form':scheme_form, 'user_form':user_form}))
	else:
		form = AuthenticationForm(request)
		return render_to_response('rendezvous/home.html', RequestContext(request, {'form': form}))

def about(request):
	return render_to_response('rendezvous/about.html', RequestContext(request, {}))

def scheme_search(request):
	data = {'html':''}

	if request.method == 'GET' and request.is_ajax():

		form = SchemeSearchForm(request.GET)

		if form.is_valid():
			form.save()

			results = []

			if form.choice == 'name':
				results = Position.objects.filter(scheme__name__icontains=form.search)

			elif form.choice == 'skill':
				skill_list = [name.lower().strip(' ') for name in form.search.split(',') if not name.isspace()]
				results = Position.objects.filter(skills__name__in=skill_list).annotate(skills_count=Count('skills')).filter(skills_count=len(skill_list)).filter(vacant=True)

			elif form.choice == 'position':
				results = Position.objects.filter(name__icontains=form.search, vacant=True)

			if form.location or form.location_default:
				if form.location:

					if Country.objects.filter(name=form.location).count() == 1:
						results = results.filter(scheme__location=form.location) | results.filter(scheme__country=form.location)
					elif City.objects.filter(name=form.location).count() == 1:
						results = results.filter(scheme__location=form.location) | results.filter(scheme__city=form.location)
					elif Region.objects.filter(name=form.location).count() == 1:
						results = results.filter(scheme__location=form.location) | results.filter(scheme__region=form.location)
					else:
						results = []
				else:
					results = results.filter(scheme__country=request.user.country)

			data['html'] = render_to_string('rendezvous/scheme_search_results.html', {'results':results})


	json = simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')

def user_search(request):
	data = {'html':''}

	if request.method == 'GET' and request.is_ajax():

		form = UserSearchForm(request.GET)

		if form.is_valid():
			form.save()

			results = []

			if form.choice == 'name':
				term = form.search
				results = UserProfile.objects.filter(fullname__icontains=term)

			elif form.choice == 'skill':
				skill_list = [name.lower().strip(' ') for name in form.search.split(',') if not name.isspace()]
				results = UserProfile.objects.filter(skills__name__in=skill_list).annotate(skills_count=Count('skills')).filter(skills_count=len(skill_list))
				
			if form.location or form.location_default:
				if form.location:

					if Country.objects.filter(name=form.location).count() == 1:
						results = results.filter(country=form.location)
					elif City.objects.filter(name=form.location).count() == 1:
						results = results.filter(city=form.location)
					elif Region.objects.filter(name=form.location).count() == 1:
						results = results.filter(region=form.location)
					else:
						results = []
				else:
					results = results.filter(region=request.user.region)
				
			data['html'] = render_to_string('rendezvous/user_search_results.html', {'results':results})

	json = simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')

def test(request):
	return render_to_response('test.html', RequestContext(request, {}))



		
