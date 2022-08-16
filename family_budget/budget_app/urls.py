from django.urls import path
from . import views, api_views


urlpatterns = [
    path('', views.home, name='home'),
    path('add_budget/', views.add_budget, name='add-budget'),
    path('budgets_list/', views.budgets_list, name='budgets-list'),
    path('update_budget/<budget_id>', views.update_budget, name='update-budget'),
    path('budget_records/<budget_id>', views.budget_records, name='budget-records'),
    path('delete_budget/<budget_id>', views.delete_budget, name='delete-budget'),
    path('delete_record/<record_id>', views.delete_record, name='delete-record'),
    path('share_budget/<budget_id>', views.share_budget, name='share-budget'),
    path('share_budget/<budget_id>/<user_id>', views.share_budget_user, name='share-budget-user'),
    path('delete_shared_user/<budget_id>/<user_id>', views.delete_shared_user, name='delete-shared-user'),

    path('api/budget_list/', api_views.api_budget),
    path('api/api_budget_management/<budget_id>', api_views.api_budget_management),
    path('api/api_record_management/<budget_id>', api_views.api_record_management),
]
