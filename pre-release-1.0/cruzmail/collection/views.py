from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import *
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_users(request):
	name_users = []
	
	
	for key in User.objects.all():
		names = dict(
			username = key.username
			)
		name_users.append(names)

	return JsonResponse(dict(user_list = name_users))

@csrf_exempt
def get_emails(request):
	name_users = []
	
	
	for key in User.objects.all():
		names = dict(
			emails = key.email
			)
		name_users.append(names)

	return JsonResponse(dict(user_list = name_users))