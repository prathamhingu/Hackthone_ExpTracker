from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transaction_list.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user

            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'add_transaction.html', {'form': form})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'delete_transaction.html', {'transaction': transaction})


@login_required
def transaction_summary(request):
    # Aggregate total amount per category
    data = (
        Transaction.objects.filter(user=request.user, transaction_type='expense')
        .values('category')
        .annotate(total=Sum('amount'))
    )

    # Prepare data for Chart.js
    categories = [item['category'] for item in data]
    amounts = [item['total'] for item in data]

    return render(request, 'transactions/transaction_summary.html', {
        'categories': categories,
        'amounts': amounts,
    })

@login_required
def transaction_data(request):
    data = (
        Transaction.objects.filter(user=request.user, transaction_type='expense')
        .values('category')
        .annotate(total=Sum('amount'))
    )
    return JsonResponse(list(data), safe=False)  # Return data as JSON


@login_required
def comparison_data(request):
    # Aggregate income and expense totals by category
    categories = Transaction.objects.values_list('category', flat=True).distinct()

    data = []
    for category in categories:
        expenses = Transaction.objects.filter(
            user=request.user, 
            transaction_type='expense', 
            category=category
        ).aggregate(total=Sum('amount'))['total'] or 0

        income = Transaction.objects.filter(
            user=request.user, 
            transaction_type='income', 
            category=category
        ).aggregate(total=Sum('amount'))['total'] or 0

        data.append({'category': category, 'expenses': expenses, 'income': income})

    return JsonResponse(data, safe=False)


@login_required
def comparison_chart(request):
    return render(request, 'comparison_chart.html')
