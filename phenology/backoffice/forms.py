from django import forms
from backend import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # magic
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)
        # magic end

        super(AccountForm, self).__init__(*args, **kwargs)

        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)
        self.fields.keyOrder = ['last_name', 'first_name', 'email',
                                'fonction', 'adresse', 'codepostal',
                                'city', 'phone', 'mobile', 'nationality']

    def save(self, *args, **kwargs):
        # save both forms
        self.uf.save(*args, **kwargs)
        return super(AccountForm, self).save(*args, **kwargs)

    class Meta:
        model = models.Observer
        exclude = ('user', 'is_crea', 'is_active', 'areas', 'date_inscription')
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 2}),
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = models.Area
        exclude = ('species', 'polygone', 'codezone')
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 4}),
        }


class SurveyForm(forms.ModelForm):
    class Meta:
        exclude = ('is_dead',)
        model = models.Survey
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 4}),
            'individual': forms.HiddenInput(),
            #'date': forms.DateInput(format="%d %B %Y"),
            #'date': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        self.base_fields['stage'].queryset = instance.\
            individual.\
            species.\
            stage_set.filter(is_active=True).order_by("order")
        self.base_fields['stage'].label = _("Change stage")
        super(SurveyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if(self.cleaned_data["answer"] in ("today", "before")):
            self.cleaned_data["answer"] = "isObserved"
        instance = super(SurveyForm, self).save(commit=False)
        instance.save()
        return instance


class CreateIndividualForm(forms.ModelForm):
    class Meta:
        exclude = ('is_dead',)
        model = models.Individual
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 4}),
            'area': forms.HiddenInput()
        }


class IndividualForm(CreateIndividualForm):
    class Meta:
        exclude = ('area',)
        model = models.Individual
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 4}),
        }
