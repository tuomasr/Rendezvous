# Django
from django.http import HttpResponse, HttpResponseRedirect
from itertools import chain

# JSON
import simplejson

# Geolocation
from cities_light.models import City, Country, Region


# A view for autocomplete
def get_location(request, location_type):
	if request.is_ajax():
		term = request.GET.get('term','') #jquery-ui.autocomplete parameter

		if location_type == 'city':
			geos = City.objects.filter(name__istartswith=term) #lookup for a city (case-insensitive)
		elif location_type == 'country':
			geos = Country.objects.filter(name__istartswith=term)
		else:
			geos = list(chain(City.objects.filter(name__istartswith=term), Country.objects.filter(name__istartswith=term), Region.objects.filter(name__istartswith=term)))

		res = []
		for c in geos:
			#make dict with the metadatas that jquery-ui.autocomple needs (the documentation is your friend)
			dict = {'id':c.id, 'label':c.__unicode__(), 'value':c.__unicode__().split(',')[0]}
			res.append(dict)
		
		data = simplejson.dumps(res)
	else:
		data = 'fail'
	
	return HttpResponse(data, 'application/json')