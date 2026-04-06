from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Booking, TripSchedule

# This function will run every time a Booking object is saved
@receiver(post_save, sender=Booking)
def update_schedule_status_on_save(sender, instance, **kwargs):
    """
    Updates the TripSchedule status to 'full' if the total number of
    participants meets or exceeds the maximum.
    """
    schedule = instance.scheduled_trip
    
    # Calculate the sum of all participants for this schedule
    total_participants = Booking.objects.filter(scheduled_trip=schedule).aggregate(
        total_adults=Sum('adults'), total_children=Sum('children')
    )
    # Add them safely (defaulting to 0 if there are no bookings)
    total_participants = (total_participants['total_adults'] or 0) + (total_participants['total_children'] or 0)
    # If the schedule is full, update its status
    if total_participants >= schedule.max_participants:
        if schedule.status != 'full': # Only save if the status changes
            schedule.status = 'full'
            schedule.save()
    # Optional: If a booking was changed/reduced, and the trip is no longer full
    elif schedule.status == 'full' and total_participants < schedule.max_participants:
        schedule.status = 'active'
        schedule.save()


# This function will run every time a Booking object is deleted
@receiver(post_delete, sender=Booking)
def update_schedule_status_on_delete(sender, instance, **kwargs):
    """
    Updates the TripSchedule status to 'active' if a booking is deleted
    and the trip is no longer full.
    """
    schedule = instance.scheduled_trip
    total_participants = Booking.objects.filter(scheduled_trip=schedule).aggregate(total=Sum('num_participants'))['total'] or 0
    if total_participants < schedule.max_participants:
        if schedule.status == 'full': # Only save if the status changes
            schedule.status = 'active'
            schedule.save()