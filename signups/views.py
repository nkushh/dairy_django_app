from django.shortcuts import render
from django.contrib import messages

from .models import Signup

from .forms import SignupForm

# Create your views here.
def home(request):
	form = SignupForm(request.POST or None)
	if(form.is_valid):
		save_it = form.save(commit=False)
		save_it.save()
		messages.success(request, "Successfully signed up. Thank you for joining!")
	context = {
		'form': form,
	}
	return render(request, "signup.html", context)
