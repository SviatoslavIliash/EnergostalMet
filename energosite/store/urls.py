from django.urls import path

from . import views

app_name = "store"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:category_name>/", views.category_detail, name="category_detail"),
]
