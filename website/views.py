from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Feedback, Trip, TripSchedule, Booking # Add Trip and Booking
from .forms import BookingForm
from django.contrib import messages
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
                return redirect('home')
            except (TripSchedule.DoesNotExist, ValueError):
                form.add_error(None, "An error occurred. The selected trip schedule was not found.")
    else:
        form = BookingForm()

    # Add the trip object to the context
    context = {'form': form, 'trip': trip}
    # Use the new 'trip_detail.html' template
    return render(request, "website/trip_detail.html", context)


def trip_schedules_api(request, trip_id):
    # Get only the schedules for the specific trip_id from the URL
    schedules = TripSchedule.objects.filter(trip_id=trip_id)

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