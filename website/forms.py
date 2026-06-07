from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_email', 'adults', 'children']
        labels = {
            'customer_name': 'Name',
            'customer_email': 'Email',
            'adults': 'Adults',
            'children': 'Children',
        }
        widgets = {
            # Option 2: Use a Dropdown (Select) for a fixed range (e.g. 1-20)
            'adults': forms.Select(
                choices=[(i, str(i)) for i in range(1, 21)], # Python creates list 1-20
                attrs={'class': 'form-select', 'style': 'width: auto; display: inline-block; align-items: center;'} # Bootstrap class for styled dropdowns
            ),
            'children': forms.Select(
                choices=[(i, str(i)) for i in range(0, 21)], # Python creates list 0-20
                attrs={'class': 'form-select', 'style': 'width: auto; display: inline-block; align-items: center;'} # Bootstrap class for styled dropdowns
            ),
        }
        