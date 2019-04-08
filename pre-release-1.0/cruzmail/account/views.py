
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib import auth
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cruzmail.account.models import Profile, PasswordResetForm


def account(request):
	params = {}
	params['category'] = 'account'
	if request.user.is_authenticated():
		return render(request, 'account.html', {'params': params})
	else:
		return redirect('/')

def new_employee(request):
	params = {}
	params['category'] = 'new_employee'
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/User_Profile', {'user': user})
	else:
		form = SignUpForm()
	return render(request, 'new_employee.html', {'form': form, 'params':params})

def create(request):
	params = {}
	params['category'] = 'create'
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/manage', {'user': user})
	else:
		form = SignUpForm()
	return render(request, 'create.html', {'form': form, 'params':params})

def logout(request):
	auth.logout(request)
	return redirect('/', {'password_reset_form': PasswordResetForm})

def collections(request):
	return redirect('/manage')

@csrf_exempt
def update_user_bio(request):
	params = {}
	bio = request.POST.get('user_bio')
	Profile.objects.update(bio=bio)
	params['success'] = "True"
	return JsonResponse(params)

@csrf_exempt
def update_user_email(request):
	params = {}
	email = request.POST.get('user_email')
	User.objects.update(email=email)
	params['success'] = "True"
	return JsonResponse(params)

@csrf_exempt
def update_user_account_privacy(request):
	params = {}
	private_account = request.POST.get('account_private')
	privacy = True if (private_account == 'on') else False
	Profile.objects.update(private_account=privacy)
	params['success'] = "True"
	return JsonResponse(params)

@csrf_exempt
def update_user_password(request):
	params = {}
	params['success'] = "False"

	new_password1 = request.POST.get('new_password1')
	old_password = request.POST.get('old_password')

	u = User.objects.get(username=request.user.username)
	check_password = u.check_password(old_password)
	if check_password:
		u.set_password(new_password1)
		u.save()
		params['success'] = "True"
	

	return JsonResponse(params)

@csrf_exempt
def reset_password(request):
	params = {}
	params['success'] = "True"
	p = PasswordResetForm
	p.save(request.POST.get('user_email'))
	return JsonResponse(params)
