# Generic
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string

# Signup and login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# JSON
import simplejson

# Project
from models import UserProfile
from forms import UserProfileCreationForm, UpdateProfileForm
from skills.views import skills_to_str, create_preferences

# Register the user
def register_view(request):
	if request.method == 'POST':
		form = UserProfileCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			return HttpResponseRedirect('/login/')
		else:
			return render_to_response('registration/register.html', RequestContext(request, {'form': form, 'display_mode':''}))
	else:
		form = UserProfileCreationForm()
		
	return render_to_response('registration/register.html', RequestContext(request, {'form': form, 'display_mode':'display:none;'}))

# A view for login
def login_view(request, next_page=None):
	print next_page

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		form = AuthenticationForm(data=request.POST)
		user = authenticate(username=username, password=password)
		
		if form.is_valid() and user is not None:
			if user.is_active:
				login(request, user)
				if next_page is None:
					return HttpResponseRedirect('/')
				else:
					return HttpResponseRedirect(next_page)
			else:
				return HttpResponse('user.is_active failed')
		else:
			return render_to_response('registration/login.html', RequestContext(request, {'form': form}))
	
	form = AuthenticationForm(request)
	
	return render_to_response('registration/login.html', RequestContext(request, {'form': form}))

# Logout
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

# Show profile
def profile_view_private(request):
	user = request.user
	pref_rat = user.preferences.to_degrees()

	return render_to_response('user/private_profile.html', RequestContext(request, {'pref_rat':pref_rat}))
	
def profile_view_public(request, userprofile_username):
	public_profile = UserProfile.objects.get(username=userprofile_username)
	return render_to_response('user/public_profile.html', RequestContext(request, {'public_profile': public_profile}))
	
# Modify profile
def update_profile(request):
	if request.method == 'POST':
		form = UpdateProfileForm(request.POST)
		user = request.user
		
		if form.is_valid() and user is not None:
			form.save(user)
			return HttpResponseRedirect('/')
	else:
		user = request.user
		username = user.username
		firstname = user.firstname
		lastname = user.lastname
		email = user.email
		description = user.description
		skill_str = skills_to_str(user)
		country = user.country
		city = user.city
		preferences = user.preferences

		form = UpdateProfileForm(initial={'username':username, 'firstname':firstname, 'lastname':lastname, 'email':email, 'description':description, 'skills':skill_str, 'country':country, 'city':city})
		
	return render_to_response('user/update_profile.html', RequestContext(request, {'form': form, 'preferences':preferences}))

def get_user(request):
	if request.is_ajax():
		term = request.GET.get('term','') #jquery-ui.autocomplete parameter
		users = request.user.linkedin_connections.filter(fullname__icontains=term) #lookup for a user (case-insensitive)
		res = []
		for c in users:
			#make dict with the metadatas that jquery-ui.autocomple needs (the documentation is your friend)
			dict = {'id':c.id, 'label':c.fullname, 'value':c.username}
			res.append(dict)
		
		data = simplejson.dumps(res)
	else:
		data = 'fail'
	
	return HttpResponse(data, 'application/json')

def list_all(request):
	user_list = UserProfile.objects.all()

	return render_to_response('user/user_list.html', RequestContext(request, {'user_list':user_list}))

def profile_view_ajax(request, userprofile_id):
	data = {'html': ''}

	if request.method == 'GET' and request.is_ajax():
		userprofile = get_object_or_404(UserProfile, pk=userprofile_id)
		pref_rat = userprofile.preferences.to_degrees()
		data['html'] = '<h3>Details for the user</h3>' + render_to_string('user/user_detail.html', RequestContext(request, {'userprofile': userprofile, 'pref_rat':pref_rat}))

		json = simplejson.dumps(data)
		return HttpResponse(json, mimetype='application/json')


