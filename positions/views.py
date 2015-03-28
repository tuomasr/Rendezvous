# Django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

# JSON
import simplejson

# Project
from models import Position

def get_positions(request):
	if request.is_ajax():
		term = request.GET.get('term','') #jquery-ui.autocomplete parameter
		positions = Position.objects.filter(name__contains=term) #lookup for a city (case-insensitive)
		res = []
		for c in positions:
			#make dict with the metadatas that jquery-ui.autocomple needs
			dict = {'id':c.id, 'label':c.__unicode__(), 'value':c.__unicode__()}
			res.append(dict)
		
		data = simplejson.dumps(res)
	else:
		data = 'fail'
	
	return HttpResponse(data, 'application/json')
