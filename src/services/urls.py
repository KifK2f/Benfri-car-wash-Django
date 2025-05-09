from django.urls import path

from services.views import ServiceHome, ServiceDetail


urlpatterns = [
    path('', ServiceHome.as_view(), name='home_service'),
    path('<str:slug>/', ServiceDetail.as_view(), name='service'),
    
]
