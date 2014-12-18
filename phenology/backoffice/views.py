#from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from backend.admin import UserAdmin
from django.forms.models import inlineformset_factory
from backend import models
from backoffice.forms import AccountForm, UserForm, AreaForm, IndividualForm, CreateIndividualForm
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


@login_required(login_url='login/')
def index(request):
    return render(request, 'board.html')