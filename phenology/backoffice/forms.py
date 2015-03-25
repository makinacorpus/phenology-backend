from django import forms
from backend import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(ugettext('Already exists'))
        return email


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class SnowingForm(forms.ModelForm):
    class Meta:
        model = models.Snowing
        fields = ('height', 'observer', 'remark', 'area', 'date')
        widgets = {
            'remark': forms.Textarea(attrs={'rows': 4}),
        }


class ResetPasswordForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)


class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # magic
        in_creation = True
        if (not kwargs.get('instance')):
            observer = models.Observer()
            observer.user = User()
            self.user = observer.user
        else:
            if kwargs.get('instance').id:
                in_creation = False
            kwargs["instance"].id
            self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        key_order = []
        if in_creation:
            self.uf = CreateUserForm(*args, **user_kwargs)
            key_order += ['username']
            self.uf.fields['email'].required = True
        else:
            self.uf = UserForm(*args, **user_kwargs)
        self.uf.fields['last_name'].required = True
        self.uf.fields['first_name'].required = True

        # magic end

        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)
        self.fields.keyOrder = key_order +\
            ['last_name',
             'first_name',
             'organism', 'email',
             'fonction', 'adresse', 'codepostal',
             'city', 'phone', 'mobile', 'category',
             'nationality']

    def is_valid(self):
        # save both forms
        is_valid = super(AccountForm, self).is_valid()
        if(not self.uf.is_valid()):
            self.errors.update(self.uf.errors)
            is_valid = False
        return is_valid

    def save(self, *args, **kwargs):
        # save both forms
        instance = self.uf.save(*args, **kwargs)
        self.instance.user = instance
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
            'stage': forms.HiddenInput(),
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
