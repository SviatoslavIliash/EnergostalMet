from django import forms
from django.core.validators import RegexValidator

from store.models import UserInfo, DeliveryMethod, PaymentMethod


class UserInfoForm(forms.Form, forms.ModelForm):
    first_name = forms.CharField(label="Ім'я", max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Прізвище", max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    email = forms.CharField(label="Email", required=False, max_length=100, widget=forms.EmailInput(
        attrs={"class": "form-control"}))
    phone_number = forms.CharField(label="Номер телефону", validators=[RegexValidator(
                regex=r'^(\+38)?0\d{9}$', message='Введіть коректний номер телефону')], max_length=13,
                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "+380931234567"}))

    class Meta:
        model = UserInfo
        fields = ["first_name", "last_name", "email", "phone_number"]


class DeliveryForm(forms.Form):
    delivery_type = forms.ModelChoiceField(label="Тип доставки",
                                           queryset=DeliveryMethod.objects.filter(enabled=True).only("name"),
                                           widget=forms.Select(attrs={"class": "form-select"}))
    city = forms.CharField(label="Місто", max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    post_department = forms.CharField(label="Адреса або номер відділення", max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control"}))
    payment_type = forms.ModelChoiceField(label="Спосіб оплати",
                                          queryset=PaymentMethod.objects.filter(enabled=True).only("name"),
                                          widget=forms.Select(attrs={"class": "form-select"}))
    comment = forms.CharField(label="Коментар", required=False, max_length=200, widget=forms.TextInput(
        attrs={"class": "form-control"}))
