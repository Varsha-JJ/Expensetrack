from django.shortcuts import render,redirect
from django.conf import settings 
from django.utils import timezone
from  .models import Expense
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.

@login_required(login_url='login')
@never_cache
def addexpense(request):
    category_choices = dict(Expense.CATEGORY_CHOICES)
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            expense_name = request.POST.get('name')
            amount = request.POST.get('amount')
            transaction_date = request.POST.get('date')
            category = request.POST.get('category')


          
            # Check if any of the required fields are empty
            # if not expense_name or not amount or not transaction_date or not category:
                # Display an error message
                # messages.warning(request, 'All fields must be filled.')
                # return render(request, 'addexpense.html')

            # try:
            #     amount = float(amount)
            #     transaction_date = timezone.make_aware(timezone.datetime.strptime(transaction_date, '%Y-%m-%d'))
            # except (ValueError, TypeError):
            #     # Handle validation errors here, e.g., return an error message to the user
            #     messages.warning(request, 'Invalid input')
            #     return render(request, 'addexpense.html',{'category_choices': category_choices})

            Expense.objects.create(
                user=user, 
                expense_name=expense_name,
                amount=amount,
                transaction_date=transaction_date,
                category=category
            )
            messages.success(request, 'Expenses added successfully')
            return redirect('addexpense')

        return render(request, 'addexpense.html',{'category_choices':category_choices})
    else:
        messages.warning(request, 'You are not logged in.')
        return redirect('login')




from django.db.models import Sum, Count 
@login_required(login_url='login')
@never_cache
def viewexpense(request):
    if request.user.is_authenticated: 
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
    else:
        messages.warning(request, 'You are not logged in.')
        return redirect('login')


@login_required(login_url='login')
@never_cache
def editexpense(request):
    if request.user.is_authenticated: 
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
    else:
            messages.warning(request, 'You are not logged in.')
            return redirect('login')

from django.shortcuts import get_object_or_404 
from datetime import datetime
@login_required(login_url='login')
@never_cache
def update(request,id):
    category_choices = dict(Expense.CATEGORY_CHOICES)
    if request.user.is_authenticated: 
        allitem = Expense.objects.get(id=id)
        if request.method == 'POST':
            expense_name = request.POST.get('name')
            new_amount = request.POST.get('amount')
            transaction_date_str = request.POST.get('date')
            category = request.POST.get('category')
            if new_amount is not None:
                expense = get_object_or_404(Expense, id=id)
                 # Convert the date string to a datetime object
                try:
                    transaction_date = datetime.strptime(transaction_date_str, '%b. %d, %Y')
                    # Extract the date part in 'YYYY-MM-DD' format
                    transaction_date = transaction_date.strftime('%Y-%m-%d')
                except ValueError:
                    # Handle the case where the date string is in an unexpected format
                    # You can return an error message or take appropriate action here
                    pass
                expense.expense_name = expense_name
                expense.amount = new_amount
                expense.transaction_date = transaction_date
                expense.category = category
                expense.save()
                messages.success(request, 'Amount updated successfully')
                return redirect('history')
        return render(request,"update.html",{"allitem":allitem,"category_choices":category_choices})
    else:
            messages.warning(request, 'You are not logged in.')
            return redirect('login')
 
    
@login_required(login_url='login')
@never_cache
def delete(request,id):
    if request.user.is_authenticated:    
        Expense.objects.get(id=id).delete()
        messages.success(request, 'Deleted successfully')
        return redirect('history')
    else:
            messages.warning(request, 'You are not logged in.')
            return redirect('login')


