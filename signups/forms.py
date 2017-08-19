from django import forms

from .models import Signup

class SignupForm(forms.ModelForm):
	class Meta:
		model = Signup
		fields = ['first_name', 'last_name', 'email']