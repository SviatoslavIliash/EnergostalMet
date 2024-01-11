from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=1, step_size=1, widget=forms.NumberInput(attrs={"class": "input_quantity"}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