from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
@login_required(login_url='login')
@never_cache
def report(request,year=None):
    if request.user.is_authenticated:
        # If no year is specified, use the current year
        if year is None:
            year = timezone.now().year
        
        unique_years = Expense.objects.values('transaction_date__year').distinct()

        # Calculate monthly expenses for all years
        yearly_data = []
        for year_data in unique_years:
            year = year_data['transaction_date__year']
            monthly_expenses = Expense.objects.filter(
                transaction_date__year=year
            ).annotate(
                month=ExtractMonth('transaction_date')
            ).values('month').annotate(total=Sum('amount')).order_by('month')

            yearly_data.append({
                'year': year,
                'monthly_expenses': monthly_expenses,
            })


        all_years = Expense.objects.values('transaction_date__year').distinct()

        # Calculate yearly expenses for all years
        yearly_expenses = []

        for year_data in all_years:
            year = year_data['transaction_date__year']
            total_expense = Expense.objects.filter(
                transaction_date__year=year
            ).aggregate(total=Sum('amount'))
            yearly_expenses.append({'year': year, 'total': total_expense['total']})


        # Calculate category-wise expenses for the specified year
        category_expenses = Expense.objects.filter(
            transaction_date__year=year
        ).values('category').annotate(total=Sum('amount')).order_by('category')

        
        # Get a list of unique years for which you have data
        unique_years = Expense.objects.values('transaction_date__year').distinct()

        # Handle form submission and get the selected year or use the current year as the default
        selected_year = request.GET.get('year', timezone.now().year)

        # Ensure that the selected year is an integer
        try:
            selected_year = int(selected_year)
        except ValueError:
            return redirect('report')

        # Initialize data to store monthly expenses for each year
        yearly_data = []

        for year_data in unique_years:
            year = year_data['transaction_date__year']
            monthly_expenses = Expense.objects.filter(
                transaction_date__year=year
            ).annotate(
                month=ExtractMonth('transaction_date')
            ).values('month').annotate(total=Sum('amount')).order_by('month')

            yearly_data.append({
                'year': year,
                'monthly_expenses': monthly_expenses,
            })

        # Create the bar chart for the selected year or all years
        if selected_year:
            selected_data = next((data for data in yearly_data if data['year'] == selected_year), None)

            if selected_data:
                years = [selected_data['year']]
                monthly_expenses_data = [selected_data['monthly_expenses']]
                title = f'Monthly Expenses for {selected_year}'
            else:
                return redirect('report')
        else:
            years = [data['year'] for data in yearly_data]
            monthly_expenses_data = [data['monthly_expenses'] for data in yearly_data]
            title = 'Monthly Expenses for All Years'

        # Create the bar chart
        plt.figure(figsize=(8, 4))
        months = range(1, 13)

        for year, monthly_expenses in zip(years, monthly_expenses_data):
            expenses = [next((item['total'] for item in monthly_expenses if item['month'] == month), 0) for month in months]
            plt.bar(months, expenses, label=str(year))

        plt.xlabel('Months')
        plt.ylabel('Total Expenses')
        plt.title(title)
        plt.xticks(months, [
            'Jan', 'Feb', 'Mar', 'Apr',
            'May', 'Jun', 'Jul', 'Aug',
            'Sep', 'Oct', 'Nov', 'Dec',
        ])
        plt.legend()

        # Save the chart to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        chart_image = base64.b64encode(buffer.read()).decode()
        buffer.close()


        context = {
        'selected_year': selected_year,
        'chart_image': chart_image,  
        'yearly_data': yearly_data,
        'yearly_expenses': yearly_expenses,
        'category_expenses': category_expenses,
        }
        return render(request,"report.html",context)
    else:
            messages.warning(request, 'You are not logged in.')
            return redirect('login')


from reportlab.pdfgen import canvas
from django.http import FileResponse
def generate_pdf_yearly(request):
    response = FileResponse(generate_pdf_file_yearly(), 
                            as_attachment=True, 
                            filename='catalog.pdf')
    return response

def generate_pdf_file_yearly():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

   
    year = timezone.now().year

    all_years = Expense.objects.values('transaction_date__year').distinct()

        # Calculate yearly expenses for all years
    yearly_expenses = []

    for year_data in all_years:
        year = year_data['transaction_date__year']
        total_expense = Expense.objects.filter(
            transaction_date__year=year
        ).aggregate(total=Sum('amount'))
        yearly_expenses.append({'year': year, 'total': total_expense['total']})

    # Start the PDF document
    p.drawString(100, 750, "Yearly Expenses Report")
    p.drawString(100, 730, "Yearly Expenses:")  
    p.drawString(120,710,"Year") 
    p.drawString(220,710,"Total Expense") 
    

    

    y_position = 690  # Starting y-position for expenses

    for expense in yearly_expenses:
        p.drawString(120, y_position, f"{expense['year']}")
        p.drawString(220, y_position, f"Rs. {expense['total']}")
        y_position -= 20  # Adjust the y-position for the next expense


    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
    
def generate_pdf_monthly(request):
    response = FileResponse(generate_pdf_file_monthly(), 
                            as_attachment=True, 
                            filename='month.pdf')
    return response


