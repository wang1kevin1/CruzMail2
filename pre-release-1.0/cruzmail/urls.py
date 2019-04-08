"""cruzmail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:

Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from .import views


from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^index', views.index, name="index"),
    url(r'^admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    path('manage/', views.manage, name='manage'),
    path('collection/', views.collection, name='collection'),
    path('',        views.home,   name='home'),
    path('menu/', views.menu, name='menu'),
    path('mailstop/', views.mailstop, name='mailstop'),
    path('logging_out/', views.logging_out, name='logging_out'),
    path('person/', views.person, name='person'),
    #path('collection/', CollectionPageViews>as_view(), name='users'),

    url(r'^account/', include('cruzmail.account.urls')),
    # url(r'^inbox/', include('cruzmail.inbox.urls'))

    # Manage (Package Management)
    #url(r'collection/^$',views.new_package, name='new_package')
    url(r'^query_package', views.query_package, name='new_package'),
    url(r'^package_delivered', views.package_delivered, name='package_delivered'),
    url(r'^update_package', views.update_package, name='update_package'),
    url(r'^add_package', views.add_package, name='add_package'),

    # Mailstops (Mailstop Management)
    #url(r'collection/^$',views.new_mailstop, name='new_mailstop')
    url(r'^query_mailstop', views.query_mailstop, name='new_mailstop'),
    url(r'^activate_mailstop', views.activate_mailstop, name='activate_mailstop'),
    url(r'^deactivate_mailstop', views.deactivate_mailstop, name='deactivate_mailstop'),
    url(r'^update_mailstop', views.update_mailstop, name='update_mailstop'),
    url(r'^add_mailstop', views.add_mailstop, name='add_mailstop'),

    # People (Recipient Management)
    #url(r'collection/^$',views.new_mailstop, name='new_mailstop')
    url(r'^query_person', views.query_person, name='new_person'),
    url(r'^away_person', views.away_person, name='away_person'),
    url(r'^update_person', views.update_person, name='update_person'),
    url(r'^add_person', views.add_person, name='add_person'),
    
    # Admin (Employee Management)
    url(r'^get_users', views.get_users, name='get_users'),
    url(r'^get_emails', views.get_emails, name='get_emails'),
    url(r'^delete_users', views.delete_users, name='delete_users'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
