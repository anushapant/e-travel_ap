from django import forms

class conformation_form(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    number_of_seats = forms.IntegerField()

class payment_form(forms.Form):
    Card_Number = forms.CharField(label='Card Number', widget=forms.TextInput(attrs={'placeholder': 'xxxx-xxxx-xxxx-xxxx'}))
    OTP = forms.CharField(label='OTP')
