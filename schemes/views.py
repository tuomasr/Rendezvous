#Django
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.forms.formsets import formset_factory
from django.template.loader import render_to_string

# Settings
from django.conf import settings

# JSON
import simplejson

# Skills
from skills.views import skills_to_list, skills_to_str

#Scheme
from schemes.models import Scheme
from schemes.forms import SchemeBasicForm, SchemePositionForm
from users.models import UserProfile
from positions.models import Position
from messaging.models import Application, Invitation

# Skills
from skills.views import skills_to_list

def index(request):
	user = request.user
	user_skillset = set(skills_to_list(user))
	latest_scheme_list = Scheme.objects.order_by('-pub_date')[:5]
	latest_scheme_list_sorted = []
	scheme_data_list = []

	if latest_scheme_list.count() > 0:
		for idx, s in enumerate(latest_scheme_list):
			matches = []
			positions = []
			states = []

			for p in Position.objects.open_positions(s):
				positions.append(p)
				matched_skills = set(skills_to_list(p)).intersection(user_skillset)
				val = float(len(matched_skills))/len(skills_to_list(p))*100
				matches.append(val)
				if val >= 50:
					states.append('high')
				elif val >= 25:
					states.append('medium')
				else:
					states.append('low')


			scheme_data = zip(positions, matches, states)
			sorted_scheme_data = sorted(scheme_data, reverse=True, key=lambda tup: tup[1])
			scheme_data_list.append(sorted_scheme_data)


		latest_scheme_list_sorted = zip(latest_scheme_list, scheme_data_list)

	return render_to_response('schemes/index.html', RequestContext(request, {'latest_scheme_list':latest_scheme_list_sorted}))
	
def detail(request, scheme_id):
	scheme = get_object_or_404(Scheme, pk=scheme_id)
	return render_to_response('schemes/detail.html', RequestContext(request, {'scheme': scheme}))

def detail_ajax(request, scheme_id):
	data = {'html': ''}

	if request.method == 'GET' and request.is_ajax():
		scheme = get_object_or_404(Scheme, pk=scheme_id)
		data['html'] = '<h3>Details for the scheme</h3>' + render_to_string('schemes/scheme_detail.html', RequestContext(request, {'scheme': scheme}))

		json = simplejson.dumps(data)
		return HttpResponse(json, mimetype='application/json')

def handle_uploaded_file(f):
	print settings.MEDIA_ROOT + 'file.txt'
	with open(settings.MEDIA_ROOT + 'file.txt', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def new_scheme(request):
	PositionFormSet = formset_factory(SchemePositionForm, max_num=10)
	user = request.user

	if request.method == 'POST':
		basic_form = SchemeBasicForm(request.POST, request.FILES)
		position_formset = PositionFormSet(request.POST, request.FILES)
		
		if basic_form.is_valid() and position_formset.is_valid() and user is not None:
			scheme = basic_form.save(user)
			if 'file' in request.FILES:
				handle_uploaded_file(request.FILES['file'])

			scheme.admins.add(user)
			scheme.save()

			for form in position_formset:
				if not form.clean():
					print 'form is not clean'
					scheme.delete()
					return render_to_response('schemes/new.html', RequestContext(request, {'basic_form': basic_form, 'position_formset':position_formset}))

				form.save(scheme, user)

			return HttpResponseRedirect('/schemes/')
		else:
			print basic_form.errors
			for form in position_formset.forms:
				print form.errors
				form.clean()
	else:
		basic_form = SchemeBasicForm()
		position_formset = PositionFormSet()
				
	return render_to_response('schemes/new.html', RequestContext(request, {'basic_form': basic_form, 'position_formset':position_formset}))
	
def manage_schemes(request):
	user = request.user
	scheme_list = []
	admin_schemes = user.admin_in_schemes.all().order_by('-pub_date')
	member_schemes = user.member_in_schemes.all().order_by('-pub_date')

	scheme_list.append(admin_schemes)
	scheme_list.append(member_schemes)

	return render_to_response('schemes/manage.html', RequestContext(request, {'scheme_list':scheme_list}))

def delete(request, scheme_id):
	user = request.user
	scheme = Scheme.objects.get(pk=scheme_id)

	if user in scheme.admins.all():
		scheme.admins.remove(user)

	elif user in scheme.members.all():
		scheme.members.remove(user)

	if scheme.admins.count() == 0:
		scheme.delete()

	return HttpResponseRedirect('/schemes/manage/')

def modify(request, scheme_id):
	user = request.user
	scheme = Scheme.objects.get(pk=scheme_id)
	PositionFormSet = formset_factory(SchemePositionForm, extra=0)

	# open a form for modifying the scheme

	if request.method == 'POST':
		basic_form = SchemeBasicForm(request.POST, instance=scheme)
		position_formset = PositionFormSet(request.POST, request.FILES)
		user = request.user

		if basic_form.is_valid() and position_formset.is_valid() and user is not None:
			print 'valid'
			scheme = basic_form.update(user, scheme)

			for form in position_formset.forms:
				position = form.save(scheme, user)

			return HttpResponseRedirect('/schemes/manage/')
		else:
			for form in position_formset.forms:
				print form.errors
	else:
		initial_data = []

		for s in scheme.positions.all():
			if s.vacant:
				d = {'position':s.name, 'skills':skills_to_str(s)}
				initial_data.append(d)

		if initial_data == []:
			initial_data.append({'position':'', 'skills':''})

		basic_form = SchemeBasicForm(initial={'name':scheme.name, 'description':scheme.description, 'url':scheme.url, 'progress':scheme.progress, 'location':scheme.location, 'admin_position':Position.objects.get(scheme=scheme, holder=user, admin=True).name})
		position_formset = PositionFormSet(initial=initial_data)

	return render_to_response('schemes/modify.html', RequestContext(request, {'basic_form': basic_form, 'position_formset':position_formset}))

def add_user_to_scheme(request, scheme_id, sender, position, status):
	scheme = Scheme.objects.get(pk=scheme_id)
	sender = UserProfile.objects.get(username=sender)

	position = scheme.positions.filter(name=position, vacant=True)[0]

	member = admin = False

	if position in scheme.positions.all():
		valid_position = True
	else:
		valid_position = False

	if status == 'member':
		member = True
	elif status == 'admin':
		admin = True

	if scheme and sender and valid_position and (member or admin):
		if member:
			scheme.members.add(sender)
		else:
			scheme.admins.add(sender)

		position.vacant = False
		position.holder = sender
		try:
			Application.objects.get(sender=sender, scheme=scheme).delete()
		except:
			Invitation.objects.get(recipient=sender, scheme=scheme).delete()
		
		position.save()
		scheme.update_date()
		scheme.save()

	return HttpResponseRedirect('/inbox/schemes/')

