from django import forms
from django.contrib.auth.models import User
from .models import Notes
from django.db import models

class AddNoteForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AddNoteForm, self).__init__(*args, **kwargs)
		self.fields['body'].label = "Content:"

	body = forms.CharField(widget=forms.Textarea(attrs={"rows":3, "cols":60}))
	class Meta:
		model = Notes

		fields = ['body']
		labels = {
			'body': 'Content:',
		}
