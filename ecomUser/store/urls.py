from django.contrib import admin
from django.urls import path
from store.views import search, store_home, product_detail

urlpatterns = [
    path("", store_home, name="ssi-store-home"),
    path("search/", search, name="search"),
    path("<slug:category_slug>/", store_home, name="ssi-store-category"),
    path("<slug:category_slug>/<slug:product_slug>/", product_detail, name="ssi-product-detail"),
]