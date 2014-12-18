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
def register(request):
    return render(request, 'board.html')


@login_required(login_url='login/')
def area_detail(request, area_id=-1):
    area = models.Area.objects.filter(id=area_id).first()
    if not area:
        area = models.Area()

    if area_id == -1 or request.user.observer in area.observer_set.all():
        if request.POST:
            form = AreaForm(request.POST, instance=area)
            if form.is_valid():
                messages.add_message(request,
                                     messages.SUCCESS,
                                     'Form is successifully updated')
                form.save()
        else:
            form = AreaForm(instance=area)
        return render_to_response("profile_area.html", {
            "form": form,
        }, RequestContext(request))
    else:
        return redirect(index)


@login_required(login_url='login/')
def individual_detail(request, ind_id=-1):
    individual = models.Individual.objects.filter(id=ind_id).first()
    if not individual:
        individual = models.Individual()
        area_id = request.GET.get("area_id")
        area = models.Area.objects.get(id=area_id)
        individual.area = area
        individual.lat = area.lat
        individual.lon = area.lon

    surveys = sorted(individual.survey_set.all(),
                     key=lambda survey: survey.date,
                     reverse=True)
    surveys = surveys[:8]

    if individual.id:
        if request.user.observer in individual.area.observer_set.all():
            if request.POST:
                form = IndividualForm(request.POST, instance=individual)
                if form.is_valid():
                    messages.add_message(request,
                                         messages.SUCCESS,
                                         'Form is successifully updated')
                    form.save()
            else:
                form = IndividualForm(instance=individual)
        else:
            messages.add_message(request,
                                 messages.WARNING,
                                 'Your are not allowed to see this form')
            return redirect(index)
    else:
        if request.POST:
            form = CreateIndividualForm(request.POST, instance=individual)
            if form.is_valid():
                messages.add_message(request,
                                     messages.SUCCESS,
                                     'Form is successifully updated')
                form.save()
        else:
            form = CreateIndividualForm(instance=individual)

    return render_to_response("profile_individual.html", {
        "form": form,
        "surveys": surveys
    }, RequestContext(request))


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
