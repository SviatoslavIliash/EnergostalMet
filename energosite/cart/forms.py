from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label=False, initial=1, min_value=1, required=True, step_size=1,
                                  widget=forms.NumberInput(
                                      attrs={"class": "input_quantity"}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

