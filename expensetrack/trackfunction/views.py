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

        # Validate the data as needed
        # For example, you can use try-except blocks to handle validation errors

        try:
            amount = float(amount)
            transaction_date = timezone.make_aware(timezone.datetime.strptime(transaction_date, '%Y-%m-%d'))
        except (ValueError, TypeError):
            # Handle validation errors here, e.g., return an error message to the user
            return render(request, 'addexpense.html', {'error_message': 'Invalid input'})

        Expense.objects.create(
            user=user, 
            expense_name=expense_name,
            amount=amount,
            transaction_date=transaction_date,
            category=category
        )
        messages.success(request, 'Expenses added successfully')
        return redirect('addexpense')
    return render(request,"addexpense.html")



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
    return render(request,"editexpense.html")

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