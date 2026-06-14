from django.urls import path
from . import views

# THIS LINE REGISTERS THE 'website' NAMESPACE
app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    # API endpoint for trip schedules (calendar events)
    path('api/trips/<int:trip_id>/schedules/', views.trip_schedules_api, name='trip_schedules_api'),
     # --- THIS IS THE IMPORTANT LINE ---
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    # -- CART URLS --
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:trip_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:trip_id>/', views.cart_remove, name='cart_remove'),
]


