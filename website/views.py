from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Feedback, Trip, TripSchedule, Booking # Add Trip and Booking
from .forms import BookingForm
from django.contrib import messages
from django.utils import timezone
from django.conf import settings # Add this line to import settings for Stripe keys
# Add these imports at the top with your other imports
import stripe
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home(request):
    trips = Trip.objects.all().order_by('id')
    feedbacks = Feedback.objects.all().order_by('-rating', '-feedback_datetime')[:5]  # Get the latest 5 feedbacks
    context = {'trips': trips, 'feedbacks': feedbacks}
    return render(request, "website/home.html", context)

def trip_detail(request, trip_id):
    # Get the specific trip we are looking at, or show a 404 error if not found
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            schedule_id = request.POST.get('scheduled_trip')
            try:
                # We only need to check schedules related to the current trip
                scheduled_trip = TripSchedule.objects.get(id=schedule_id, trip=trip)
                booking.scheduled_trip = scheduled_trip
                booking.save()
                messages.success(request, f'Thank you! Your trip to {trip.name} has been successfully booked.')
                return redirect('website:home')
            except (TripSchedule.DoesNotExist, ValueError):
                form.add_error(None, "An error occurred. The selected trip schedule was not found.")
    else:
        form = BookingForm()

    # Add the trip object to the context
    context = {'form': form, 
               'trip': trip,
               'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY}  # Pass the Stripe publishable key to the template
    # Use the new 'trip_detail.html' template
    return render(request, "website/trip_detail.html", context)


def trip_schedules_api(request, trip_id): # Calendar is using this data
    # Get only the schedules for the specific trip_id from the URL
    schedules = TripSchedule.objects.filter(trip_id=trip_id, 
                                            start_datetime__gte=timezone.now()).order_by('start_datetime')

    # Prepare the data to be returned as JSON
    events = []
    for schedule in schedules:
        events.append({
            'title': schedule.trip.name,
            'start': schedule.start_datetime.isoformat(),
            'end': schedule.end_datetime.isoformat(),
            'id': schedule.id,
            'status': schedule.status,
        })
    return JsonResponse(events, safe=False)

# Set the Stripe API key from your settings
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt # For API endpoints, CSRF handling can be different. This is the simplest approach.
@require_POST
def create_payment_intent(request):
    try:
        # Decode the incoming JSON data from the frontend
        data = json.loads(request.body)
        total_amount = data.get('amount')

        # Create a PaymentIntent with the amount and currency
        # The amount must be in the smallest currency unit (e.g., cents for EUR)
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount * 100),
            currency='eur',
            automatic_payment_methods={'enabled': True},
        )

        # Send the client secret back to the frontend
        return JsonResponse({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        # Return a JSON response with the error message
        return JsonResponse({'error': str(e)}, status=400)