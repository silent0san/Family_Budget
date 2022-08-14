from django import forms
from django.forms import ModelForm
from .models import Budget, BudgetRecord


class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        exclude = ('shared_with',)
        fields = {'name'}
        widgets = {'owner': forms.HiddenInput(), 'created_dane': forms.HiddenInput(), 'shared_with': forms.HiddenInput(),
                   'sum': forms.HiddenInput()}


class RecordForm(ModelForm):
    class Meta:
        model = BudgetRecord
        fields = {'name', 'value'}
        widgets = {'created_date': forms.HiddenInput()}
    field_order = ['name', 'value']
