from django import forms
from django.forms.utils import flatatt
from django.utils.html import format_html


CLASS_CHOICES = (
    ("economy", "Economy"),
    ("first", "First Class")
)

ROUND_TRIP = (
    ("yes", "Yes"),
    ("no", "No")
)

MEAL = (
    ("veg", "Yes, a vegetarian meal - $10"),
    ("non-veg", "Yes, a non-vegetarian meal - $12"),
    ("fruit", "Yes, a fruit meal - $8"),
    ("no", "No, I'm good")
)

SPECIAL_SERVICES = (
    ("exp_mother", "Expectant Mother"),
    ("um", "Unaccompanied Minor(s)"),
)


class confirmation_form(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    number_of_seats = forms.IntegerField(label='Number of seats')
    seats_class = forms.ChoiceField(choices=CLASS_CHOICES, label='Class')
    meals = forms.ChoiceField(choices=MEAL, label='Would you like to book an in-flight meal? (Extra charges are mentioned below) ',
                              widget=forms.RadioSelect)
    wheelchair = forms.IntegerField(
        label='Would you like to book an assisted wheelchair? If yes, enter the number of wheelchairs required.', required=False)
    stroller = forms.IntegerField(
        label='Would you like to book a stroller? If yes, enter the number of strollers required.', required=False)
    services = forms.ChoiceField(choices=SPECIAL_SERVICES,
                              label='Would you like assistance for any of the following?',
                              widget=forms.RadioSelect, required=False)
    round_trip = forms.ChoiceField(choices=ROUND_TRIP,label='Would you also like to book a return flight?',widget=forms.RadioSelect)

class confirmation_form2(forms.Form):
    number_of_seats = forms.IntegerField(label='Number of seats')
    seats_class = forms.ChoiceField(choices=CLASS_CHOICES, label='Class')
    meals = forms.ChoiceField(choices=MEAL, label='Would you like to book an in-flight meal? (Extra charges are mentioned below) ',
                              widget=forms.RadioSelect)
    wheelchair = forms.IntegerField(
        label='Would you like to book an assisted wheelchair? If yes, enter the number of wheelchairs required.',
        required=False)
    stroller = forms.IntegerField(
        label='Would you like to book a stroller? If yes, enter the number of strollers required.', required=False)
    services = forms.ChoiceField(choices=SPECIAL_SERVICES,
                                 label='Would you like assistance for any of the following?',
                                 widget=forms.RadioSelect, required=False)


class round_tripF(forms.Form):
    from_place = forms.CharField(label='From:')
    to_place = forms.CharField(label='To:')
    date = forms.DateField(label='Date:', widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}))
    number_of_seats = forms.IntegerField(label='The number of seats you would like to book')
    seats_class = forms.ChoiceField(choices=CLASS_CHOICES, label='Class')

class payment_form(forms.Form):
    Card_Number = forms.CharField(label='Card Number', widget=forms.TextInput(attrs={'placeholder': 'xxxx-xxxx-xxxx-xxxx'}))
    OTP = forms.CharField(label='OTP')

