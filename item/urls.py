from django.urls import path
from . import views

urlpatterns = [
    path("item-type", views.ItemTypeView.as_view(), name="item-type"),
    path("", views.ItemView.as_view(), name="item"),
]
