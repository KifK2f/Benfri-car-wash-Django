from django.urls import path
from customers import views
from customers.views import CustomerCreate, CustomerHome, CustomerUpdate, CustomerDelete

urlpatterns = [
    path('customer/', CustomerHome.as_view(), name='account-customer'),
    path('create-customer/', CustomerCreate.as_view(), name='create-customer'),
    path('customer/edit/<str:slug>/', CustomerUpdate.as_view(), name='edit-customer'),
    path('customer/delete/<str:slug>/', CustomerDelete.as_view(), name='delete-customer'),
    # path('ajax/load-vehicles/', views.load_vehicles, name='ajax_load_vehicles'),
]



