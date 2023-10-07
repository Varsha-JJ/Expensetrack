from django.shortcuts import render,redirect
from django.conf import settings 
from django.utils import timezone
from  .models import Expense
from django.contrib import messages

# Create your views here.


def addexpense(request):
    user = request.user

    if request.method == 'POST':
        expense_name = request.POST.get('name')
        amount = request.POST.get('amount')
        transaction_date = request.POST.get('date')
        category = request.POST.get('category')

        # Check if any of the required fields are empty
        if not expense_name or not amount or not transaction_date or not category:
            # Display an error message
            messages.warning(request, 'All fields must be filled.')
            return render(request, 'addexpense.html')

        try:
            amount = float(amount)
            transaction_date = timezone.make_aware(timezone.datetime.strptime(transaction_date, '%Y-%m-%d'))
        except (ValueError, TypeError):
            # Handle validation errors here, e.g., return an error message to the user
            messages.error(request, 'Invalid input')
            return render(request, 'addexpense.html')

        Expense.objects.create(
            user=user, 
            expense_name=expense_name,
            amount=amount,
            transaction_date=transaction_date,
            category=category
        )
        messages.success(request, 'Expenses added successfully')
        return redirect('addexpense')

    return render(request, 'addexpense.html')



from django.db.models import Sum, Count 
def viewexpense(request):
    # Group expenses by month and year and calculate the total amount for each month
    expenses_by_month = Expense.objects.annotate(month=TruncMonth('transaction_date')).values('month').annotate(
        total_amount=Sum('amount'), expense_count=Count('id')).order_by('-month')

    # Create a dictionary to store expenses by month
    expenses_by_month_dict = {}

    for entry in expenses_by_month:
        month = entry['month']
        total_amount = entry['total_amount']
        expense_count = entry['expense_count']

        # Retrieve expenses for the current month
        expenses_for_month = Expense.objects.filter(transaction_date__month=month.month, transaction_date__year=month.year)

        # Add the expenses to the dictionary
        expenses_by_month_dict[month] = {
            'total_amount': total_amount,
            'expense_count': expense_count,
            'expenses': expenses_for_month
        }

    context = {'expenses_by_month': expenses_by_month_dict}
    return render(request,"viewexpense.html",context)

def editexpense(request):
     # Group expenses by month and year and calculate the total amount for each month
    expenses_by_month = Expense.objects.annotate(month=TruncMonth('transaction_date')).values('month').annotate(
        total_amount=Sum('amount'), expense_count=Count('id')).order_by('-month')

    # Create a dictionary to store expenses by month
    expenses_by_month_dict = {}

    for entry in expenses_by_month:
        month = entry['month']
        total_amount = entry['total_amount']
        expense_count = entry['expense_count']

        # Retrieve expenses for the current month
        expenses_for_month = Expense.objects.filter(transaction_date__month=month.month, transaction_date__year=month.year)

        # Add the expenses to the dictionary
        expenses_by_month_dict[month] = {
            'total_amount': total_amount,
            'expense_count': expense_count,
            'expenses': expenses_for_month
        }

    context = {'expenses_by_month': expenses_by_month_dict}
    return render(request,"editexpense.html",context)

from django.shortcuts import get_object_or_404
def update(request,id):
    allitem = Expense.objects.get(id=id)
    if request.method == 'POST':
        new_amount = request.POST.get('amount')
        if new_amount is not None:
            expense = get_object_or_404(Expense, id=id)
            expense.amount = new_amount
            expense.save()
            messages.success(request, 'Amount updated successfully')
            return redirect('editexpense')
    return render(request,"update.html",{"allitem":allitem})

def delete(request,id):
    Expense.objects.get(id=id).delete()
    messages.success(request, 'Deleted successfully')
    return redirect('editexpense')


def report(request):
    return render(request,"report.html")


from django.db.models import Sum
from django.db.models.functions import TruncMonth
def history(request):
    # Group expenses by month and year and calculate the total amount for each group
    expenses_by_month = Expense.objects.annotate(month=TruncMonth('transaction_date')).values('month').annotate(total_amount=Sum('amount')).order_by('-month')

    # Pass the expenses_by_month queryset to the template for rendering
    context = {'expenses_by_month': expenses_by_month}
    return render(request,"history.html",context)