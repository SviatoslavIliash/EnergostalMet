from django.urls import path, re_path
from django.templatetags.static import static
from django.views.generic import RedirectView

from . import views

app_name = "store"
urlpatterns = [
    path("", views.index, name="index"),
    re_path("favicon.ico", RedirectView.as_view(url=static('store/images/logo__blue.ico'), permanent=True)),
    path("checkout/", views.checkout, name="checkout"),
    path("success_order/<int:order_number>", views.success_order, name="success_order"),
    path("<slug:category_slug>/", views.category_detail, name="category_detail"),
    # maybe should be moved to separate app like articles. should be discussed.
    path("article/<slug:article_slug>/", views.article, name="article"),

    path("<slug:category_slug>/<slug:product_slug>/", views.product_detail, name="product_detail"),

]
