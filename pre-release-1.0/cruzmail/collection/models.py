# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.contrib.auth.tokens import *
import datetime
from django.http import HttpResponse

class mailstops_master(models.Model):
   mailstop  = models.CharField(max_length = 50, primary_key = True, default = '')

   ms_name = models.CharField(max_length = 50, default = '')

   ms_route_choice = (
       ('W', 'W'),
       ('C', 'C'),
       ('E', 'E'))
   ms_route = models.CharField(max_length = 10, choices = ms_route_choice, default = 'W')

   ms_route_order = models.CharField(max_length = 3, default = '')

   ms_status_choice = (
       ('Active', 'Active'),
       ('Inactive', 'Inactive'),)
   ms_status = models.CharField(max_length = 8, choices = ms_status_choice, default = 'Active')

class people_master(models.Model):
   name        = models.CharField(max_length = 50, primary_key = True, default = '')
   ppl_email   = models.CharField(max_length = 50, default = '')

   ppl_status_choice = (
       ('Available', 'Available'),
       ('Away', 'Away'),)
   ppl_status = models.CharField(max_length = 9, choices = ppl_status_choice, default = 'Available')

   mailstop = models.CharField(max_length = 50, default = '')

   # allows for people with the same name to reside in system as long as different mailstops. Messes up request.POST.get
   #class Meta:
       #unique_together = (('name', 'mailstop'),)

class packages_master(models.Model):
   pkg_tracking = models.CharField(max_length = 50, primary_key = True, default = '')
   name         = models.CharField(max_length = 50, default = '')
   mailstop     = models.CharField(max_length = 50, default = '')


   pkg_status_choice = (
       ('recieved', 'recieved'),
       ('delivered', 'delivered'))
   pkg_status   = models.CharField(max_length = 9, choices = pkg_status_choice, default = '')

   pkg_sign_choice = (
       ('y', 'yes'),
       ('n', 'no'))
   pkg_sign     = models.CharField(max_length = 10, choices = pkg_sign_choice, default = 'n')


   pkg_email_choice = (
       ('y', 'yes'),
       ('n', 'no'))
   pkg_email    = models.CharField(max_length = 10, choices = pkg_email_choice, default = 'y')

   pkg_weight_choice = (
       ('s', '1 to 5'),
       ('m', '6 to 15'),
       ('l', 'over 16'))
   pkg_weight   = models.CharField(max_length = 7, choices = pkg_weight_choice, null = False)
   pkg_date_rec = models.DateField(default = datetime.date.today)
   pkg_date_del = models.DateField(default = datetime.date.today)
   pkg_remarks  = models.CharField(max_length = 144, default = '')