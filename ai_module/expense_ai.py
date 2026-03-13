from django.db.models import Sum
from expenses.models import Expense


def generate_ai_insight():

    insights = []

    # Highest category
    top_category = Expense.objects.values('category__name')\
        .annotate(total=Sum('amount'))\
        .order_by('-total')\
        .first()

    if top_category:
        insights.append(
            f"💰 Highest spending category is {top_category['category__name']}."
        )

    # Highest department
    top_department = Expense.objects.values('department__name')\
        .annotate(total=Sum('amount'))\
        .order_by('-total')\
        .first()

    if top_department:
        insights.append(
            f"🏢 Department spending the most is {top_department['department__name']}."
        )

    # Highest expense
    highest = Expense.objects.order_by('-amount').first()

    if highest:
        insights.append(
            f"⚠ Highest expense recorded: ₹{highest.amount} ({highest.title})."
        )

    return " ".join(insights)