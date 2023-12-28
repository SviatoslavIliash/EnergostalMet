from django.urls import path

from . import views

app_name = "store"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:category_name>/", views.category_detail, name="category_detail"),
    path("<int:product_id>/product/", views.product_detail, name="product_detail"),

    # maybe should be moved to separate app like cart. should be discussed.
    path("cart", views.cart, name="cart"),

    # maybe should be moved to separate app like articles. should be discussed.
    path("article/<str:article_name>/", views.article, name="article"),
    #path("about", views.about, name="about"),
    #path("contacts", views.contacts, name="contacts"),
]
