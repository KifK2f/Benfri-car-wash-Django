from django.urls import path
from vehicles.views import CarCreate, MotorcycleCreate, VehicleCreate, VehicleHome, CarDetail, MotorcycleDetail, CarHome, MotorcycleHome, CarUpdate, CarDelete, MotorcycleUpdate, MotorcycleDelete
from django.conf.urls.static import static

urlpatterns = [
    path('my-vehicles/', VehicleHome.as_view(), name='home-vehicle'),
    path('create-vehicle/', VehicleCreate.as_view(), name='create-vehicle'),
    
    path('car/', CarHome.as_view(), name='home-car'),
    path('create-car/', CarCreate.as_view(), name='create-car'),
    path('car/edit/<str:slug>/', CarUpdate.as_view(), name='edit-car'),
    path('car/delete/<str:slug>/', CarDelete.as_view(), name='delete-car'),
    path('car/<str:slug>/', CarDetail.as_view(), name='car'),
    
    path('motorcycle/', MotorcycleHome.as_view(), name='home-motorcycle'),
    path('motorcycle/<str:slug>/', MotorcycleDetail.as_view(), name='motorcycle'),
    path('create-motorcycle/', MotorcycleCreate.as_view(), name='create-motorcycle'),    
    path('motorcycle/edit/<str:slug>/', MotorcycleUpdate.as_view(), name='edit-motorcycle'),
    path('motorcycle/delete/<str:slug>/', MotorcycleDelete.as_view(), name='delete-motorcycle'),
]
