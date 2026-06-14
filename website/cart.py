from decimal import Decimal
from django.conf import settings
from .models import Trip # Assuming your product model is named Trip

class Cart:
    def __init__(self, request):
        """
        Initialize the cart. The cart is stored in the session.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add_to_cart(self, trip, quantity=1, override_quantity=False):
        """
        Add a trip to the cart or update its quantity.
        """
        trip_id = str(trip.id)
        if trip_id not in self.cart:
            self.cart[trip_id] = {
                'quantity': 0,
                'price': str(trip.price)  # Store price as string to avoid serialization issues
            }
        if override_quantity:
            self.cart[trip_id]['quantity'] = quantity
        else:
            self.cart[trip_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Mark the session as modified to make sure it gets saved.
        """
        self.session.modified = True

    def remove_from_cart(self, trip):
        """
        Remove a trip from the cart.
        """
        trip_id = str(trip.id)
        if trip_id in self.cart:
            del self.cart[trip_id]
            self.save()
    
    def __iter__(self):
        """
        Iterate over the items in the cart and get the trips
        from the database.
        """
        trip_ids = self.cart.keys()
        # get the trip objects and add them to the cart
        trips = Trip.objects.filter(id__in=trip_ids)
        cart = self.cart.copy()
        for trip in trips:
            cart[str(trip.id)]['trip'] = trip

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()