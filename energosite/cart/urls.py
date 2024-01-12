from django.urls import path
from . import views

app_name = "cart"
urlpatterns = [
    path("", views.cart_detail, name='cart_detail'),
    path("remove/<slug:product_slug>/", views.cart_remove, name='cart_remove'),
    path("add/<slug:product_slug>/", views.cart_add, name='cart_add'),
]
