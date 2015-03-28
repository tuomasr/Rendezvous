from django import template

register = template.Library()

@register.filter
def list_skills(skills):
	return ', '.join([s.name for s in skills]) + '.'