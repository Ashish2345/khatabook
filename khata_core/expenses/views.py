from django.views.generic import ListView

from .models import Expense


class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/expenses_list.html"
