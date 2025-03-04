import datetime
from django.shortcuts import redirect, render
from .forms import ExpenseForm, GroupExpenseForm
from .models import Expense, Category, GroupExpense
from django.db.models import Sum
from django.contrib.auth.decorators import login_required 
from .filters import ExpenseFilter
from django.contrib.auth.models import User


@login_required
def add_group_expense(request):
    if request.method == 'POST':
        form = GroupExpenseForm(request.POST)
        if form.is_valid():
            group_expense = form.save(commit=False)
            group_expense.date = datetime.date.today()  # Set the date
            group_expense.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('group_expense_list')
    else:
        form = GroupExpenseForm()
    
    return render(request, 'myapp/add_group_expense.html', {'form': form})


@login_required 
def group_expense_list(request): 
    expenses = GroupExpense.objects.filter(users=request.user)
    return render(request, 'myapp/group_expense_list.html', {'expenses': expenses}) 


@login_required 
def expense_list(request): 
    expenses = Expense.objects.filter(user=request.user) 
    expense_filter = ExpenseFilter(request.GET, queryset=expenses) 
    return render(request, 'myapp/expense_list.html', {'filter': expense_filter}) 


@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name, user=request.user)
        return redirect('category_list')
    return render(request, 'myapp/add_category.html') 


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)  # Show only user's categories
    return render(request, 'myapp/category_list.html', {'categories': categories})
# Render template for GET request

@login_required
def index(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)  # Delay saving to DB
            expense.user = request.user  # Assign the logged-in user
            expense.save()  # Save to the database
        
    expenses = Expense.objects.filter(user=request.user)
    
    # Total expenses for the logged-in user
    total_expenses = expenses.aggregate(Sum('amount'))
    
    # Expenses for the last year
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    yearly_expenses = expenses.filter(date__gt=last_year)
    yearly_sum = yearly_expenses.aggregate(Sum('amount'))
    
    # Expenses for the last month
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    monthly_expenses = expenses.filter(date__gt=last_month)
    monthly_sum = monthly_expenses.aggregate(Sum('amount'))
    
    # Expenses for the last week
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    weekly_expenses = expenses.filter(date__gt=last_week)
    weekly_sum = weekly_expenses.aggregate(Sum('amount'))
    
    # Daily sums for the logged-in user's expenses
    daily_sums = expenses.values('date').order_by('date').annotate(sum=Sum('amount'))
    
    # Categorical sums for the logged-in user's expenses
    categorical_sums = expenses.values('category').order_by('category').annotate(sum=Sum('amount'))
    
    expense_form = ExpenseForm(user=request.user)
    return render(request, 'myapp/index.html', {'expense_form':expense_form, 'expenses':expenses, 'total_expenses':total_expenses, 'yearly_sum':yearly_sum, 'monthly_sum': monthly_sum, 'weekly_sum':weekly_sum, 'daily_sums':daily_sums, 'categorical_sums':categorical_sums})
    
    

def edit(request, id):
    expense = Expense.objects.get(id=id)
    expense_form= ExpenseForm(instance=expense)
    
    if request.method == "POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid:
            form.save()
            return redirect('index')
    return render(request, 'myapp/edit.html', {'expense_form': expense_form})


def delete(request, id):
    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')
    


