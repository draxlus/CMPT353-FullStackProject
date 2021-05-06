from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
from .models import *
from .forms import OrderForm, UpdateOrderForm

def home(request):
	orders = Order.objects.all()

	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/customer_dashboard.html', context)
	return render(request, 'accounts/customer_dashboard.html')

def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
def employee(request):
	orders = Order.objects.all()

	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders,'delivered':delivered,
	'pending':pending }
	return render(request, 'accounts/dashboard.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('employee')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('employee')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			# return redirect('/')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {'form':form}
	return render(request, 'accounts/order.html', context)

def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = UpdateOrderForm(instance=order)

	if request.method == 'POST':
		form = UpdateOrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order.html', context)

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)