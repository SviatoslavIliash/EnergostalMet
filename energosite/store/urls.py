from django.urls import path

from . import views

app_name = "store"
urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:category_slug>/", views.category_detail, name="category_detail"),
    # maybe should be moved to separate app like articles. should be discussed.
    path("article/<slug:article_slug>/", views.article, name="article"),

    path("<slug:category_slug>/<slug:product_slug>/", views.product_detail, name="product_detail"),

]
