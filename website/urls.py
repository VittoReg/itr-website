from django.urls import path
from . import views

# THIS LINE REGISTERS THE 'website' NAMESPACE
app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    #path('foro-romano/', views.foro_romano, name='foro_romano'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    # API endpoint for trip schedules (calendar events)
    path('api/trips/<int:trip_id>/schedules/', views.trip_schedules_api, name='trip_schedules_api'),
     # --- THIS IS THE IMPORTANT LINE ---
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
]

