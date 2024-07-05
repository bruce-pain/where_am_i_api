from django.urls import path
from api import views

urlpatterns = [path("get-me", views.get_me)]

