from django import forms

CLASS_CHOICES = (
    ("economy", "Economy"),
    ("first", "First Class")
)

class conformation_form(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    number_of_seats = forms.IntegerField(label='The number of seats you would like to book')
    seats_class = forms.ChoiceField(choices=CLASS_CHOICES, label='class')

class payment_form(forms.Form):
    Card_Number = forms.CharField(label='Card Number', widget=forms.TextInput(attrs={'placeholder': 'xxxx-xxxx-xxxx-xxxx'}))
    OTP = forms.CharField(label='OTP')
