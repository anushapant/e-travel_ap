from django import forms

CLASS_CHOICES = (
    ("economy", "Economy"),
    ("first", "First Class")
)

ROUND_TRIP = (
    ("yes", "Yes"),
    ("no", "No")
)

class confirmation_form(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    number_of_seats = forms.IntegerField(label='The number of seats you would like to book')
    seats_class = forms.ChoiceField(choices=CLASS_CHOICES, label='Class')
    round_trip = forms.ChoiceField(choices=ROUND_TRIP,label='Would you also like to book a return flight?',widget=forms.RadioSelect)

class confirmation_form2(forms.Form):
    number_of_seats = forms.IntegerField(label='The number of seats you would like to book')
    seats_class = forms.ChoiceField(choices=CLASS_CHOICES, label='Class')

class round_tripF(forms.Form):
    from_place = forms.CharField(label='From:')
    to_place = forms.CharField(label='To:')
    date = forms.DateField(label='Date:', widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}))
    number_of_seats = forms.IntegerField(label='The number of seats you would like to book')
    seats_class = forms.ChoiceField(choices=CLASS_CHOICES, label='Class')

class payment_form(forms.Form):
    Card_Number = forms.CharField(label='Card Number', widget=forms.TextInput(attrs={'placeholder': 'xxxx-xxxx-xxxx-xxxx'}))
    OTP = forms.CharField(label='OTP')
