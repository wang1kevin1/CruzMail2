import csv

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Permission
from django.views.decorators.csrf import csrf_exempt
from .collection.models import mailstops_master, packages_master, people_master

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from django.core.mail import send_mail
from background_task import background


# PACKAGE VIEWS-------------------------------------------------------------------------------------------------------------
@csrf_exempt
def query_package(request):

    #make sure user is logged in
    if request.user is None:
      return

    params = []    
    index = request.POST.get('index')

    #gets proper queries and stores it into an array
    for r in packages_master.objects.filter(pkg_tracking__startswith =     request.POST.get('search'),
                                            mailstop__startswith =     request.POST.get('mailstop'),
                                            name__startswith =         request.POST.get('name'),
                                            pkg_email__startswith =    request.POST.get('email'),
                                            pkg_status__startswith =   request.POST.get('status'),):

      t = dict(pkg_tracking = r.pkg_tracking,
               pkg_status = r.pkg_status,
               pkg_date_rec = r.pkg_date_rec,
               name = r.name,
               mailstop = r.mailstop,
               sign = r.pkg_sign,
               weight = r.pkg_weight,
               email = r.pkg_email,
               pkg_width = r.pkg_width,
               pkg_height = r.pkg_height,
               pkg_length = r.pkg_length,
               pkg_remarks = r.pkg_remarks
              )
      params.append(t)

    print(params)
    return JsonResponse(dict(params= params))

@csrf_exempt
def package_delivered(request):

    if request.user is None:
      return

    print(request.POST.get('pkg_tracking'))

    #updates package as delievered and saves it
    #t = packages_master.objects.get(pkg_tracking=request.POST.get('pkg_tracking'))

    send_mail(
    'PACKAGE ' + request.POST.get('pkg_tracking') + ' DELIVERED TO ' + request.POST.get('mailstop'),
    'Your package has been delivered to the mailstop at ' + request.POST.get('mailstop') + '.',
    'cruzmail.ucsc@gmail.com',
    [request.POST.get('pkg_email')],
    )

    p = packages_master.objects.get(pkg_tracking=request.POST.get('pkg_tracking'))
    p.pkg_status = 'delivered'
    p.save()

    return JsonResponse(dict(test="ok"))

@csrf_exempt
def update_package(request):

    if request.user is None:
      return
    height = request.POST.get('height')
    width  = request.POST.get('width')
    length = request.POST.get('height')
    if height is '':
      height = None
    if width is '':
      width = None
    if length is '':
      length = None

    #update package information based on the data from request parameter
    p = packages_master.objects.get(pkg_tracking=request.POST.get('track'))
    p.name =       request.POST.get('name')
    p.pkg_email =  request.POST.get('email')
    p.pkg_weight = request.POST.get('weight')
    p.pkg_sign =   request.POST.get('sign')

    p.pkg_width =  width
    p.pkg_height = height
    p.pkg_length = length
    
    p.save()
    return JsonResponse(dict(test="ok"))

@csrf_exempt
def add_package(request):

    if request.user is None:
      return

    height = request.POST.get('height')
    width  = request.POST.get('width')
    length = request.POST.get('height')
    if height is '':
      height = None
    if width is '':
      width = None
    if length is '':
      length = None
    #inputs package information based on the data from request parameter
    packages_master.objects.create(pkg_tracking = request.POST.get('track'),
                                  name =        request.POST.get('name'),
                                  mailstop =    request.POST.get('mailstop'),
                                  pkg_status =  'received',
                                  pkg_sign =    request.POST.get('sign'),
                                  pkg_email =   request.POST.get('email'),
                                  pkg_weight =  request.POST.get('weight'),
                                  pkg_remarks = request.POST.get('remark'),
                                  pkg_height =  height,
                                  pkg_width =   width,
                                  pkg_length =  length)

    send_mail(
    'PACKAGE ' + request.POST.get('track'),
    'This is a notification that your package has arrived at the UCSC barn. It will take another 1 to 2 days to deliver the package to your location.',
    'cruzmail.ucsc@gmail.com',
    [request.POST.get('email')],
    )

    return JsonResponse(dict(test="ok"))

