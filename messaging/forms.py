# Python
import uuid

# Django
from django import forms

# Project
from messaging.models import Application
from schemes.models import Scheme
from models import Message
from positions.models import Position

class SimpleMessageForm(forms.Form):
	# A basic message
	headline = forms.CharField(max_length=50)
	contents = forms.CharField(widget=forms.Textarea)

	def save(self, sender, recipient):
		data = self.cleaned_data
		new_message = Message(sender=sender, recipient=recipient, headline=data['headline'], contents=data['contents'])
		new_message.save()

class SimpleReplyForm(SimpleMessageForm):
	def get_thread(self, parent):
		if parent.thread:
			return parent.thread
		else:
			parent.thread = parent
			parent.save()
			return parent

	def save(self, sender, recipient, parent):
		data = self.cleaned_data
		reply_message = Message(sender=sender, recipient=recipient, headline=data['headline'], contents=data['contents'], parent=parent, thread=self.get_thread(parent))
		reply_message.save()

		return reply_message

class ApplicationForm(forms.Form):
	# A form for creating new applications to Schemes
	
	headline = forms.CharField(max_length=30)
	positions = forms.ChoiceField()
	description = forms.CharField(widget=forms.Textarea)
	
	def save(self, user, scheme):
		data = self.cleaned_data
		headline = data['headline']
		position = data['positions']
		description = data['description']
				
		application = Application(sender=user, recipient=scheme.admins.all()[0], scheme=scheme, headline=headline, position=position, contents=description)
		application.save()
		application.thread = application
		application.save()
		
	