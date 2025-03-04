from django.forms import ModelForm
from django import forms
from .models import GroupExpense, Category, Expense
from django.contrib.auth.models import User

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter categories by the logged-in user (assuming there's a user field in Category model)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
        
        
class GroupExpenseForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), 
        widget=forms.CheckboxSelectMultiple,  # Allows multiple user selection with checkboxes
        required=True
    )

    class Meta:
        model = GroupExpense
        fields = ['name', 'amount', 'users']