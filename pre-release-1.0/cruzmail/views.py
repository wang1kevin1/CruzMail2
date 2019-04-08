from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Permission
from django.views.decorators.csrf import csrf_exempt
from .collection.models import mailstops_master, packages_master, people_master

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

# PACKAGE VIEWS-------------------------------------------------------------------------------------------------------------
@csrf_exempt
def query_package(request):

    #make sure user is logged in
    if request.user is None:
      return

    params = []    

    #gets the search information if exists
    search = request.POST.get('search')
    index = request.POST.get('index')

    #gets proper queries and stores it into an array
    for r in packages_master.objects.all():
        if search is None or search == '' or search == r.pkg_tracking:
            t = dict(pkg_tracking = r.pkg_tracking,
                     pkg_status = r.pkg_status,
                     pkg_date_rec = r.pkg_date_rec,
                     name = r.name,
                     mailstop = r.mailstop,
                     sign = r.pkg_sign,
                     weight = r.pkg_weight,
                     email = r.pkg_email
                    )
            params.append(t)

    return JsonResponse(dict(params= params))

@csrf_exempt
def package_delivered(request):

    if request.user is None:
      return

    #updates package as delievered and saves it
    #t = packages_master.objects.get(pkg_tracking=request.POST.get('pkg_tracking'))


    p = packages_master.objects.get(pkg_tracking=request.POST.get('pkg_tracking'))
    p.pkg_status = 'delivered'
    p.save()

    return JsonResponse(dict(test="ok"))

@csrf_exempt
def update_package(request):

    if request.user is None:
      return

    #update package information based on the data from request parameter
    t = packages_master.objects.get(pkg_tracking=request.POST.get('track'))
    t.name =       request.POST.get('name')
    t.pkg_email =  request.POST.get('email')
    t.pkg_weight = request.POST.get('weight')
    t.pkg_sign =   request.POST.get('sign')
    t.save()
    return JsonResponse(dict(test="ok"))

@csrf_exempt
def add_package(request):

    if request.user is None:
      return


    #inputs package information based on the data from request parameter
    packages_master.objects.create(pkg_tracking = request.POST.get('track'),
                                  name = request.POST.get('name'),
                                  mailstop = request.POST.get('mailstop'),
                                  pkg_status = 'received',
                                  pkg_sign = request.POST.get('sign'),
                                  pkg_email = request.POST.get('email'),
                                  pkg_weight = '1 to 5',
                                  pkg_remarks = request.POST.get('remark'))
    return JsonResponse(dict(test="ok"))

# MAILSTOP VIEWS-------------------------------------------------------------------------------------------------------------
@csrf_exempt
def query_mailstop(request):

    if request.user is None:
      return

    params = []
    search = request.POST.get('search')
    index = int(request.POST.get('index'))
    for r in mailstops_master.objects.all():
      if search is None or (len(search) <= len(r.mailstop) and search == r.mailstop[0:len(search)]):
        t = dict(mailstop       = r.mailstop,
                 ms_name        = r.ms_name,
                 ms_route       = r.ms_route,
                 ms_route_order = r.ms_route_order,
                 ms_status      = r.ms_status
                )
        params.append(t)
    return JsonResponse(dict(params= params))

@csrf_exempt
def activate_mailstop(request):

    if request.user is None:
      return

    t = mailstops_master.objects.get(mailstop=request.POST.get('mailstop'))
    t.ms_status='Active'
    t.save()
    return JsonResponse(dict(test="ok"))

@csrf_exempt
def deactivate_mailstop(request):

    if request.user is None:
      return

    t = mailstops_master.objects.get(mailstop=request.POST.get('mailstop'))
    t.ms_status='Inactive'
    t.save()
    return JsonResponse(dict(test="ok"))