def generate_pdf_file_monthly():
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    year = timezone.now().year 

    unique_years = Expense.objects.values('transaction_date__year').distinct()

        # Calculate monthly expenses for all years
    yearly_data = []
    for year_data in unique_years:
        year = year_data['transaction_date__year']
        monthly_expenses = Expense.objects.filter(
             transaction_date__year=year
        ).annotate(
            month=ExtractMonth('transaction_date')
        ).values('month').annotate(total=Sum('amount')).order_by('month')
        yearly_data.append({
            'year': year,
            'monthly_expenses': monthly_expenses,
        })
    
     # Start the PDF document
    p.drawString(100, 750, "Monthly Expenses Report")

    y_position = 720  # Starting y-position for expenses

    for yearly_item in yearly_data:
        year = yearly_item['year']
        p.drawString(100, y_position, f"Year: {year}")

        y_position -= 20  # Adjust the y-position for the next year's data

        for monthly_data in yearly_item['monthly_expenses']:
            month = monthly_data['month']
            total = monthly_data['total']
            p.drawString(120, y_position, f"Month: {month}")
            p.drawString(220, y_position, f"Total Expense: Rs. {total or 0}")

            y_position -= 20  # Adjust the y-position for the next month's data

    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# def generate_pdf_category(request):
#     response = FileResponse(generate_pdf_file_category(), 
#                             as_attachment=True, 
#                             filename='category_expense.pdf')
#     return response

def generate_pdf_file_category(requset):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    year = datetime.now().year
    category = Expense.objects.filter(transaction_date__year=year
        ).values('category').annotate(total=Sum('amount')).order_by('category')
    
    p.drawString(100,790,f"Category expense for {year}")
    y = 700
    p.drawString(100,730,"Category")
    p.drawString(300,730,"Total")
    p.drawString(100,720,"----------------------------------------------------------------")
    for c in category:
        category = c['category']
        amount = c['total']

            
       
        p.drawString(100,y,f"{category}")
        p.drawString(300,y,f"Rs. {amount}")
        y -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=True, 
                            filename='category_expense.pdf')






from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator
from django.db.models import Q
@login_required(login_url='login')
@never_cache
def history(request):
    if request.user.is_authenticated:
        # Get all expenses
        expenses = Expense.objects.all()

        # Filter expenses based on query parameters
        search_term = request.GET.get('search', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        category = request.GET.get('category', '')

        if search_term:
            expenses = expenses.filter(Q(expense_name__icontains=search_term) | Q(category__icontains=search_term))

        if start_date:
            expenses = expenses.filter(transaction_date__gte=start_date)

        if end_date:
            expenses = expenses.filter(transaction_date__lte=end_date)
        
        if category:
            expenses = expenses.filter(category=category)


        category_choices = dict(Expense.CATEGORY_CHOICES)

        # Paginate the results
        page = request.GET.get('page', 1)
        items_per_page = 8  # Number of items to display per page
        paginator = Paginator(expenses, items_per_page)
        expenses = paginator.get_page(page)

        # Pass the filtered and paginated expenses, along with category choices, to the template
        context = {
            'expenses': expenses,
            'search_term': search_term,
            'start_date': start_date,
            'end_date': end_date,
            'category': category,
            'categories': category_choices,  # Pass the categories to the template
        }
        return render(request, "history.html", context)
    else:
        messages.warning(request, 'You are not logged in.')
        return redirect('login')




from collections import defaultdict
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from decimal import Decimal



@login_required(login_url='login')
@never_cache
def dashboard(request):
    if request.user.is_authenticated:
        expenses = Expense.objects.all()
        # Retrieve recent transactions
        recent_transactions = Expense.objects.order_by('-transaction_date')[:5]  # Get the latest 5 transactions, adjust as needed
        # Calculate expenses by category
        expenses_by_category = defaultdict(float)
        for expense in expenses:
            category = expense.category
            amount = float(expense.amount)  # Convert Decimal to float
            expenses_by_category[category] += amount
        
        # Create a pie chart
        labels = list(expenses_by_category.keys())
        amounts = list(expenses_by_category.values())

        plt.figure(figsize=(8, 8))
        plt.pie(amounts, labels=labels, autopct='%1.1f%%', startangle=140)
        

        # Save the pie chart as an image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()

        # Convert the image to base64 for embedding in HTML
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return render(request,"dashboard.html",{'image_base64': image_base64,'recent_transactions':recent_transactions})
    else:
        messages.warning(request, 'You are not logged in.')
        return redirect('login')