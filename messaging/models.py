# Python
import datetime

# Django
from django.db import models
from django.db.models import Q

class MessageManager(models.Manager):
	# Returns all messages that were received by the given user.
	def inbox(self, user):
		return self.get_query_set().filter(recipient=user.pk, deleted=False, read=False)

	# Return outbox
	def outbox(self, user):
		return self.get_query_set().filter(sender=user, deleted=False)

	# Return trash
	def trash(self, user):
		return self.get_query_set().filter(recipient=user, deleted=False)

	# Return conversation
	def threads_for_user(self, user):
		return self.select_related('sender', 'recipient').filter(Q(recipient=user) | Q(sender=user)).order_by('-thread').filter(deleted=False)

	def thread(self, thread):
		return self.get_query_set().filter(thread=thread, deleted=False)

class Message(models.Model):
	# Who
	sender = models.ForeignKey('users.UserProfile', related_name='sent_messages')			# A message has only one sender but the sender can have multiple sent messages
	recipient = models.ForeignKey('users.UserProfile', related_name='received_messages')	# A message has multiple recipients and the recipient has multiple received messages

	# What
	headline = models.CharField(max_length=50, blank=False)
	contents = models.TextField(blank=False)
	parent = models.ForeignKey('self', related_name='next_messages', null=True, blank=True)
	thread = models.ForeignKey('self', related_name='child_messages', null=True, blank=True)

	# When
	sent_at = models.DateTimeField('date published', auto_now_add=True)
	read_at = models.DateTimeField(null=True, blank=True)
	deleted_at = models.DateTimeField(null=True, blank=True)

	# Settings
	read = models.BooleanField(default=False)
	deleted = models.BooleanField(default=False)

	# Custom manager for messages
	objects = MessageManager()

	def mark_read(self):
		self.read = True
		self.read_at = datetime.datetime.now()
		self.save()

	def mark_deleted(self):
		self.deleted = True
		self.deleted_at = datetime.datetime.now()
		self.save()

	def __unicode__(self):
		return unicode(self.sender.username + ' - ' + self.headline + ': ' + self.contents)
	
class Application(Message):
	# Which scheme?
	scheme = models.ForeignKey('schemes.Scheme', blank=False, related_name='applications')				# A scheme can have multiple applications but an application has only one scheme
	
	# Application-specific contents
	position = models.CharField(max_length=50, blank=False)

	objects = MessageManager()
	
	def __unicode__(self):
		return unicode(self.sender.username + ' applying for ' + self.position + ' - ' + self.headline + ': ' + self.contents)

class Invitation(Message):
	# Which scheme?
	scheme = models.ForeignKey('schemes.Scheme', blank=False)				# A scheme can have multiple applications but an application has only one scheme

	# Invitation-specific contents
	position = models.CharField(max_length=50, blank=False)

	# Is the invitation accepted?
	accepted = models.BooleanField(default=False)

	objects = MessageManager()

	def __unicode__(self):
		return unicode(self.sender.username + ' invited ' + self.recipient + ' to ' + self.position + ' - ' + self.headline + ': ' + self.contents)



