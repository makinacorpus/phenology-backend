from django import forms
from backend import models
from django.contrib.auth.models import User


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