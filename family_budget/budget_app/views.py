from django.shortcuts import render


def home(request):
    return render(request, 'budget_app/home.html')
