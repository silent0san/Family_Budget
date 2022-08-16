from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from family_budget.budget_app.models import Budget, BudgetRecord
from .serializers import BudgetSerializer, RecordSerializer
from rest_framework import status


@api_view(['GET', 'POST'])
def api_budget(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10

    if request.method == 'GET':
        all_budgets = Budget.objects.all().order_by('created_date')
        result_page = paginator.paginate_queryset(all_budgets, request)
        serializer = BudgetSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = BudgetSerializer(data=request.data)
        if request.user.is_authenticated:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE', 'PATH'])
def api_budget_management(request, budget_id):
    try:
        budget = get_object_or_404(Budget, pk=budget_id)
    except Exception as error:
        return Response(f'Budget does not exist: {str(error)}', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BudgetSerializer(budget)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BudgetSerializer(budget, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user == budget.owner:
            budget.delete()
            return Response("Budget deleted", status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PATH':
        serializer = BudgetSerializer(data=request.data, partial=True)
        if request.user == budget.owner:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def api_record_management(request, budget_id):
    try:
        budget = get_object_or_404(Budget, pk=budget_id)
    except Exception as error:
        return Response(f'Budget does not exist: {str(error)}', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        all_budgets_records = BudgetRecord.objects.all().order_by('created_date').filter(budget=budget)
        result_page = paginator.paginate_queryset(all_budgets_records, request)
        serializer = RecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = RecordSerializer(data=request.data)
        if request.user == budget.owner or request.user in budget.shared_with.all():
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
