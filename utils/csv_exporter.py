import csv
from django.http import HttpResponse
from expenses.models import Expense


def export_expenses_csv():

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'Title',
        'Amount',
        'Category',
        'Department',
        'Date'
    ])

    expenses = Expense.objects.all()

    for e in expenses:

        writer.writerow([
            e.title,
            e.amount,
            e.category.name,
            e.department.name,
            e.date
        ])

    return response