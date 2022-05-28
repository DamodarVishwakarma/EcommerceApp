from django.urls import path
from . views import*


urlpatterns = [
    path("", home, name="ssi-home"),
    path("about", about, name="ssi-about")
]
