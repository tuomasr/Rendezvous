# Django
from django import forms

# Project
from skills.models import Skill

class AddSkillsForm(forms.Form):
	skills = forms.CharField(widget=forms.Textarea)
	
	def get_skills(self):
		data = self.cleaned_data
		return data['skills']