@csrf_exempt
def update_mailstop(request):

    if request.user is None:
      return

    t = mailstops_master.objects.get(mailstop=request.POST.get('ms_id'))
    t.ms_name         = request.POST.get('ms_name')
    t.ms_route_choice = request.POST.get('ms_route')
    t.ms_route_order  = request.POST.get('ms_route_order')
    t.ms_status       = request.POST.get('ms_status')
    t.save()
    return JsonResponse(dict(test="ok"))

@csrf_exempt
def add_mailstop(request):

    if request.user is None:
      return

    mailstops_master.objects.create(mailstop        = request.POST.get('ms_id'),
                                    ms_name         = request.POST.get('ms_name'),
                                    ms_route        = request.POST.get('ms_route'),
                                    ms_route_order  = request.POST.get('ms_route_order'),
                                    ms_status       = 'Active'
                                   )
    return JsonResponse(dict(test="ok"))

# PEOPLE (CUSTOMER) VIEWS-------------------------------------------------------------------------------------------------------------
@csrf_exempt
def query_person(request):

    if request.user is None:
      return

    params = []
    search = request.POST.get('search')
    index = int(request.POST.get('index'))
    for r in people_master.objects.all():
      if search is None or (len(search) <= len(r.name) and search == r.name[0:len(search)]):
        t = dict(name       = r.name,
                 ppl_email  = r.ppl_email,
                 ppl_status = r.ppl_status,
                 mailstop   = r.mailstop
                )
        params.append(t)
    return JsonResponse(dict(params= params))

@csrf_exempt
def away_person(request):

    if request.user is None:
      return

    t = people_master.objects.get(name=request.POST.get('name'))
    t.ppl_status='Away'
    t.save()
    return JsonResponse(dict(test="ok"))

@csrf_exempt
def update_person(request):

    if request.user is None:
      return

    t = people_master.objects.get(name=request.POST.get('ppl_name'))
    t.ppl_email   = request.POST.get('ppl_email')
    t.ppl_status  = request.POST.get('ppl_status')
    t.mailstop    = request.POST.get('mailstop')
    t.save()
    return JsonResponse(dict(test="ok"))

@csrf_exempt
def add_person(request):

    if request.user is None:
      return

    people_master.objects.create(name        = request.POST.get('ppl_name'),
                                 ppl_email   = request.POST.get('ppl_email'),
                                 ppl_status  = 'Available',
                                 mailstop    = request.POST.get('mailstop'),
                                )
    return JsonResponse(dict(test="ok"))


# ADMIN VIEWS-------------------------------------------------------------------------------------------------------------

@csrf_exempt
def get_users(request):

  if request.user is None:
    return

  name_users = []
  
  
  for key in User.objects.all():
    names = dict(
      username = key.username,
      emails = key.email,
      password = key.password,
      )

    name_users.append(names)
  return JsonResponse(dict(user_list = name_users))

@csrf_exempt
def get_emails(request):

  if request.user is None:
    return

  email_names = []
  
  
  for key in User.objects.all():
    names = dict(
      emails = key.email

      )
    #print (key.email)
    email_names.append(names)

  return JsonResponse(dict(user_emails = email_names))

@csrf_exempt
def delete_users(request):

  if request.user is None:
    return

  users = User.objects.get(username=request.POST.get('key'))
  print (request.POST.get('key'))
  print (users)
  users.delete()

  
  return JsonResponse(dict(test="ok"))


#REDIRECT URLS-------------------------------------------------------------------------------------------------------------
def index(request):
    return render(request, 'search.html')

def home(request):
    return render(request, 'search.html')

@login_required(login_url='/account/login')
def manage(request):
    return render(request, 'package.html')

@login_required(login_url='/account/login')
def menu(request):
  return render(request, 'menu.html')


@login_required(login_url='/account/login')
def collection(request):
  return render(request, 'users.html')

@login_required(login_url='/account/login')
def mailstop(request):
  return render(request, 'mailstop.html')

@login_required(login_url='/account/login')
def person(request):
  return render(request, 'person.html')

def logging_out(request):
  logout(request)
  return redirect('../')

