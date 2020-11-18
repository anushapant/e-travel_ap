from django import forms

class conformation_form(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    number_of_seats = forms.IntegerField(required=False)
