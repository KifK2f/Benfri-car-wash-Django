"""
URL configuration for washing_station project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from washing_station import views
from washing_station import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication_app.urls')),
    path('home-page/', views.home, name='home'),
    path('customer/', include('customers.urls')),
    path('employee/', include('employees.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('services/', include('services.urls')),
    path('bookings/', include('bookings.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
