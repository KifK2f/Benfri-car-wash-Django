from django.urls import path
from employees import views
from employees.views import EmployeeCreate, EmployeeHome, EmployeeUpdate, EmployeeDelete

urlpatterns = [
    path('employee/', EmployeeHome.as_view(), name='account-employee'),
    path('create-employee/', EmployeeCreate.as_view(), name='create-employee'),
    path('employee/edit/<str:slug>/', EmployeeUpdate.as_view(), name='edit-employee'),
    path('employee/delete/<str:slug>/', EmployeeDelete.as_view(), name='delete-employee'),
]



