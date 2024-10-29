from django import forms
from finance.models import *



class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields='__all__'



class BudgetForm(forms.ModelForm):
    class Meta:
        model=Budget
        fields='__all__'