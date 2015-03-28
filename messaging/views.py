#Django
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string

# JSON
import simplejson

#Too bad
from django.views.decorators.csrf import csrf_exempt

#Project
from messaging.forms import ApplicationForm
from messaging.models import Message, Application, Invitation
from schemes.models import Scheme
from users.models import UserProfile
from forms import SimpleMessageForm, SimpleReplyForm

def send_application(request, scheme_id):
	scheme = Scheme.objects.get(pk=scheme_id)

	choice_list = []

	for s in scheme.positions.all():
		if s.vacant:
			t = (s.name, s.name)
			choice_list.append(t)

	if request.method == 'POST':
		form = ApplicationForm(request.POST)
		form.fields['positions'].choices = choice_list		# Django rage...
		user = request.user

		print form.errors
		
		if form.is_valid() and user is not None:
			form.save(user, scheme)

			return HttpResponseRedirect('/')
	else:
		form = ApplicationForm()
		form.fields['positions'].choices = choice_list
	
	return render_to_response('applications/send_application.html', RequestContext(request, {'form':form, 'scheme':scheme}))


def show_inbox(request):
	user = request.user
	msgs = Message.objects.threads_for_user(user)
	thread_list = []
	sorted_thread_list = []

	if msgs.count() > 0:
		prev = msgs[0]
		thread = []

		for m in msgs:
			if m.thread is None:
				thread_list.append([m])
			elif m.thread == prev.thread:
				thread.append(m)
			else:
				thread_list.append(thread)
				thread = []
				thread.append(m)
				prev = m
			m.mark_read()

		if not thread == []:
			thread_list.append(thread)

		for t in thread_list:
			t = sorted(t, key=lambda r: r.sent_at, reverse=True)
			sorted_thread_list.append(t)

		sorted_thread_list = sorted(sorted_thread_list, key=lambda r: r[0].sent_at, reverse=True)

	return render_to_response('messaging/inbox.html', RequestContext(request, {'thread_list':sorted_thread_list}))

def show_scheme_messaging(request):
	user = request.user

	applications_to_schemes = Application.objects.filter(recipient=user)
	applications_by_user = Application.objects.filter(sender=user)
	invitations_to_schemes = Invitation.objects.filter(recipient=user)
	invitations_by_user = Invitation.objects.filter(sender=user)

	[x.mark_read() for x in (list(applications_to_schemes) + list(invitations_to_schemes))]

	return render_to_response('messaging/collaborating.html', RequestContext(request, {'invitations_to_schemes':invitations_to_schemes, 'invitations_by_user':invitations_by_user, 'applications_to_schemes':applications_to_schemes, 'applications_by_user':applications_by_user}))

def send_message(request, userprofile_username):
	sender = request.user
	recipient = UserProfile.objects.get(username=userprofile_username)

	if request.method == 'POST':
		form = SimpleMessageForm(request.POST)

		if form.is_valid() and sender is not None and recipient is not None:
			form.save(sender, recipient)
			return HttpResponseRedirect('/')

	else:
		form = SimpleMessageForm()

	return render_to_response('messaging/send_message.html', RequestContext(request, {'form':form, 'recipient':recipient}))

def delete_message(request, message_id):
	message = Message.objects.get(pk=message_id)
	message.mark_deleted()

	return HttpResponseRedirect('/inbox/')

def reply(request, message_id):
	sender = request.user
	parent = Message.objects.get(pk=message_id)
	recipient = parent.sender

	if request.method == 'POST':
		form = SimpleReplyForm(request.POST)

		if form.is_valid() and sender is not None and recipient is not None:
			form.save(sender, recipient, parent)
			return HttpResponseRedirect('/')
	else:
		form = SimpleReplyForm()

	return render_to_response('messaging/reply.html', RequestContext(request, {'form':form, 'parent':parent}))

def show_application(request, application_id):
	message = {'html':''}

	if request.is_ajax():
		a = Application.objects.get(pk=application_id)

		thread = Message.objects.thread(a)

		html = render_to_string('applications/application_thread.html', {'thread': thread })
		message['html'] = html
	else:
		message['html'] = "Paskaa."
	
	json = simplejson.dumps(message)
	return HttpResponse(json, mimetype='application/json')

def reply_application(request, application_id):
	data = {'html':''}

	if request.method == 'POST' and request.is_ajax():
		form = SimpleReplyForm(request.POST)

		sender = request.user
		parent = Application.objects.get(pk=application_id)
		recipient = parent.sender

		if form.is_valid():
			msg = form.save(sender, recipient, parent)

		thread = Message.objects.thread(parent)

		data['html'] = render_to_string('applications/new_message.html', {'m': msg})
	else:
		form = SimpleReplyForm()
		data['html'] = '<h3>Your reply</h3>' + render_to_string('applications/reply_form.html', {'form': form, 'application_id':application_id})

	json = simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')
