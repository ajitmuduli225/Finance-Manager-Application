from django.shortcuts import render,redirect

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from finance.models import *
from finance.forms import *
from django.db.models import Sum
from datetime import datetime
from django.contrib import messages








def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')





def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'transactions': transactions})

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})

def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    if transaction.user == request.user:
        transaction.delete()
    return redirect('dashboard')




def generate_report(request):
    transactions = Transaction.objects.filter(user=request.user)
    total_income = transactions.filter(category='Salary').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.exclude(category='Salary').aggregate(Sum('amount'))['amount__sum'] or 0
    savings = total_income - total_expenses
    current_month = datetime.now().month
    monthly_transactions = transactions.filter(date__month=current_month)
    return render(request, 'report.html', {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings,
        'monthly_transactions': monthly_transactions,
    })





def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'set_budget.html', {'form': form})

def check_budget(request):
    budgets = Budget.objects.filter(user=request.user)
    for budget in budgets:
        total_spent = Transaction.objects.filter(user=request.user, category=budget.category).aggregate(Sum('amount'))['amount__sum'] or 0
        if total_spent > budget.limit:
            messages.warning(request, f"You have exceeded your budget for {budget.category}!")
    return redirect('dashboard')
