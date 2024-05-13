from django.urls import path
from . import views

urlpatterns = [
    path("add-sensor", views.AddSensor)
]