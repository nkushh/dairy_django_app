from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

# Create your views here.

def all_accounts(request):
	users = User.objects.all()
	context = {
		'users' : users,
	}
	return render(request, 'authentication/accounts.html', context)

def register_user(request):
	if request.method=='POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			username = userObj['username']
			email = userObj['email']
			password = userObj['password']

			if not(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				User.objects.create_user(username, email, password)
				messages.success(request, "Success! Account detail successfully recorded.")
				return redirect('authentication:accounts')
			else:
				raise forms.ValidationError('Username with that email or password already exists')

	else:
		form = UserRegistrationForm()
	return render(request, 'authentication/register-user.html', {'form' : form})