# MAILSTOP VIEWS-------------------------------------------------------------------------------------------------------------
@csrf_exempt
def query_mailstop(request):

    if request.user is None:
      return

    params = []
    search = request.POST.get('search')
    index = int(request.POST.get('index'))
    for r in mailstops_master.objects.filter(mailstop__icontains = search).union(mailstops_master.objects.filter(ms_name__icontains = search)):
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
    index = int(request.POST.get('index'))
    for r in people_master.objects.filter(name__icontains = request.POST.get('search')):
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
    t.ppl_status='Inactive'
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
                                 ppl_status  = 'Active',
                                 mailstop    = request.POST.get('mailstop'),
                                )
    return JsonResponse(dict(test="ok"))

@csrf_exempt
def export_packages(request):
    return export_csv(request, packages_master)

@csrf_exempt
def export_people(request):
    return export_csv(request, people_master)

@csrf_exempt
def export_mailstops(request):
    return export_csv(request, mailstops_master)

@csrf_exempt
def export_csv(request, tableName):

    if request.user is None:
      return
    #print("In export_csv python method")
    meta = tableName._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    #writer.writerow(field_names)
    for obj in tableName.objects.all():
        #print("Getting Attributes of " + obj.name)
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

@csrf_exempt
@background(schedule=120)
def import_people(request):

    #request = request.__dict__
    if request.user is None:
        return

    # Delete values in people table
    clear_table(people_master)

    # Upload temp import csv
    if request.method == "POST":
        f = request.FILES['people_csv']
        with open("/tmp/people_csv.csv", 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    
    # Read uploaded CSV and import data
    with open("/tmp/people_csv.csv") as f:
        reader = csv.reader(f)

        # Creates a new model for each row in the csv file
        for row in reader:
            _, created = people_master.objects.get_or_create(
                name=row[2]+" "+row[1],
                ppl_email=row[6]+"@ucsc.edu",
                ppl_status=row[4],
                mailstop=row[5],
            )

    return redirect('/person')

@csrf_exempt
def import_packages(request):
    if request.user is None:
        return

    # Delete values in people table
    clear_table(packages_master)

    # Upload temp import csv
    if request.method == "POST":
        f = request.FILES['package_csv']
        with open("/tmp/package_csv.csv", 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    
    # Read uploaded CSV and import data
    with open("/tmp/package_csv.csv") as f:
        reader = csv.reader(f)
        # Creates a new model for each row in the csv file
        for row in reader:
            _, created = packages_master.objects.get_or_create(
                pkg_tracking=row[0],
                name=row[1],
                mailstop=row[2],
                pkg_status=row[3],
                pkg_sign=row[4],
                pkg_email=row[5],
                pkg_weight=row[6],
                pkg_height=row[7],
                pkg_width=row[8],
                pkg_length=row[9],
                pkg_date_rec=row[10],
                pkg_date_del=row[11],
                pkg_remarks=row[12],
            )

    return redirect('/manage')

@csrf_exempt
def import_mailstops(request):

    if request.user is None:
        return

    # Delete values in mailstop table
    clear_table(mailstops_master)

    # Upload temp import csv
    if request.method == "POST":
        f = request.FILES['mailstop_csv']
        with open("/tmp/mailstop_csv.csv", 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    
    # Read uploaded CSV and import data
    with open("/tmp/mailstop_csv.csv") as f:
        reader = csv.reader(f)
        # Creates a new model for each row in the csv file
        for row in reader:
            _, created = mailstops_master.objects.get_or_create(
                mailstop=row[1],
                ms_name=row[0],
                ms_route=row[2],
                ms_route_order=row[3],
                ms_status='Active',
            )
    
    return redirect('/mailstop')

@csrf_exempt
def clear_table(tableName):
    tableName.objects.all().delete()

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

  if request.user.is_authenticated:
    return render(request, 'menu.html')
  return render(request, 'search.html')

@login_required(login_url='/account/login')
def manage(request):

  return render(request, 'package.html')

@login_required(login_url='/account/login')
def menu(request):
  return render(request, 'menu.html')

@login_required(login_url='/account/login')
def help(request):
  return render(request, 'help.html')


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

