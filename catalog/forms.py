from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy
import datetime


class RenewBookForm(forms.Form):

    renewal_date = forms.DateField(help_text='Enter a date between now and 4 weeks(default 3)')

    def clean_renewal_date(self):

        date = self.cleaned_data['renewal_date']
        if date < datetime.date.today():
            raise ValidationError(ugettext_lazy('Invalid date'))

        if date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(ugettext_lazy('Invalid date'))

        return date


class CreateUserForm(forms.Form):
    pass
