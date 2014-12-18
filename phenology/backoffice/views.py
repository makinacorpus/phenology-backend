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


@login_required(login_url='login/')
def user_detail(request):

    if request.POST:
        form = AccountForm(request.POST,
                           instance=request.user.observer)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Form is successifully updated')
            form.save()
        else:
            print form.errors
    else:
        form = AccountForm(instance=request.user.observer)

    return render_to_response("profile.html", {
        "form": form,
    }, RequestContext(request))


def register_user(request):
    if request.user:
        return redirect(index)

    if request.POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Form is successifully updated')
            form.save()
        else:
            print form.errors
    else:
        instance = models.Observer()
        instance.user = User()
        form = AccountForm(instance=instance)

    return render_to_response("generic_form.html", {
        "form": form,
    }, RequestContext(request))
