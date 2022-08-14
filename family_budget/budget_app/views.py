from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import BudgetForm, RecordForm
from family_budget.budget_app.models import Budget, BudgetRecord


def home(request):
    return render(request, 'budget_app/home.html')


@login_required(login_url='/login')
def add_budget(request):
    submitted = False
    current_logged_user = User.objects.get()
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            saved_form_data = form.save(commit=False)
            saved_form_data.owner = current_logged_user
            form.save()
            return redirect("/add_budget?submitted=True")
    else:
        form = BudgetForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'budget_app/add_budget.html', {"form": form, 'submitted': submitted})


@login_required(login_url='/login')
def budgets_list(request):
    current_logged_user = User.objects.get()
    users_budgets = Budget.objects.order_by('created_date').filter(owner=current_logged_user)

    return render(request, 'budget_app/budgets_list.html', {"current_logged_user": current_logged_user,
                                                            "users_budgets": users_budgets})


@login_required(login_url='/login')
def update_budget(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)
    budget_form = BudgetForm(request.POST or None, instance=budget)

    if budget_form.is_valid():
        budget_form.save()
        return redirect('budgets-list')

    return render(request, 'budget_app/update_budget.html', {'budget': budget,
                                                             'budget_form': budget_form})


@login_required(login_url='/login')
def budget_records(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)

    records = BudgetRecord.objects.order_by('-created_date').filter(budget=budget)

    if request.method == "POST":
        record_form = RecordForm(request.POST)
        if record_form.is_valid():
            saved_form_data = record_form.save(commit=False)
            saved_form_data.budget = budget
            record_form.save()

            budget.total_value += saved_form_data.value
            budget.save()

            return HttpResponseRedirect(request.path_info)
    else:
        record_form = RecordForm()

    return render(request, 'budget_app/budget_records.html', {'budget': budget,
                                                              'record_form': record_form,
                                                              'records': records})


@login_required(login_url='/login')
def delete_record(request, record_id):
    record = BudgetRecord.objects.get(pk=record_id)

    budget_id = str(record.budget.id)
    budget = Budget.objects.get(pk=budget_id)

    record.delete()

    budget.total_value -= record.value
    budget.save()

    return redirect('/budget_records/' + budget_id)
