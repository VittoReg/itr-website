from django.db import models

# Create your models here.
class Trip(models.Model):
    name = models.CharField(max_length=100)
    description_short = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.IntegerField()  # duration in hours
    image_path = models.CharField(max_length=200, blank=True, default='images/default.jpg')  # Optional field for image path or URL

    def __str__(self):
        return self.name
    
class TripSchedule(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
        ('postponed', 'Postponed'),
        ('full', 'Full'),
    ]

    trip =models.ForeignKey(Trip, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.trip.name} on {self.start_datetime.strftime('%d-%m-%Y %H:%M')}"
    
class Booking(models.Model):
    scheduled_trip = models.ForeignKey(TripSchedule, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    booking_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.customer_name} for {self.scheduled_trip}"
    
class Feedback(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_lastname = models.CharField(max_length=100)
    customer_email = models.EmailField()
    # Define the choices
    RATING_CHOICES = [
        (1, '1 ★'),
        (2, '2 ★★'),
        (3, '3 ★★★'),
        (4, '4 ★★★★'),
        (5, '5 ★★★★★'),
    ]
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    feedback_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.customer_name} {self.customer_lastname} for {self.trip.name}"