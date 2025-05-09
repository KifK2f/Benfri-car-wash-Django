from django.urls import path
from bookings import views
from bookings.views import BookingCreate, BookingHome, BookingUpdate, BookingDelete, BookingHomeReceptionist, BookingHomeCleaner
from django.conf.urls.static import static
from washing_station import settings

urlpatterns = [
    path('booking/', BookingHome.as_view(), name='home-booking'),
    path('booking-receptionist/', BookingHomeReceptionist.as_view(), name='home-booking-receptionist'),
    path('booking-cleaner/', BookingHomeCleaner.as_view(), name='home-booking-cleaner'),
    path('create-booking/', BookingCreate.as_view(), name='create-booking'),
    path('booking/edit/<str:slug>/', BookingUpdate.as_view(), name='edit-booking'),
    path('booking/delete/<str:slug>/', BookingDelete.as_view(), name='delete-booking'),
    path('ajax/load-vehicles/', views.load_vehicles, name='ajax_load_vehicles'),
    
    # path('booking/edit/<str:slug>/', BookingUpdate.as_view(), name='edit-booking'),

    # path('booking/<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



