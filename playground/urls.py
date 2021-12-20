from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('SAAMTour/',views.floor),
    path('SAAMTour/SAAMTourbyFloor/',views.say_hello),
    path('SAAMTour/SAAMTourbyNameSearch/',views.searchByName),
]  
