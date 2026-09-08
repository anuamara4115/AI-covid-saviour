from app.views import home, HospitalDetailView,Home, predictImage
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('services', home, name='services'),
    path('hospital/<int:pk>', HospitalDetailView.as_view(), name='hospital_detail'),
     path('', Home, name='Home'),
    path("prediction",predictImage, name="prediction")

]
