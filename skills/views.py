# Django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q, Count
from django.template.loader import render_to_string

# JSON
import simplejson

# Project
from users.models import UserProfile
from skills.models import Skill, Preferences
from skills.forms import AddSkillsForm
from linkedin_integration.forms import ReviewProfileForm

# Add skills for some target object such as User or Position
def add_skills_for(target, skills_str):
	skill_list = [name.lower().strip(' ') for name in skills_str.split(',') if not name.isspace()]	# remove skills that contain only whitespace		
	skill_list = list(set(skill_list)) 																# remove duplicates

	for s in skill_list:		
		obj, created = Skill.objects.get_or_create(name=s)
		target.skills.add(obj)
		target.save()

def skills_to_list(obj):
	return [str(skill) for skill in obj.skills.all()]

def skills_to_str(obj):
	return ', '.join([str(skill) for skill in obj.skills.all()])

# Update an existing skillset with new skills.
def update_skills(user, skills):
	skill_list = [name.lower().strip(' ') for name in skills.split(',') if not name.isspace()]	# remove skills that contain only whitespace
	current_skillset = []
	
	for s in user.skills.all():
		current_skillset.append(s.name)
	
	current_skillset = [name.lower().strip(' ') for name in current_skillset if not name.isspace()]
	
	#set removes duplicates
	added = list(set(skill_list)-set(current_skillset))
	removed = list(set(current_skillset)-set(skill_list))
	
	for s in added:		
		obj, created = Skill.objects.get_or_create(name=s)
		
		if created:
			user.skills.add(obj)
			user.save()
		else:
			user.skills.add(obj)
			user.save()

	for s in removed:
		user.skills.get(name=s).delete()
		user.save()

# A view for autocomplete
def get_skills(request):
	if request.is_ajax():
		term = request.GET.get('term','') #jquery-ui.autocomplete parameter
		skills = Skill.objects.filter(name__istartswith=term) #lookup for a city (case-insensitive)
		res = []
		for c in skills:
			#make dict with the metadatas that jquery-ui.autocomple needs (the documentation is your friend)
			dict = {'id':c.id, 'label':c.__unicode__(), 'value':c.__unicode__()}
			res.append(dict)
		
		data = simplejson.dumps(res)
	else:
		data = 'fail'
	
	return HttpResponse(data, 'application/json')

# Add skills to your profile
def manage_skills(request):
	if request.method == 'POST':
		form = AddSkillsForm(request.POST)
		user = request.user
		
		if form.is_valid() and user is not None:
			# transform the skill list from a string to a Python list
			skill_list = [name.lower().strip(' ') for name in form.get_skills().split(',') if not name.isspace()]	# remove skills that contain only whitespace
			update_skillset(user, skill_list)
			
			return HttpResponseRedirect('/')
	else:
		user = request.user
		skill_str = user.skillset
		form = AddSkillsForm(initial={'skills':skill_str})
		
	return render_to_response('skills/manage.html', RequestContext(request, {'form': form}))

def search_users_by_skills(request):
	data = {'html':''}

	if request.method == 'GET' and request.is_ajax():
		skill_list = [name.lower().strip(' ') for name in request.GET.getlist('content')[0].split(',') if not name.isspace()]

		user_list = UserProfile.objects.filter(skills__name__in=skill_list).annotate(skills_count=Count('skills')).filter(skills_count=len(skill_list))

		data['html'] = render_to_string('schemes/suggestions.html', {'user_list':user_list})

	json = simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')

def create_preferences(user):
	p = Preferences()
	p.engineering = 50
	p.design = 50
	p.business = 50
	p.communication = 50
	p.save()

	user.preferences = p
	user.preferences.save()

