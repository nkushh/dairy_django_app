from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cow, Milk, MilkSale
import datetime, calendar

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
	cattle = Cow.objects.count()
	milk = Milk.objects.aggregate(Sum('amount'))

	today = datetime.datetime.now()
	mwaka = today.year
	last_month = today.month - 1

	current_month_milk = Milk.objects.filter(milking_date__year=mwaka, milking_date__month=today.month).values('cow').aggregate(current_month=Sum('amount'))
	previous_month_milk = Milk.objects.filter(milking_date__year=mwaka, milking_date__month=last_month).values('cow').aggregate(previous_month=Sum('amount'))
	current_year_milk = Milk.objects.filter(milking_date__year=mwaka).values('cow').aggregate(current_year=Sum('amount'))
	users = User.objects.count()
	context = {
		'total_cattle' : cattle,
		'total_accounts' : users,
		'total_milk' : milk,
		'current_month_milk' : current_month_milk,
		'previous_month_milk' : previous_month_milk,
		'current_year_milk' : current_year_milk,
	}

	return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def fetch_cattle(request):
	cattle = Cow.objects.all()
	context = {
		'cattle' : cattle,
	}
	return render(request, 'dairy/cattle-list.html', context)


@login_required(login_url='login')
def add_cattle(request):
	return render(request, 'dairy/add-cattle.html')


@login_required(login_url='login')
def new_cattle(request):
	if request.method == "POST":
		tag_no = request.POST['tag_no']
		name = request.POST['name']
		breed = request.POST['breed']

		cow = Cow(tag_no=tag_no, name=name, breed=breed).save()
		messages.success(request, "Success! Cattle details successfully recorded.")
		return redirect('dairy:cattle-list')
	else:
		messages.error(request, "Error! Cattle details were not recorded.")
		return redirect('dairy:cattle-list')


@login_required(login_url='login')
def cattle_detail(request, cattle_id):
	cow = get_object_or_404(Cow, pk=cattle_id)
	milk = Milk.objects.filter(cow=cow).values('milking_date').annotate(total_milk=Sum('amount')).order_by('-milking_date')
	context = {
		'cow' : cow,
		'milk' : milk,
	}

	return render(request, 'dairy/cattle-detail.html', context)


@login_required(login_url='login')
def edit_cattle(request, cattle_id):
	cow = get_object_or_404(Cow, pk=cattle_id)
	context = {
		'cow' : cow,
	}

	return render(request, 'dairy/edit-cattle.html', context)


@login_required(login_url='login')
def update_cattle(request, cattle_id):
	if request.method == "POST":
		cow = get_object_or_404(Cow, pk=cattle_id)

		cow.tag_no = request.POST['tag_no']
		cow.name = request.POST['name']
		cow.breed = request.POST['breed']
		cow.save()

		messages.success(request, "Success! Cattle details successfully updated.")
		return redirect('dairy:cattle-detail', cattle_id=cow.pk)
	else:
		messages.error(request, "Error! Cattle details were not updated.")
		return redirect('dairy:cattle-detail', cattle_id=cow.pk)


@login_required(login_url='login')
def delete_cattle(request, cattle_id):
	cow = get_object_or_404(Cow, pk=cattle_id)
	cow.delete()
	messages.success(request, "Success! Cattle details successfully deleted.")
	return redirect('dairy:cattle-list')



# Milk related functions

@login_required(login_url='login')
def add_milk(request):
	cattle = Cow.objects.all()
	context = {
		'cattle' : cattle,
	}
	return render(request, 'dairy/add-milk.html', context)


@login_required(login_url='login')
def milk_records(request):
	today = datetime.datetime.now()
	mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	cattle = Cow.objects.all()
	milk = Milk.objects.filter(milking_date__year=mwaka, milking_date__month=today.month).values('cow').annotate(total_milk=Sum('amount')).order_by('-total_milk')
	context = {
		'cattle' : cattle,
		'months_choices' : months_choices,
		'milk' : milk,
	}
	return render(request, 'dairy/milk-records.html', context)


@login_required(login_url='login')
def record_milk_produced(request):
	if request.method == "POST":
		cow = get_object_or_404(Cow, pk=request.POST['cow'])
		session = request.POST['session']
		amount = request.POST['amount']
		milk = Milk(cow=cow, session=session, amount=amount).save()
		messages.success(request, "Success! {}'s {} Milk record submitted.".format(cow, session))
		return redirect('dairy:milk-records')

@login_required(login_url='login')
def record_cattle_milk(request):
	if request.method == "POST":
		cow = get_object_or_404(Cow, pk=request.POST['cow'])
		session = request.POST['session']
		amount = request.POST['amount']
		milk = Milk(cow=cow, session=session, amount=amount).save()
		messages.success(request, "Success! Milk record submitted.")
		return redirect('dairy:cattle-detail', cattle_id=cow.pk)


@login_required(login_url='login')
def monthly_milk_records(request, month):
	today = datetime.datetime.now()
	mwaka = today.year
	if not month:
		month = today.month

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))


	cattle = Cow.objects.all()
	milk = Milk.objects.filter(milking_date__year=mwaka, milking_date__month=month).values('cow').annotate(total_milk=Sum('amount')).order_by('-total_milk')
	query_month = calendar.month_name[int(month)]

	context = {
		'milk' : milk,
		'cattle' : cattle,
		'months_choices' : months_choices,
		'query_month' : query_month,
	}
	return render(request, 'dairy/milk-records.html', context)


@login_required(login_url='login')
def milk_sale_records(request):
	sales = MilkSale.objects.all()

	today = datetime.datetime.now()
	mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	context = {
		'sales' : sales,
		'months_choices' : months_choices,
	}
	return render(request, 'dairy/milk-sale.html', context)


@login_required(login_url='login')
def record_milk_sale(request):
	if request.method == "POST":
		milk = float(request.POST['milk'])
		amount = milk * float(request.POST['amount'])
		date_sold = request.POST['date_sold'] 
		sale = MilkSale(milk=milk, amount=amount, date_sold=date_sold).save()
		return redirect('dairy:milk-sale-records')


@login_required(login_url='login')
def monthly_milk_sales(request, month):
	today = datetime.datetime.now()
	mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))


	sales = MilkSale.objects.filter(date_sold__year=mwaka, date_sold__month=month).order_by('-date_sold')
	context = {
		'sales' : sales,
		'months_choices' : months_choices,
	}
	return render(request, 'dairy/milk-sale.html', context)

@login_required(login_url='login')
def annual_milk_sales(request):
	sales = MilkSale.objects.filter(milking_date__year=today.year).values('milking_date.month').annotate(total_sales=Sum('amount')).order_by('milking_date.month')
	context = {
		'sales' : sales,
	}
	return render(request, 'dairy/milk-sale.html', context)



